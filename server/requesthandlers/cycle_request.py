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
    headers = request.headers
    data = request.json()
    sha256 = data.get('sha256')
    cron = data.get('cron')
    content_type = headers.get('Content-Type')

    # ' application/json'?
    if (headers.get('Content-Type') == 'application/json'):
        logging.error("Wrong Header! Expected: json")
        response.status = "415 Unsupported Media Type"
        response.body = {
            "error": "Please use content_type: application/json"
        }
        return response

    try:
        scheduler.add_job(func=lambda : vt_request.request_to_vt(sha256),
                          trigger='cron',id=sha256,
                          replace_existing=True, **cron)
    except Exception as e:
        print ('type is:', e.__class__.__name__)
        print_exc()

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "message": "Your schedule has been created"
    }

    return response
