import json
import os
from dotenv import load_dotenv
import openai
from utils.WeatherUtil import WeatherUtil

# 加载 .env 文件中的环境变量
load_dotenv()

try:
    # 设置 OpenAI 客户端
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    messages = [{'role': 'user', 'content': '苏州天气如何'}]

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

    arguments = ''
    name = ''
    id = ''
    msg = ''
    for chunk in stream:
        print(chunk)
        if chunk.choices[0].delta.tool_calls is not None:
            if chunk.choices[0].delta.tool_calls[0].function.name is not None:
                name = chunk.choices[0].delta.tool_calls[0].function.name
                id = chunk.choices[0].delta.tool_calls[0].id
                msg = chunk.choices[0].delta
            arguments += chunk.choices[0].delta.tool_calls[0].function.arguments
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print(arguments)
    print(name)
    result = json.loads(arguments)
    location = result.get('location')
    print(location)

    weather_info = WeatherUtil.get_weather(location)

    messages.append(msg)
    messages.append({'tool_call_id': id, 'role': 'tool', "name": "get_current_weather", 'content': weather_info})
    print(messages)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


except Exception as e:
    print(f"An error occurred: {e}")
