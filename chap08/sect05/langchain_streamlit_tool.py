import streamlit as st

from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from datetime import datetime
import pytz

import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 모델 초기화 
llm = ChatOpenAI(model = "gpt-4o-mini")

# 도구 함수 정의 
@tool
def get_current_time(timezone: str, location: str) -> str:
    """ 현재 시각을 반환하는 함수"""

    try:
        tz = pytz.timezone(timezone)

        now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        result = f'{timezone} ({location}) 현재 시각 {now}' # 타임존, 지역명, 현재 시각을 문자열로 반환

        print(result)

        return result
    except pytz.UnknownTimeZoneError:
        return f'알 수 없는 타임존: {timezone}'

tools = [get_current_time]
tool_dict = {"get_current_time": get_current_time}

llm_with_tools = llm.bind_tools(tools)


# 사용자의 메시지를 처리하는 함수 
def get_ai_response(messages):
    response = llm_with_tools.stream(messages)


    gathered = None
    for chunk in response:
        yield chunk

        if gathered is None:
            gathered = chunk
        else: 
            gathered += chunk
    
    if gathered.tool_calls:
        st.session_state.messages.append(gathered)

        for tool_call in gathered.tool_calls:
            selected_tool = tool_dict[tool_call['name']]
            tool_msg = selected_tool.invoke(tool_call)
            print(tool_msg, type(tool_msg))
            st.session_state.messages.append(tool_msg)

        for chunk in get_ai_response(st.session_state.messages):
            yield chunk

st.title(" GPT-4o LangChain Chat")

if "messages" not in st.session_state:
    st.session_state['messages'] = [
        SystemMessage('너는 사용자를 돕기 위해 최선을 다하는 인공지능 봇이다.'),
        AIMessage('How can I help you?')
    ]

for msg in st.session_state.messages:
    if msg.content:
        if isinstance(msg, SystemMessage):
            st.chat_message('system').write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message('assistance').write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message('user').write(msg.content)
        elif isinstance(msg, ToolMessage):
            st.chat_message('tool').write(msg.content)

# 사용자 입력 처리 
if prompt := st.chat_input():
    st.chat_message('user').write(prompt) # 사용자 메시지 출력 
    st.session_state.messages.append(HumanMessage(prompt)) # 사용자 메시지 저장 

    response = get_ai_response(st.session_state['messages'])

    result = st.chat_message('assistant').write_stream(response) # ai 메시지 출력
    st.session_state['messages'].append(AIMessage(result)) # ai 메시지 저장