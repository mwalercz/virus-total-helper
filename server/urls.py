from server.requesthandlers import testhandlers
from server.requesthandlers.requesthandlers import virus_info_handler
from server.requesthandlers.single_request import single_handler
from server.requesthandlers.cycle_request import cycle_handler

URLS = {"GET/test/default": testhandlers.default_handler,
        "POST/test/scheduler": testhandlers.scheduler_handler,
        "POST/test/binary": testhandlers.binary_handler,
        "POST/api/virus": virus_info_handler,
        "POST/api/singleVirusTotal": single_handler,
        "POST/api/scheduleVirusTotal": cycle_handler}
