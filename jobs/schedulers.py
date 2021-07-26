import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.reports.schedulers import delete_temp_files

scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

scheduler.add_job(delete_temp_files, 'interval', minutes=3)

atexit.register(lambda: scheduler.shutdown())
