from routes import app
from flask import Response, stream_with_context, request, jsonify, session
import os
from dotenv import load_dotenv
import openai
from queue import Queue
from services.session_service import SessionService

# 加载 .env 文件中的环境变量
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# 创建一个全局的消息队列
message_queue = Queue()


@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    session['current_session_id'] = session_id
    return jsonify(SessionService.get_history(session_id))


@app.route('/chat-stream', methods=['POST'])
def chat_stream():
    if 'current_session_id' not in session:
        return {"error": "No session ID found"}, 400

    content = request.json.get('content', 'Default message if none provided')
    current_session_id = session['current_session_id']
    SessionService.add_message(current_session_id, 'user', content)
    message_queue.put(content)
    return {"status": "Data received"}, 200


@app.route('/update', methods=['GET'])
def stream_chat():
    # 定义一个生成器函数，用于流式发送数据
    def generate():
        try:
            # 创建 OpenAI 客户端
            client = openai.OpenAI(api_key=api_key)

            while True:
                content = message_queue.get()  # 阻塞直到消息到达
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": content}],
                    stream=True,
                )

                yield "event: start\n"
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        data = chunk.choices[0].delta.content.replace('\n', '<br/>');
                        yield f"data: {data}\n\n"
                yield "event: end\n"
                yield "data: \n\n"

        except Exception as e:
            # 发送错误信息
            yield f"data:An error occurred: {e}\n\n"

    # 使用 Response 对象返回流式响应
    return Response(stream_with_context(generate()), content_type='text/event-stream')


@app.route('/response_commit', methods=['POST'])
def response_commit():

    content = request.json.get('content', 'Default message if none provided')
    current_session_id = session['current_session_id']
    SessionService.add_message(current_session_id, 'assistant', content)
    return {"status": "Data received"}, 200