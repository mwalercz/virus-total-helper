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
        self._initialize_logs()
        self._initialize_objects()
        self._initialize_signals()
        self._start_receptionist_and_scheduler()
        # self.wait_for_threads_to_finish()

    def exit_gracefully(self):
        self.receptionist.stop()

    def _initialize_logs(self):
        logging.basicConfig(filename=config.log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def _initialize_objects(self):
        self.scheduler = Scheduler()
        self.dispatcher = Dispatcher(scheduler=self.scheduler.apscheduler,
                                     urls=urls.URLS)
        self.receptionist = Receptionist(dispatcher=self.dispatcher,
                                         hostname=config.hostname,
                                         port=config.port,
                                         connection_no=config.connection_no)

    def _initialize_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def _start_receptionist_and_scheduler(self):
        self.scheduler.start()
        self.receptionist.start()

    def _wait_for_threads_to_finish(self):
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                thread.join()


