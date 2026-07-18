import os
import platform
import getpass
from datetime import datetime, date
import psutil


try:
    from browser_history import get_history
    HISTORY_AVAILABLE = True
except ImportError:
    HISTORY_AVAILABLE = False

try:
    import pyautogui
    SCREENSHOT_AVAILABLE = True
except Exception:
    SCREENSHOT_AVAILABLE = False


today = date.today()
today_str = today.strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")


username = getpass.getuser()
computer = platform.node()

folder = f"Daily_Task_{today_str}"
os.makedirs(folder, exist_ok=True)

report_file = os.path.join(folder, "daily_task_report.txt")
screenshot_file = os.path.join(folder, "desktop_screenshot.png")


os_name = platform.system()
os_release = platform.release()
os_version = platform.version()
processor = platform.processor()
python_version = platform.python_version()
machine = platform.machine()


cpu_usage = psutil.cpu_percent(interval=1)

memory = psutil.virtual_memory()

disk = psutil.disk_usage('/')


running_apps = []

for proc in psutil.process_iter(['pid', 'name']):
    try:
        name = proc.info['name']
        pid = proc.info['pid']

        if name:
            running_apps.append((name, pid))

    except Exception:
        pass

running_apps = sorted(running_apps)


today_links = []

if HISTORY_AVAILABLE:

    try:

        outputs = get_history()

        for url, visit_time in outputs.histories:

            try:

                if hasattr(visit_time, "date"):
                    d = visit_time.date()

                else:
                    d = datetime.fromisoformat(
                        str(visit_time).replace("Z", "")
                    ).date()

                if d == today:
                    today_links.append(url)

            except Exception:
                continue

    except Exception as e:
        today_links.append(f"Browser history unavailable : {e}")

# Remove duplicate URLs
today_links = list(dict.fromkeys(today_links))


screenshot_status = ""

if SCREENSHOT_AVAILABLE:

    try:
        pyautogui.screenshot(screenshot_file)
        screenshot_status = "SUCCESS"

    except Exception as e:
        screenshot_status = f"FAILED ({e})"

else:
    screenshot_status = "PyAutoGUI not available"


with open(report_file, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("          DAILY TASK ACTIVITY REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Date            : {today_str}\n")
    f.write(f"Time            : {current_time}\n")
    f.write(f"User            : {username}\n")
    f.write(f"Computer Name   : {computer}\n\n")


    f.write("SYSTEM INFORMATION\n")
    f.write("-" * 60 + "\n")

    f.write(f"Operating System : {os_name}\n")
    f.write(f"OS Release       : {os_release}\n")
    f.write(f"OS Version       : {os_version}\n")
    f.write(f"Machine          : {machine}\n")
    f.write(f"Processor        : {processor}\n")
    f.write(f"Python Version   : {python_version}\n\n")


    f.write("SYSTEM RESOURCE USAGE\n")
    f.write("-" * 60 + "\n")

    f.write(f"CPU Usage        : {cpu_usage}%\n")

    f.write(
        f"RAM Usage        : {memory.percent}% "
        f"({memory.used//(1024**3)} GB / {memory.total//(1024**3)} GB)\n"
    )

    f.write(
        f"Disk Usage       : {disk.percent}% "
        f"({disk.used//(1024**3)} GB / {disk.total//(1024**3)} GB)\n\n"
    )

    
    f.write("RUNNING APPLICATIONS\n")
    f.write("-" * 60 + "\n")

    if running_apps:

        for i, (name, pid) in enumerate(running_apps, start=1):
            f.write(f"{i}. {name} (PID : {pid})\n")

    else:
        f.write("No running applications found.\n")


    f.write("\n")
    f.write("TODAY'S BROWSER HISTORY\n")
    f.write("-" * 60 + "\n")

    if today_links:

        for i, link in enumerate(today_links[:50], start=1):
            f.write(f"{i}. {link}\n")

    else:
        f.write("No browser history found for today.\n")

  
    f.write("\n")
    f.write("SCREENSHOT STATUS\n")
    f.write("-" * 60 + "\n")

    f.write(f"{screenshot_status}\n")

    if screenshot_status == "SUCCESS":
        f.write(f"Saved To : {os.path.abspath(screenshot_file)}\n")


print("=" * 60)
print("DAILY TASK REPORT GENERATED SUCCESSFULLY")
print("=" * 60)

print("Folder        :", os.path.abspath(folder))
print("Report File   :", os.path.abspath(report_file))

if screenshot_status == "SUCCESS":
    print("Screenshot    :", os.path.abspath(screenshot_file))
else:
    print("Screenshot    :", screenshot_status)

print("CPU Usage     :", cpu_usage, "%")
print("RAM Usage     :", memory.percent, "%")
print("Disk Usage    :", disk.percent, "%")
print("=" * 60)
