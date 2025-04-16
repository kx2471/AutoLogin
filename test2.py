import time
import pyautogui

print("3초 후 마우스 이동 및 클릭합니다...")
time.sleep(3)

# 클릭 위치 확인
target_x, target_y = 417, 570
print(f"👉 이동 중: ({target_x}, {target_y})")
pyautogui.moveTo(target_x, target_y, duration=0.5)

print("🖱 클릭 실행")
pyautogui.click()
print("✅ 클릭 명령 완료")
