from server.requesthandlers import testhandlers

URLS = {"GET/test/default": testhandlers.default_handler,
        "POST/test/scheduler": testhandlers.scheduler_handler,
        "POST/test/binary": testhandlers.binary_handler}
