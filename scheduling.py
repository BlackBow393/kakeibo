from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

# main.pyを呼び出し実行する関数
def run_main():
    subprocess.run(["C:\\Users\\t9374\\OneDrive\\デスクトップ\\個人家計簿\\automation_env\\Scripts\\python.exe","main.py"])

scheduler = BlockingScheduler()

# 毎日PC稼働時かつ午前9時に定期実行1回目
scheduler.add_job(
    run_main,
    "cron",
    hour=9,
    minute=0,
    id="first_job"
)

# 毎日PC稼働時かつ正午に定期実行2回目
scheduler.add_job(
    run_main,
    "cron",
    hour=12,
    minute=0,
    id="second_job"
)

# 毎日PC稼働時かつ午後4時に定期実行1回目
scheduler.add_job(
    run_main,
    "cron",
    hour=16,
    minute=0,
    id="third_job"
)

scheduler.start()