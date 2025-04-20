import os
import time
import pyautogui
import traceback
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 환경변수 로드
load_dotenv()
USER_ID = os.getenv("USER_ID")
USER_PW = os.getenv("USER_PW")

# Chrome 설정
options = Options()
options.add_experimental_option("detach", True)
service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. 로그인
    driver.get("https://www.widenet.co.kr/intranet/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wideid")))

    driver.find_element(By.ID, "wideid").send_keys(USER_ID)
    driver.find_element(By.ID, "widepass").send_keys(USER_PW)
    driver.find_element(By.ID, "loginBtn").click()

    print("⏳ 로그인 후 대기 중...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '김상옥')]"))
    )
    print("✅ 로그인 성공!")

    # 2. 출근 모달 대기
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "wn_chul_suk_modal"))
    )
    time.sleep(2)

    # 3. 출근 선택
    select = Select(driver.find_element(By.ID, "ktype"))
    select.select_by_value("A")
    print("✅ 출근 유형 선택 완료")

    # 4. 화면 캡처
    screenshot_path = os.path.join(os.getcwd(), "screenshot_debug.png")
    driver.save_screenshot(screenshot_path)
    print(f"📸 화면 캡처 완료: {screenshot_path}")
    time.sleep(1)

    # 5. 이미지 인식 후 클릭 시도
    try:
        print("🔍 이미지 인식으로 저장 버튼 찾는 중...")
        location = pyautogui.locateOnScreen("save_button.png", confidence=0.7)

        if location:
            x, y = pyautogui.center(location)
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()
            print("✅ 저장 버튼 클릭 완료!")
        else:
            print("❌ 버튼 이미지를 찾을 수 없습니다.")

    except Exception as e:
        print("❌ 오류 발생:", e)
        traceback.print_exc()
        driver.save_screenshot("error_debug.png")
        print("📸 error_debug.png 저장됨")

except Exception as e:
    print("❌ 전반적인 오류 발생:", e)
    traceback.print_exc()
    driver.save_screenshot("error_debug.png")
    print("📸 error_debug.png 저장됨")

finally:
    # driver.quit()  # 필요시 브라우저 자동 종료
    pass
