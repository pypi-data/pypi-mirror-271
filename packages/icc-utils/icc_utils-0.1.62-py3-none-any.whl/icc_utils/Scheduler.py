import schedule
import threading
import time


class Scheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, func, trigger, *args, **kwargs):
        """
        Adds a task to the scheduler.

        Args:
            func: The function to schedule.
            trigger: A dict containing the schedule type (e.g., 'daily', 'interval', 'minute', 'at') and its parameters.
            args, kwargs: Arguments and keyword arguments for the scheduled function.
        """
        if trigger['type'] == 'interval':
            # Schedule a task that runs at a regular interval in seconds
            schedule.every(trigger['interval']).seconds.do(func, *args, **kwargs)
        elif trigger['type'] == 'daily' and 'time' in trigger:
            # Schedule a task that runs once a day at a specific time
            schedule.every().day.at(trigger['time']).do(func, *args, **kwargs)
        elif trigger['type'] == 'minute':
            # Schedule a task that runs every 'X' minutes
            schedule.every(trigger['interval']).minutes.do(func, *args, **kwargs)
        elif trigger['type'] == 'at' and 'time' in trigger:
            # Schedule a task that runs at a specific time
            schedule.every().day.at(trigger['time']).do(func, *args, **kwargs)
        else:
            raise ValueError("Unsupported trigger type or missing parameters")

        # Keep track of tasks if needed for later use or management
        self.tasks.append((func, trigger, args, kwargs))

    @staticmethod
    def run_continuously(interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    try:
                        schedule.run_pending()
                        time.sleep(interval)
                    except (KeyboardInterrupt, SystemExit):
                        cease_continuous_run.set()  # Signal to stop the loop
                        schedule.clear()  # Clear all scheduled tasks

        continuous_thread = ScheduleThread()
        continuous_thread.start()

        try:
            while continuous_thread.is_alive():
                continuous_thread.join(timeout=1)  # Wait for the thread to finish unless interrupted
        except (KeyboardInterrupt, SystemExit):
            cease_continuous_run.set()  # Ensure that the event is set to stop the thread in case of interruption
            continuous_thread.join()  # Wait for the thread to properly finish

        print("Scheduler stopped and exited cleanly.")

