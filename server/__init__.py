import configparser
import logging
import os
import threading
import signal

from . import urls
from . import config
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .receptionist import Receptionist


class App:
    def initialize(self):
        self._initialize_config()
        self._initialize_logs()
        self._initialize_objects()
        self._initialize_signals()
        self._start_receptionist_and_scheduler()
        # self._wait_for_sigint()

    def handle_sig(self, signum, frame):
        self.receptionist.stop()

    def exit_gracefully(self):
        # os.kill(os.getpid(), signal.SIGINT)
        self.receptionist.stop()

    def _initialize_logs(self):
        logging.basicConfig(filename=config.log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def _initialize_config(self):
        cfg = configparser.ConfigParser()
        cfg.read('../config.ini')
        config.hostname = cfg['connection']['Host']
        config.port = int(cfg['connection']['Port'])
        config.connection_no = int(cfg['connection']['Number'])
        config.html_dir = cfg['paths']['Html']
        config.log_filename = cfg['paths']['Logs']
        config.absolute_path = cfg['paths']['Absolute']

    def _initialize_objects(self):
        self.scheduler = Scheduler()
        self.dispatcher = Dispatcher(scheduler=self.scheduler.apscheduler,
                                     urls=urls.URLS)
        self.receptionist = Receptionist(dispatcher=self.dispatcher,
                                         hostname=config.hostname,
                                         port=config.port,
                                         connection_no=config.connection_no)

    def _initialize_signals(self):
        signal.signal(signal.SIGINT, self.handle_sig)
        signal.signal(signal.SIGTERM, self.handle_sig)

    def _start_receptionist_and_scheduler(self):
        self.scheduler.start()
        self.receptionist.start()

    def _wait_for_sigint(self):
        signal.pause()
