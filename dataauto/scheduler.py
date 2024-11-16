# dataauto/scheduler.py

import schedule
import time
import threading
import subprocess
import sys

def run_command(command, file_path):
    """Run a CLI command using subprocess."""
    subprocess.run([sys.executable, '-m', 'dataauto.cli', command, file_path])

def schedule_command(command, file_path, schedule_time):
    """
    Schedule a CLI command at a specific time using the schedule module.

    Parameters:
        command (str): CLI command to execute.
        file_path (str): File path to pass to the command.
        schedule_time (str): Time to execute the command in HH:MM format.

    Returns:
        None
    """
    def job():
        run_command(command, file_path)

    try:
        schedule.every().day.at(schedule_time).do(job)
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    except Exception as e:
        raise e

def run_scheduler():
    """Run the scheduler to execute pending jobs."""
    while True:
        schedule.run_pending()
        time.sleep(1)