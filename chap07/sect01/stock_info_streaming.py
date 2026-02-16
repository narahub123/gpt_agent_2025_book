from gpt_functions import get_current_time, tools, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client= OpenAI(api_key=api_key)

def get_ai_response(messages, tools=None, stream=True):
    response = client.chat.completions.create(
        model="gpt-4o", 
        stream=stream,
        messages=messages,
        tools=tools
    )

    if stream:
        for chunk in response:
            yield chunk

    else:
         return response

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야"}    
    ]

for msg in st.session_state.messages:
    if msg['role'] == 'assistant' or msg['role'] == 'user':
        st.chat_message(msg['role']).write(msg['content'])  

if user_input := st.chat_input():
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    st.chat_message('user').write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    # print(ai_response)

    content = ''
    tool_calls = None

    with st.chat_message('assistant').empty():
        for chunk in ai_response:
            content_chunk = chunk.choices[0].delta.content
            if content_chunk:
                print(content_chunk, end='')
                content += content_chunk
                st.markdown(content) # 스트림릿 챗 메시지에 마크다운으로 출력 
    
    print('\n================')
    print(content)

    # ai_message = ai_response.choices[0].message
    
    # tool_calls = ai_message.tool_calls

    if tool_calls: # toole_calls가 존재하는 경우
        for tool_call in tool_calls:

            tool_name = tool_call.function.name
            tool_call_id = tool_call.id

            arguments = json.loads(tool_call.function.arguments) # arguments는 JSON 문자열이므로 파싱 필요

            if tool_name == "get_current_time":
                func_result = get_current_time(timezone=arguments['timezone'])
            elif tool_name == 'get_yf_stock_info':
                func_result = get_yf_stock_info(ticker=arguments['ticker'])
            elif tool_name == 'get_yf_stock_history':
                func_result = get_yf_stock_history(ticker=arguments['ticker'], period=arguments['period'])
            elif tool_name == 'get_yf_stock_recommendations':
                func_result = get_yf_stock_recommendations(ticker=arguments['ticker'])

            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": func_result
            })  

        st.session_state.messages.append({'role': 'system', 'content': '이제 주어진 결과를 바탕으로 답변할 차례다.'})

        

        ai_response = get_ai_response(st.session_state.messages)
        ai_message = ai_response.choices[0].message

    st.session_state.messages.append({
        'role': 'assistant',
        'content': content
    })

    print("AI\t: " + content) # AI 응답 출력

    # st.chat_message('assistant').write(ai_message.content)


