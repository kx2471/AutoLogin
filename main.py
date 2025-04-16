import os
import time
import pyautogui
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 📌 환경변수 로드
load_dotenv()
USER_ID = os.getenv("USER_ID")
USER_PW = os.getenv("USER_PW")

# 📌 Chrome 설정
options = Options()
options.add_experimental_option("detach", True)  # 브라우저 창 유지

service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. 로그인 페이지 이동
    driver.get("https://www.widenet.co.kr/intranet/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wideid")))

    # 2. 로그인 입력
    driver.find_element(By.ID, "wideid").send_keys(USER_ID)
    driver.find_element(By.ID, "widepass").send_keys(USER_PW)
    driver.find_element(By.ID, "loginBtn").click()

    # 3. 로그인 성공 확인 (이름으로 확인)
    print("⏳ 로그인 후 대기 중...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '김상옥')]"))
    )
    print("✅ 로그인 성공!")

    # 4. 출근 모달 대기
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "wn_chul_suk_modal"))
    )
    time.sleep(2)  # 모달 로딩 여유

    # 5. 출근 유형 선택
    select = Select(driver.find_element(By.ID, "ktype"))
    select.select_by_value("A")
    print("✅ 출근 유형 '출근(A)' 선택 완료")

    # 6. 저장 버튼 위치 클릭 (화면 확인용)
    screenshot_path = os.path.join(os.getcwd(), "screenshot_debug.png")
    driver.save_screenshot(screenshot_path)
    print(f"📸 화면 캡처 완료: {screenshot_path}")

    # 7. 마우스로 물리 클릭 (미리 측정한 좌표 사용)
    x, y = 417, 570
    print(f"🖱 마우스 클릭 위치: ({x}, {y})")
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click()
    print("✅ 물리 클릭 완료")

except Exception as e:
    print("❌ 오류 발생:", e)
    driver.save_screenshot("error_debug.png")
    print("📸 error_debug.png 저장됨")

finally:
    # 브라우저는 확인을 위해 열어두고 종료는 수동
    pass
