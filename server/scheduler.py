from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from server.queuerequest import Queuerequest
from server.requesthandlers import vt_request
import queue
import logging

class Scheduler:
    def __init__(self):
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': {'type': 'threadpool', 'max_workers': 50},
            'processpool': ProcessPoolExecutor(max_workers=20)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.apscheduler = BackgroundScheduler()

    def do_requests(self):
        try:
            sha256 = Queuerequest.queue_request.pop()
        except queue.Empty:
            return
        self.add_job(lambda: vt_request.request_to_vt(sha256))

    def start(self):
        self.apscheduler.start()
        cron = {"second": "20"}
        self.apscheduler.add_job(func=lambda: self.do_requests(),
                                trigger='cron',
                                replace_existing=True, **cron)
