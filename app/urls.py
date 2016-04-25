from app.requesthandlers import requesthandlers

URLS = {"GET/test/default": requesthandlers.default_handler,
        "POST/test/scheduler": requesthandlers.scheduler_handler,
        "POST/test/binary": requesthandlers.binary_handler}
