import tkinter as tk
from tkinter import messagebox, simpledialog, font
from tkcalendar import Calendar
import datetime
import json
import os
import threading
import time
import pystray
from PIL import Image, ImageDraw
from main import run_main

SCHEDULE_FILE = "schedules.json"

def load_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        return {}
    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)

def save_schedules(data):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def run_scheduler(schedules, get_time, get_credentials):
    def check_loop():
        while True:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            current_time = get_time()
            for date in schedules:
                dt = f"{date} {current_time}"
                if now == dt:
                    print(f"⏰ 실행 시간 도달: {dt} → main.py 실행 중...")
                    user_id, user_pw, user_name = get_credentials()
                    run_main(user_id, user_pw, user_name)
            time.sleep(30)
    threading.Thread(target=check_loop, daemon=True).start()

def get_user_credentials():
    user_id = simpledialog.askstring("로그인 정보", "아이디를 입력하세요:")
    user_pw = simpledialog.askstring("로그인 정보", "비밀번호를 입력하세요:", show="*")
    user_name = simpledialog.askstring("로그인 정보", "이름을 입력하세요 (ex: 김상옥):")
    return user_id, user_pw, user_name

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("자동 출근 스케줄러")
        self.root.geometry("800x500")

        self.user_id, self.user_pw, self.user_name = get_user_credentials()

        self.cal_font = font.Font(family="Helvetica", size=16)

        self.calendar = Calendar(
            root,
            mindate=datetime.date.today(),
            date_pattern="yyyy-mm-dd",
            font=self.cal_font
        )
        self.calendar.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.time_button = tk.Button(root, text="시간 설정", command=self.set_time)
        self.time_button.pack(pady=10)

        self.time_var = tk.StringVar(value="09:00")
        self.schedules = load_schedules()
        self.last_clicked_date = None

        self.highlight_scheduled_dates()
        self.update_button()

        self.calendar.bind("<<CalendarSelected>>", self.handle_date_click)

        run_scheduler(
            self.schedules,
            lambda: self.time_var.get(),
            lambda: (self.user_id, self.user_pw, self.user_name)
        )

        self.setup_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    # ---------------- 스케줄 처리 ----------------

    def highlight_scheduled_dates(self):
        self.calendar.calevent_remove('all')
        for date_str in self.schedules:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                self.calendar.calevent_create(date_obj, "일정 있음", "scheduled")
            except Exception as e:
                print(f"날짜 파싱 오류: {date_str}", e)
        self.calendar.tag_config("scheduled", background="yellow", foreground="black")

    def update_button(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        selected_date = self.calendar.get_date()
        today = datetime.date.today().strftime("%Y-%m-%d")

        if selected_date < today:
            return

        if selected_date in self.schedules:
            tk.Button(self.button_frame, text="일정 삭제", command=self.delete_schedule).pack()
        else:
            tk.Button(self.button_frame, text="일정 추가", command=self.add_schedule).pack()

    def add_schedule(self):
        date = self.calendar.get_date()
        self.schedules[date] = True
        save_schedules(self.schedules)
        self.highlight_scheduled_dates()
        messagebox.showinfo("일정 추가", f"{date} 일정이 추가되었습니다.")
        self.update_button()

    def delete_schedule(self):
        date = self.calendar.get_date()
        if date in self.schedules:
            del self.schedules[date]
            save_schedules(self.schedules)
            self.highlight_scheduled_dates()
            messagebox.showinfo("일정 삭제", f"{date} 일정이 삭제되었습니다.")
            self.update_button()

    def set_time(self):
        time_input = simpledialog.askstring("시간 설정", "시간을 입력하세요 (HH:MM)", initialvalue=self.time_var.get())
        if time_input:
            try:
                datetime.datetime.strptime(time_input, "%H:%M")
                self.time_var.set(time_input)
            except ValueError:
                messagebox.showerror("시간 형식 오류", "올바른 시간 형식(HH:MM)을 입력하세요.")

    def handle_date_click(self, event=None):
        selected_date = self.calendar.get_date()
        today = datetime.date.today().strftime("%Y-%m-%d")

        if selected_date < today:
            return

        if selected_date == self.last_clicked_date:
            if selected_date in self.schedules:
                self.delete_schedule()
            else:
                self.add_schedule()
        else:
            self.last_clicked_date = selected_date
            self.update_button()

    # ---------------- 트레이 관련 ----------------

    def setup_tray_icon(self):
        icon_image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("복원", self.restore_window),
            pystray.MenuItem("종료", self.exit_app)
        )
        self.tray_icon = pystray.Icon("출근도우미", icon_image, "출근 스케줄러", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_image(self):
        image = Image.new("RGB", (64, 64), "white")
        draw = ImageDraw.Draw(image)
        draw.ellipse((10, 10, 54, 54), fill="gold")
        return image

    def minimize_to_tray(self):
        self.root.withdraw()
        print("🪄 창이 트레이로 최소화됨")

    def restore_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def exit_app(self, icon=None, item=None):
        print("👋 종료됨")
        self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

# ---------------- 실행 ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
