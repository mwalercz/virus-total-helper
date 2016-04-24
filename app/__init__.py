import logging
import threading
import signal

from . import config
from .urls import URLS
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .receptionist import Receptionist


class App:
    def initialize(self):
        self.initialize_logs()
        self.initialize_objects()
        self.initialize_signals()
        self.start_receptionist_and_scheduler()
        # self.wait_for_threads_to_finish()

    def initialize_logs(self):
        logging.basicConfig(filename=config.log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def initialize_objects(self):
        self.scheduler = Scheduler()
        self.dispatcher = Dispatcher(scheduler=self.scheduler.apscheduler,
                                     urls=urls.URLS)
        self.receptionist = Receptionist(dispatcher=self.dispatcher,
                                         port=config.port,
                                         connection_no=config.connection_no)

    def initialize_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def start_receptionist_and_scheduler(self):
        self.scheduler.start()
        self.receptionist.start()

    def wait_for_threads_to_finish(self):
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                thread.join()

    def exit_gracefully(self):
        self.receptionist.stop()
