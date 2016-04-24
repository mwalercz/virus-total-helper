import inspect


class Dispatcher:
    def __init__(self, urls, scheduler):
        self.urls = urls
        self.scheduler = scheduler

    def dispatch(self, request):
        fun = self._pick_handler_function(request.command, request.path)
        return self._execute_handler_function(request, fun)

    def _pick_handler_function(self, command, path):
        return self.urls[command + path]

    def _execute_handler_function(self, request, fun):
        parameter_number = len(inspect.signature(fun).parameters)
        if parameter_number == 1:
            return fun(request)
        elif parameter_number == 2:
            return fun(request, self.scheduler)
        else:
            raise ArgumentLookupError(fun)


class ArgumentLookupError(Exception):
    def __init__(self, fun):
        self.fun = fun

    def __str__(self):
        return repr('cant find proper params in' + self.fun)
