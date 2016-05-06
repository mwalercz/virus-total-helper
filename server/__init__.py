import logging
import threading
import signal

import urls
from . import config
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .receptionist import Receptionist


class App:
    def initialize(self):
        self._initialize_logs()
        self._initialize_config()
        self._initialize_objects()
        self._initialize_signals()
        self._start_receptionist_and_scheduler()
        self._wait_for_recepcionist_to_finish()

    def exit_gracefully(self):
        self.receptionist.stop()

    def _initialize_logs(self):
        logging.basicConfig(filename=config.log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def _initialize_config(self):
        config_file = open('../config.ini')
        config_dict = {}
        config_line = config_file.readline()
        config_word = []
        while config_line != "":
            if config_line != "\n":
                config_word = config_line.split(" = ")
                config_dict[config_word[0]] = config_word[1].strip(""" '"\n""")
            config_line = config_file.readline()

        config.log_filename = config_dict["log_filename"]
        config.html_dir = config_dict["html_dir"]
        config.port = int(config_dict["port"])
        config.connection_no = int(config_dict["connection_no"])
        config.hostname = config_dict["hostname"]

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

    def _wait_for_recepcionist_to_finish(self):
        for thread in threading.enumerate():
            if thread.getName() == "Recepcionist":
                thread.join()
