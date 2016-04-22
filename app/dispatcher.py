import inspect


class Dispatcher:
    def __init__(self, urls):
        self.urls = urls

    def dispatch_request(self, request):
        fun = self._pick_handler_function(request.command, request.path)
        return self._execute_handler_function(request, fun)

    def _pick_handler_function(self, command, path):
        return self.urls[command + path]

    def _execute_handler_function(self, request, fun):
        if 'request' in inspect.signature(fun).parameters:
            return fun(request)
        if 'binary' in inspect.signature(fun).parameters:
            return fun(request.get_binary())
        if 'json' in inspect.signature(fun).parameters:
            return fun(request.get_json())
        raise ArgumentLookupError(fun)


class ArgumentLookupError(Exception):
    def __init__(self, fun):
        self.fun = fun

    def __str__(self):
        return repr('cant find proper params in' + self.fun)
