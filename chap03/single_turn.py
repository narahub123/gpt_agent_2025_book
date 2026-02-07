from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client= OpenAI(api_key=api_key)

while True:
    user_input = input("사용자: ")

    if user_input == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-4o", # 사용할 모델 설정
        temperature=0.9, # 생성 다양성 조절 (0.0~1.0) 1에 가까울수록 창의적이고 일관되지 않은 응답 생성
        messages=[
            {"role": "system", "content": "너는 사용자를 도와주는 상담사야"},
            {"role": "user", "content": user_input}
        ]
    )

    print("AI: " + response.choices[0].message.content)