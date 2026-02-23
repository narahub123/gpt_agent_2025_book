from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from typing_extensions import TypedDict
from typing import List

from utils import save_state # 나중에 작성 예정 

from datetime import datetime 

from dotenv import load_dotenv
import os 

load_dotenv()
os.getenv("OPENAI_API_KEY")

# 현재 폴더 경로 찾기 
# 랭그래프 이미지로 저장 및 추후 작업 결과 파일 저장 경로로 활용 
filename = os.path.basename(__file__)
absolute_path = os.path.abspath(__file__)
current_path = os.path.dirname(absolute_path)

# 모델 초기화 
llm = ChatOpenAI(model="gpt-4o")

# 상태 정의 
class State(TypedDict):
    messages: List[AnyMessage|str]

# 사용자와 대화할 노드(agent) : communicator 
def communicator(state: State):
    print("\n\n==============COMMUNICATOR================")

    communicator_system_prompt = PromptTemplate.from_template(
        """
        너는 책을 쓰는 AI 팀의 커뮤니케이터로서, 
        AI 팀의 진행 상황을 사용자에게 보고하고, 사용자의 의견을 파악하기 위해 대화를 나눈다.

        messages: {messages}
        """
    )

    system_chain = communicator_system_prompt | llm

    #  상태 메시지 가져오기 
    messages = state['messages']

    # 입력값 정의 
    inputs = {'messages': messages}

    gathered = None

    print('\nAI\t: ', end='')
    for chunk in system_chain.stream(inputs):
        print(chunk.content, end='')

        if gathered is None:
            gathered = chunk
        else:
            gathered += chunk

    messages.append(gathered)

    return {'messages': messages}

# 상태 그래프 정의 
graph_builder = StateGraph(State)

# Nodes 
graph_builder.add_node("communicator", communicator)

# Edges 
graph_builder.add_edge(START, 'communicator')
graph_builder.add_edge('communicator', END)

graph = graph_builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path=absolute_path.replace('.py', '.png'))

# 상태 초기화 
state = State(
    messages=[
        SystemMessage(
            f"""
            너희 AI들은 사용자의 요구에 맞는 책을 쓰는 작가 팀이다.
            사용자가 사용하는 언어로 대화하라.

            현재 시각은 {datetime.now().strftime('%Y-%m=%d %H:%M:%S')}이다.
            """
        )
    ]
)

# 터미널 창에서 사용자의 입력을 받고 graph를 실행하는 부분 
while True:
    user_input = input("\nUser\t:").strip()

    if user_input.lower() in ['exit', 'quit', 'q']:
        print('Goodbye!')
        break
    
    state['messages'].append(HumanMessage(user_input))
    state = graph.invoke(state)

    print('\n----------------------- Messages Conunt\t', len(state["messages"]))

    save_state(current_path, state) # 현재 state 내용 저장 