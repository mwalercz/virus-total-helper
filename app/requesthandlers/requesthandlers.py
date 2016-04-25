import logging


def default_handler(request, response):
    response.body = {'greetings': 'hello world'}
    return response


def scheduler_handler(request, response, scheduler):
    param = request.json()
    scheduler.add_job(lambda: scheduler_job(param))
    response.body = param
    return response


def binary_handler(request, response):
    # binary jest typu b''
    binary = request.binary()
    # nasz serwer umie wysylac tylko jsony wiec trzeba to co dostalismy na jsona
    response.body = {"binary_request": binary.decode('utf-8')}
    return response


def scheduler_job(x):
    logging.debug("scheduler_job: " + str(x))
