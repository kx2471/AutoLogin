import pyautogui
import time

time.sleep(3)  # 3초 안에 마우스를 원하는 위치로 옮기세요

# 현재 마우스 좌표 출력
print("현재 마우스 위치:", pyautogui.position())

# 화면 스크린샷 저장
screenshot = pyautogui.screenshot()
screenshot.save("screenshot_debug.png")
print("📸 스크린샷 저장 완료!")
