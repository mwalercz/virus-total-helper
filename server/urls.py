from server.requesthandlers import test_requests
from server.requesthandlers.virus_info_request import virus_info_handler
from server.requesthandlers.single_request import single_handler
from server.requesthandlers.cycle_request import cycle_handler

URLS = {"GET/test/default": test_requests.default_handler,
        "POST/test/scheduler": test_requests.scheduler_handler,
        "POST/test/binary": test_requests.binary_handler,
        "POST/api/virus": virus_info_handler,
        "POST/api/singleVirusTotal": single_handler,
        "POST/api/scheduleVirusTotal": cycle_handler}
