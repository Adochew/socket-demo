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

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

except Exception as e:
    print(f"An error occurred: {e}")
