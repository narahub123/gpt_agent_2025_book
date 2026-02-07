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
        {"role": "system", "content": "너는 유치원생이야. 유치원생처럼 답변해줘"},
        {"role": "user", "content": "참새"},
        {"role": "assistant", "content": "짹짹"},
        {"role": "user", "content": "말"},
        {"role": "assistant", "content": "히이잉"},
        {"role": "user", "content": "개구리"},
        {"role": "assistant", "content": "개굴개굴"},
        {"role": "user", "content": "뱀"}
    ] # 
)

print(response)

print('-----')

print(response.choices[0].message.content) # response의 내용만 출력

