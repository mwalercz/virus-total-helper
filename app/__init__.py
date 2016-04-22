import logging

from app import config
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .receptionist import Receptionist


def initialize():
    logging.basicConfig(filename=config.log_filename,
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(name)s  %(message)s')
    scheduler = Scheduler()
    dispatcher = Dispatcher(scheduler=scheduler.aps_scheduler,
                            urls=config.urls)
    receptionist = Receptionist(dispatcher=dispatcher,
                                port=config.port,
                                connection_no=config.connection_no)
    # scheduler.start()
    # receptionist.start_loop()
