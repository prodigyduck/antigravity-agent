# Refactor agent.py for Dynamic Input

## Goal Description
Modify `agent.py` to accept target URL and user requirements via command-line arguments instead of hardcoded values. This allows the user to generate test scripts for different scenarios without modifying the code.

## Proposed Changes

### [agent.py](file:///c:/projects/exLangGraph/agent.py)
- Import `argparse`.
- In `if __name__ == "__main__":` block:
    - Initialize `argparse.ArgumentParser`.
    - Add arguments `--url` (default: https://www.google.com) and `--requirement` (required).
    - Parse arguments.
    - Pass parsed arguments to `run_antigravity_agent`.

## Verification Plan

### Automated Tests
- Run the script with custom arguments and verify `generated_test.py` reflects the new requirement.
    ```bash
    python agent.py --url "https://www.naver.com" --requirement "네이버 메인 페이지에서 검색창을 찾고 'Playwright'를 입력하는 테스트를 작성해줘."
    ```
- Check if `generated_test.py` contains "https://www.naver.com" and logic for Naver.
