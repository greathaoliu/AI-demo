from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥
client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model='deepseek-ai/DeepSeek-R1',
    messages=[
        {'role': 'user',
        'content': "中国大模型行业2025年将会迎来哪些机遇和挑战"}
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end='')
