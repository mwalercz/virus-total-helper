import logging


def default_handler(request, response):
    response.body = {'greetings': 'hello world'}
    return response


def scheduler_handler(request, response):
    param = request.json()
    request.scheduler.add_job(lambda: scheduler_job(param))
    response.body = param
    return response


def binary_handler(request, response):
    # binary jest typu b''
    binary = request.binary()
    # nasz serwer umie odsylac tylko JSONY
    # dlatego body ma byc obiektem obslugiwanym przez json.dumps(), czyli dict, list itp
    response.body = {"binary_request": binary.decode('utf-8')}
    return response


def scheduler_job(x):
    logging.debug("scheduler_job: " + str(x))
