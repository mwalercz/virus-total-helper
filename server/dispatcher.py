import inspect

from server.http import HTTPResponse


class NoSuchUrl(Exception):
    def __init__(self, url):
        self.url = url


class Dispatcher:
    def __init__(self, urls, scheduler):
        self.urls = urls
        self.scheduler = scheduler

    def dispatch(self, request):
        fun = self._pick_handler_function(request.command, request.path)
        return self._execute_handler_function(request, fun)

    def _pick_handler_function(self, command, path):
        key = command + path
        if key in self.urls:
            return self.urls[key]
        else:
            raise NoSuchUrl(key)

    def _execute_handler_function(self, request, fun):
        parameter_number = len(inspect.signature(fun).parameters)
        if parameter_number == 2:
            return fun(request, HTTPResponse())
        elif parameter_number == 3:
            return fun(request, HTTPResponse(), self.scheduler)
        else:
            raise ArgumentLookupError(fun)


class ArgumentLookupError(Exception):
    def __init__(self, fun):
        self.fun = fun

    def __str__(self):
        return repr('cant find proper params in' + self.fun)
