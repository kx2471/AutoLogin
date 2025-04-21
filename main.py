def run_main(USER_ID, USER_PW, USER_NAME):
    import os
    import time
    import pyautogui
    import traceback
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC

    options = Options()
    options.add_experimental_option("detach", True)
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.widenet.co.kr/intranet/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wideid")))

        driver.find_element(By.ID, "wideid").send_keys(USER_ID)
        driver.find_element(By.ID, "widepass").send_keys(USER_PW)
        driver.find_element(By.ID, "loginBtn").click()

        print("⏳ 로그인 후 대기 중...")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(), '{USER_NAME}')]"))
        )
        print("✅ 로그인 성공!")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "wn_chul_suk_modal"))
        )
        time.sleep(2)

        select = Select(driver.find_element(By.ID, "ktype"))
        select.select_by_value("A")
        print("✅ 출근 유형 선택 완료")

        screenshot_path = os.path.join(os.getcwd(), "screenshot_debug.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 화면 캡처 완료: {screenshot_path}")
        time.sleep(1)

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
        pass
