
import time
from playwright.sync_api import sync_playwright, expect

def test_naver_homepage_elements():
    """
    Naver 홈페이지의 주요 요소(검색창, 버튼)를 검증하는 테스트 함수.
    """
    print("--- Playwright 테스트 시작 (Naver.com) ---")
    
    # 1. Playwright 컨텍스트 시작
    with sync_playwright() as p:
        # 2. 브라우저 실행 (Chromium, headless=False로 설정하여 실행 과정을 시각적으로 확인)
        # slow_mo=500ms를 설정하여 각 동작 사이에 0.5초 지연을 줍니다.
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        try:
            # 3. Naver 홈페이지 접속
            print("ACTION: https://www.naver.com 으로 이동 중...")
            page.goto("https://www.naver.com")

            # 4. 페이지 제목 검증 (기본 로딩 확인)
            expect(page).to_have_title("NAVER")
            print("PASS: 페이지 제목이 'NAVER'로 올바르게 로드되었습니다.")

            # 5. 주요 요소 파악 및 검증: 검색 입력창
            # Naver의 검색 입력창은 보통 'query' ID를 사용합니다.
            search_input_selector = "#query"
            search_input = page.locator(search_input_selector)
            
            expect(search_input).to_be_visible()
            print(f"PASS: 검색 입력창 ({search_input_selector})이 화면에 보입니다.")

            # 6. 검색 입력창에 텍스트 입력
            test_query = "QA 자동화 전문가"
            search_input.fill(test_query)
            print(f"ACTION: 검색창에 '{test_query}'를 입력했습니다.")

            # 7. 주요 요소 파악 및 검증: 검색 버튼
            # Naver의 검색 버튼은 보통 'btn_search' 클래스를 가진 버튼입니다.
            search_button_selector = "button.btn_search"
            search_button = page.locator(search_button_selector)
            
            expect(search_button).to_be_visible()
            print(f"PASS: 검색 버튼 ({search_button_selector})이 화면에 보입니다.")

            # 8. 검색 버튼 클릭
            search_button.click()
            print("ACTION: 검색 버튼을 클릭했습니다.")

            # 9. 검색 결과 페이지로 이동했는지 검증
            # URL이 'search.naver.com'을 포함하는지 확인합니다.
            page.wait_for_url(lambda url: "search.naver.com" in url)
            print("PASS: 검색 결과 페이지(search.naver.com)로 성공적으로 이동했습니다.")
            
            # 10. 최종 확인을 위해 2초 대기
            time.sleep(2)

        except Exception as e:
            print(f"ERROR: 테스트 중 오류 발생: {e}")
            
        finally:
            # 11. 브라우저 종료
            browser.close()
            print("--- Playwright 테스트 종료 ---")

if __name__ == "__main__":
    # 스크립트 실행
    test_naver_homepage_elements()
