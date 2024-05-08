import os
from dotenv import load_dotenv
import openai

# 加载 .env 文件中的环境变量
load_dotenv()

try:
    # 设置 OpenAI 客户端
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # 创建聊天完成
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}],
        model="gpt-3.5-turbo",
    )

    # 输出 API 响应
    print(chat_completion)
except Exception as e:
    print(f"An error occurred: {e}")
