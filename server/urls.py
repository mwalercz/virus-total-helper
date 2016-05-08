from server.requesthandlers import testhandlers
from server.requesthandlers.requesthandlers import virus_info_handler, single_handler

URLS = {"GET/test/default": testhandlers.default_handler,
        "POST/test/scheduler": testhandlers.scheduler_handler,
        "POST/test/binary": testhandlers.binary_handler,
        "POST/api/virus": virus_info_handler,
        "POST/api/singleVirusTotal": single_handler}
