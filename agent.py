import os
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

# LangChain & Gemini Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, ToolMessage
import operator

# 환경 변수 로드
load_dotenv()

# 1. 브라우저 도구 설정 (Playwright Tool)
# Agent가 웹사이트를 실제로 방문해서 구조를 볼 수 있게 합니다.
browser = create_sync_playwright_browser(headless=True)
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
tools = toolkit.get_tools()

# 2. LLM 설정 (Gemini Pro)
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
    convert_system_message_to_human=True
)

# 3. LangGraph 상태(State) 정의
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    target_url: str
    generated_code: str

# 4. 노드 정의: 웹사이트 분석 (Inspector)
def inspect_site(state: AgentState):
    print(f"\n🔍 [Agent] 웹사이트 분석 중: {state['target_url']}...")
    
    # Playwright 도구를 사용해 페이지 소스를 가져오는 로직을 LLM에게 시킵니다.
    # 여기서는 간단히 navigate와 get_content 도구를 LLM이 스스로 호출하게 하거나,
    # 직접 실행 로직을 짤 수 있습니다. Vibe Coding을 위해 LLM에게 맡깁니다.
    
    prompt = f"""
    당신은 QA 자동화 전문가입니다. 
    다음 URL에 접속해서 페이지의 주요 요소(버튼, 입력창, 레이아웃)를 파악하세요.
    URL: {state['target_url']}
    
    현재 사용 가능한 도구(Tools)를 사용하여 페이지 내용을 가져오세요.
    """
    
    # 도구 바인딩
    llm_with_tools = llm.bind_tools(tools)
    human_message = HumanMessage(content=prompt)
    response = llm_with_tools.invoke([human_message])
    
    messages = [human_message, response]
    if response.tool_calls:
        tool_map = {t.name: t for t in tools}
        for tool_call in response.tool_calls:
            tool = tool_map[tool_call["name"]]
            try:
                tool_output = tool.invoke(tool_call["args"])
            except Exception as e:
                tool_output = f"Error: {e}"
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))
            print(f"🔧 [Agent] 도구 실행: {tool_call['name']} -> 완료")

    return {"messages": messages}

# 5. 노드 정의: 코드 생성 (Coder)
def generate_test_script(state: AgentState):
    print("\n💻 [Agent] Playwright 테스트 스크립트 작성 중...")
    
    # 이전 단계(inspect)에서 얻은 정보를 바탕으로 코드 작성을 요청
    messages = state['messages']
    
    prompt = """
    위에서 분석한 내용을 바탕으로, Python Playwright 'sync_api'를 사용하는 독립적인 테스트 스크립트를 작성해줘.
    
    요구사항:
    1. 'generated_test.py' 라는 파일로 저장될 수 있는 완전한 파이썬 코드여야 함.
    2. 주석을 달아서 각 단계가 무엇을 하는지 설명할 것.
    3. 브라우저는 headless=False 로 설정해서 실행 과정을 볼 수 있게 할 것.
    4. 마크다운 코드 블록(```python ... ```) 안에 코드를 넣어줘.
    """
    
    response = llm.invoke(messages + [HumanMessage(content=prompt)])
    
    # 코드 블록 파싱 (간단한 후처리)
    content = response.content
    code = ""
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0]
    elif "```" in content:
        code = content.split("```")[1].split("```")[0]
    else:
        code = content
        
    return {"generated_code": code, "messages": [response]}

# 6. 그래프 연결 (Workflow)
workflow = StateGraph(AgentState)

workflow.add_node("inspector", inspect_site)
workflow.add_node("coder", generate_test_script)

# 흐름 정의: 시작 -> 분석 -> 코드생성 -> 끝
workflow.set_entry_point("inspector")
workflow.add_edge("inspector", "coder")
workflow.add_edge("coder", END)

app = workflow.compile()

# 7. 실행 함수
def run_antigravity_agent(user_requirement: str, url: str):
    print(f"🚀 [Antigravity] Vibe Coding 시작... 목표: {user_requirement}")
    
    initial_state = {
        "messages": [],
        "target_url": url,
        "generated_code": ""
    }
    
    result = app.invoke(initial_state)
    
    # 결과 파일 저장
    code = result["generated_code"]
    if code:
        with open("generated_test.py", "w", encoding="utf-8") as f:
            f.write(code)
        print("\n✨ [Success] 'generated_test.py' 파일이 생성되었습니다!")
        print("   실행 명령: python generated_test.py")
    else:
        print("\n⚠️ 코드를 생성하지 못했습니다.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Antigravity Agent: Generate Playwright tests from natural language requirements.")
    parser.add_argument("--url", type=str, default="https://www.google.com", help="Target URL to test (default: https://www.google.com)")
    parser.add_argument("--requirement", type=str, required=True, help="Natural language requirement for the test")

    args = parser.parse_args()
    
    run_antigravity_agent(args.requirement, args.url)