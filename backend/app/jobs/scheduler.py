from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from typing import Callable

def start_scheduler(run_fn: Callable[[], None], every_minutes: int = 360) -> BackgroundScheduler:
    sched = BackgroundScheduler()
    sched.add_job(run_fn, trigger=IntervalTrigger(minutes=every_minutes), id="sabia_pipeline", replace_existing=True)
    sched.start()
    return sched
