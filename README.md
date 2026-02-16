# exLangGraph: AI 기반 Playwright 테스트 자동 생성기

이 프로젝트는 **LangGraph**와 **Google Gemini (LLM)**을 결합하여, 사용자의 자연어 요구사항에 맞춰 웹 서비스의 테스트 코드를 자동으로 생성해주는 AI 에이전트 서비스입니다.

## 🚀 주요 기능

- **지능형 웹 사이트 분석**: Playwright 도구를 사용하여 대상 URL의 HTML 구조, 버튼, 입력창 등을 AI가 직접 탐색하고 분석합니다.
- **자동 코드 생성**: 분석된 사이트 구조를 바탕으로 Python Playwright (`sync_api`) 기반의 실행 가능한 테스트 스크립트를 작성합니다.
- **맞춤형 테스트 시나리오**: 명령어 인자를 통해 원하는 테스트 시나리오를 자유롭게 설정할 수 있습니다.
- **워크플로우 시각화**: LangGraph를 활용하여 '사이트 분석(Inspector) → 코드 생성(Coder)'으로 이어지는 명확한 에이전트 루프를 제공합니다.

## 🛠 기술 스택

- **Core Framework**: LangGraph, LangChain
- **LLM**: Google Gemini Flash (ChatGoogleGenerativeAI)
- **Automation**: Playwright (Browser Interaction)
- **Language**: Python

## 📦 설치 및 설정

### 1. 가상환경 및 라이브러리 설치
```bash
# 가상환경 생성 및 활성화
python -m venv venv
./venv/Scripts/activate  # Windows

# 필요 라이브러리 설치
pip install langchain-google-genai langgraph playwright python-dotenv
playwright install
```

### 2. 환경 변수 설정
프로젝트 루트 폴더에 `.env` 파일을 생성하고, [Google AI Studio](https://aistudio.google.com/)에서 발급받은 API 키를 입력합니다.
```env
GOOGLE_API_KEY=your_api_key_here
```

## 💻 사용 방법

`agent.py` 실행 시 대상 URL과 테스트 요구사항을 인자로 전달합니다.

```bash
python agent.py --url "https://www.naver.com" --requirement "네이버 검색창에 'Playwright'를 입력하고 검색 버튼을 누른 뒤 결과가 잘 나오는지 확인해줘."
```

### 실행 결과
1. 에이전트가 웹사이트에 접속하여 분석을 시작합니다.
2. 분석 완료 후 요구사항에 맞는 테스트 코드를 생성합니다.
3. 최종적으로 **`generated_test.py`** 파일이 생성됩니다.
4. 생성된 코드는 다음 명령어로 실행해볼 수 있습니다:
   ```bash
   python generated_test.py
   ```

## 📂 파일 구조

- `agent.py`: LangGraph 기반의 메인 에이전트 로직 (Inspector & Coder)
- `list_models.py`: 현재 API 키로 사용 가능한 Gemini 모델 목록 확인 스크립트
- `generated_test.py`: AI가 생성한 최종 테스트 결과물
- `.env`: API 키 저장용 환경 변수 파일

---

이 프로젝트는 LangGraph의 상태 관리(State Management)를 활용하여 AI 에이전트가 복잡한 분석 업무를 수행하도록 설계되었습니다.
