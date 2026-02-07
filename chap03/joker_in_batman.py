from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o", # 사용할 모델 설정 
    temperature=0.9, # 생성 다양성 조절 (0.0~1.0) 1에 가까울수록 창의적이고 일관되지 않은 응답 생성
    messages=[
        {"role": "system", "content": "너는 배트맨에 나오는 조커야. 조커의 악당 캐릭터에 맞게 답변해줘"},
        {"role": "user", "content": "세상에서 누가 제일 아름답니?"}
    ] # 
)

print(response)

print('-----')

print(response.choices[0].message.content) # response의 내용만 출력

