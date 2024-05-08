from routes import app
from flask import Response, stream_with_context, request, jsonify
import os
from dotenv import load_dotenv
import openai
import time

# 加载 .env 文件中的环境变量
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# 用于存储数据的列表
data_store = []


@app.route('/chat-stream', methods=['POST'])
def chat_stream():
    content = request.json.get('content', 'Default message if none provided')
    data_store.append(content)
    return {"status": "Data received"}, 200


@app.route('/update', methods=['GET'])
def stream_chat():
    # 定义一个生成器函数，用于流式发送数据
    def generate():
        last_index = 0
        try:
            # 创建 OpenAI 客户端
            client = openai.OpenAI(api_key=api_key)

            while True:
                # 循环检查是否有新内容
                while last_index < len(data_store):
                    content = data_store[last_index]
                    last_index += 1

                    stream = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": content}],
                        stream=True,
                    )

                    yield "event: start\n"
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            data = chunk.choices[0].delta.content.replace('\n', '<br/>');
                            # 发送数据块
                            yield f"data: {data}\n\n"
                    yield "event: end\n"
                    yield f"data: \n\n"
                # 等待一段时间后再次检查是否有新内容
                time.sleep(1)

        except Exception as e:
            # 发送错误信息
            yield f"data:An error occurred: {e}\n\n"

    # 使用 Response 对象返回流式响应
    return Response(stream_with_context(generate()), content_type='text/event-stream')
