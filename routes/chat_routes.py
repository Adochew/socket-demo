from routes import app
from flask import Response, stream_with_context, request, jsonify, session
import os
from dotenv import load_dotenv
import openai
import json
from queue import Queue
from services.session_service import SessionService
from utils.OSSUtil import OSSUtil
from utils.WeatherUtil import WeatherUtil

# 加载 .env 文件中的环境变量
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# 维护全局消息队列
message_queue = Queue()

# all function plugins
functions = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. 北京市 or New York"
                        }
                    },
                    "required": [
                        "location"
                    ]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_image",
                "description": "Get a image by user's prompt",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "what the image looks like, e.g. 画一只小狗 or draw a cat"
                        }
                    },
                    "required": [
                        "prompt"
                    ]
                }
            }
        }
    ]


@app.route('/chat-stream', methods=['POST'])
def chat_stream():
    if 'current_session_id' not in session:
        return {"error": "No session ID found"}, 400

    content = request.json.get('content', 'Default message if none provided')
    current_session_id = session['current_session_id']
    SessionService.add_message(current_session_id, 'user', content)

    history = SessionService.get_history(current_session_id)
    messages = [
        {"role": msg['role'], "content": msg['content']}
        for msg in history
    ]

    message_queue.put(messages)
    return {"status": "Data received"}, 200


@app.route('/update', methods=['GET'])
def stream_chat():
    # 定义一个生成器函数，用于流式发送数据
    def generate():
        # 创建 OpenAI 客户端
        client = openai.OpenAI(api_key=api_key)

        while True:
            try:
                # 从队列中获取消息
                messages = message_queue.get()
                print("Received messages:", messages)
                if messages == '[END-SSE]':
                    break

                # 创建聊天完成请求并设置为流式
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    stream=True,
                    tool_choice='auto',
                    tools=[
                        {
                            "type": "function",
                            "function": {
                                "name": "get_current_weather",
                                "description": "Get the current weather in a given location",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "location": {
                                            "type": "string",
                                            "description": "The city name, e.g. 北京市 or New York"
                                        }
                                    },
                                    "required": [
                                        "location"
                                    ]
                                }
                            },
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "get_image",
                                "description": "Get a image by user's prompt",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "what the image looks like, e.g. 画一只小狗 or draw a cat"
                                        }
                                    },
                                    "required": [
                                        "prompt"
                                    ]
                                }
                            }
                        }
                    ]
                )
                print(stream)

                # tool call参数
                id = ''
                name = ''
                msg = ''
                arguments = ''

                # 开始发送事件
                yield "event: start\n"
                # 遍历流中的每个数据块
                for chunk in stream:
                    if chunk.choices[0].delta.tool_calls is not None:
                        if chunk.choices[0].delta.tool_calls[0].function.name is not None:
                            name = chunk.choices[0].delta.tool_calls[0].function.name
                            id = chunk.choices[0].delta.tool_calls[0].id
                            msg = chunk.choices[0].delta
                        arguments += chunk.choices[0].delta.tool_calls[0].function.arguments
                    if chunk.choices[0].delta.content:
                        print(chunk)
                        data = chunk.choices[0].delta.content.replace('\n', '<br>')
                        yield f"data: {data}\n\n"

                if name == 'get_image':
                    print("Tool Calling: Get Image")
                    result = json.loads(arguments)
                    prompt = result.get('prompt')

                    yield "event: image\n"
                    yield "data: \n\n"
                    response = client.images.generate(
                        model="dall-e-2",
                        prompt=prompt,
                        size="256x256",
                        quality="standard",
                        n=1,
                    )
                    image_url = OSSUtil.upload_image(response.data[0].url)
                    yield f"data: {image_url}\n\n"
                    yield "event: end-image\n"
                    yield "data: \n\n"
                    break
                elif name == 'get_current_weather':
                    print("Tool Calling: Get Weather")
                    result = json.loads(arguments)
                    location = result.get('location')

                    weather_info = WeatherUtil.get_weather(location)
                    messages.append(msg)
                    messages.append({'tool_call_id': id, 'role': 'tool', "name": "get_current_weather", 'content': weather_info})

                    stream = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stream=True,
                        max_tokens=2000
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            data = chunk.choices[0].delta.content.replace('\n', '<br>')
                            yield f"data: {data}\n\n"

                yield "event: end\n"
                yield "data: \n\n"

            except Exception as e:
                print("An error occurred:", e)
                yield f"data: An error occurred: {str(e)}\n\n"

    # 使用 Response 对象返回流式响应
    return Response(stream_with_context(generate()), content_type='text/event-stream')


@app.route('/response_commit', methods=['POST'])
def response_commit():
    content = request.json.get('content', 'Default message if none provided')
    current_session_id = session['current_session_id']
    SessionService.add_message(current_session_id, 'assistant', content.replace('<br>', '\n'), 'text')

    message_queue.put('[END-SSE]')
    return {"status": "Data received"}, 200


@app.route('/image_commit', methods=['POST'])
def image_commit():
    content = request.json.get('content', 'Default message if none provided')
    current_session_id = session['current_session_id']
    SessionService.add_message(current_session_id, 'assistant', content, 'image')

    return {"status": "Data received"}, 200
