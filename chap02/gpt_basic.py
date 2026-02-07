from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o", # 사용할 모델 설정 
    temperature=0.1, # 생성 다양성 조절 (0.0~1.0) 1에 가까울수록 창의적이고 일관되지 않은 응답 생성
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "2022년 월드컵 우승 팀은 어디야?"}
    ] # 
)

print(response)

print('-----')

print(response.choices[0].message.content) # response의 내용만 출력

