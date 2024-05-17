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
        messages=[{'role': 'user', 'content': 'user test'}, {'role': 'assistant', 'content': 'assistant test'}, {'role': 'user', 'content': '写一首诗歌'}, {'role': 'assistant', 'content': '在这个世界上<br><br>有太多的迷茫<br><br>沉默的夜晚<br><br>心中的烦恼<br><br>我在人群中徘徊<br><br>寻找那个温暖的怀抱<br><br>却发现自己孤单<br><br>无法抹去心头的忧愁<br><br>但愿在这个世界上<br><br>有一束光照亮我<br><br>让我找到前行的方向<br><br>让我找到自己的归宿<br><br>在这个世界上<br><br>我愿化身为风<br><br>吹散所有的纷扰<br><br>让心灵再次安宁开放。'}, {'role': 'user', 'content': '翻译成英文'}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

    print(stream)

except Exception as e:
    print(f"An error occurred: {e}")