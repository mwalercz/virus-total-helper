import configparser
import json
import logging
import os
import signal
import collections

from .requesthandlers.vt_request import make_request_to_vt
from . import urls
from . import config
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .receptionist import Receptionist


class Server:
    def try_serve(self):
        try:
            self.serve()
        except OSError as error:
            logging.error("Probably port is already in use, please change port in config.ini. " + str(error))

    def serve(self):
        self._initialize_config()
        self._initialize_logs()
        self._initialize_objects()
        self._initialize_default_job()
        self._initialize_signals()
        self._start_receptionist_and_scheduler()
        # self._wait_for_sigint()

    def handle_sig(self, signum, frame):
        self.exit_gracefully()

    def exit_gracefully(self):
        self._dump_deque_to_file()
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
        config.dump_filename = cfg["paths"]["Dump"]
        config.vt_delay = cfg['vt']['Delay']

    def _initialize_objects(self):
        self.deque = collections.deque(self._get_dump())
        self.scheduler = Scheduler().apscheduler
        self.dispatcher = Dispatcher(scheduler=self.scheduler,
                                     deque=self.deque,
                                     urls=urls.URLS)
        self.receptionist = Receptionist(dispatcher=self.dispatcher,
                                         hostname=config.hostname,
                                         port=config.port,
                                         connection_no=config.connection_no)

    def _get_dump(self):
        if(os.path.isfile(config.dump_filename)):
            with open(config.dump_filename) as file:
                return json.loads(file.read())
        else:
            return []

    def _dump_deque_to_file(self):
        with open(config.dump_filename, 'w+') as file:
            file.write(json.dumps(list(self.deque)))

    def _initialize_signals(self):
        signal.signal(signal.SIGINT, self.handle_sig)
        signal.signal(signal.SIGTERM, self.handle_sig)

    def _start_receptionist_and_scheduler(self):
        self.scheduler.start()
        self.receptionist.start()

    def _wait_for_sigint(self):
        signal.pause()

    def _initialize_default_job(self):
        cron = {"second": "*/" + config.vt_delay}
        self.scheduler.add_job(func=lambda: self.check_deque_and_make_request_to_vt(),
                               trigger='cron',
                               replace_existing=True, **cron)

    def check_deque_and_make_request_to_vt(self):
        try:
            sha256 = self.deque.popleft()
            make_request_to_vt(sha256)
        except IndexError:
            logging.info("Deque is empty")
