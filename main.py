import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# 📌 .env에서 로그인 정보 불러오기
load_dotenv()
USER_ID = os.getenv("USER_ID")
USER_PW = os.getenv("USER_PW")

# 📌 Chrome 옵션 설정
options = Options()
options.add_experimental_option("detach", True)  # 브라우저 창 유지
# options.add_argument('--headless')  # 창 숨기기 (필요시 사용)

# 📌 ChromeDriver 실행
service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. 회사 인트라넷 로그인 페이지 접속
    driver.get("https://www.widenet.co.kr/intranet/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wideid")))

    # 2. 로그인 정보 입력
    driver.find_element(By.ID, "wideid").send_keys(USER_ID)
    driver.find_element(By.ID, "widepass").send_keys(USER_PW)
    driver.find_element(By.ID, "loginBtn").click()

    # 3. 대시보드 로딩 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard-card-bottom")))
    print("✅ 로그인 성공!")

    # 4. 출근 모달이 열리면 출근 처리 시도
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "wn_chul_suk_modal")))
    time.sleep(1)  # 로딩 여유 시간

    try:
        # 출근 유형 선택 (출근: A)
        select = Select(driver.find_element(By.ID, "ktype"))
        select.select_by_value("A")

        # 저장 버튼 클릭
        driver.find_element(By.ID, "chulSave").click()
        print("✅ 출근 완료!")

    except Exception as e:
        print("❌ 출근 처리 중 오류:", e)

except Exception as e:
    print("❌ 로그인 또는 페이지 진입 실패:", e)

finally:
    # 필요시 종료
    # driver.quit()
    pass
