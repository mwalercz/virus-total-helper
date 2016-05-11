# @author: Marek
# cykliczne zapytanie do VT

# TODO: sprawdzic, czy conr ma odpowiedni format
# TODO: sprawdzic czy mamy juz takie SHA w bazie

import logging
from traceback import print_exc

from server.requesthandlers import vt_request
from apscheduler.events import SchedulerEvent


def cycle_handler(request, response, scheduler):
    # obliczamy sha256 dla pliku binarnego
    try:
        data = request.json()
    except NotJsonError as error:
        logging.error("Given body is not json")
        response.status = "415 Unsupported Media Type"
        response.body = {
            "error": "Given body is not json"
        }
        return response

    sha256 = data.get('sha256')
    cron = data.get('cron')

    try:
        scheduler.add_job(func=lambda: vt_request.request_to_vt(sha256),
                          trigger='cron', id=sha256,
                          replace_existing=True, **cron)
    except Exception as e:
        logging.error("Scheduler reject job")
        response.status = "406 Not Acceptable"
        response.body = {
            "error": "Wrong parameters. Check corn or sha256"
        }
        return response

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "message": "Your schedule has been created"
    }

    return response
