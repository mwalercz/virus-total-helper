# @author: Marek
# cykliczne zapytanie do VT

import logging

from server.customhttp import NotJsonError
from server.requesthandlers import vt_request
from server.customhttp import HTTPResponse


def cycle_handler(request, response, scheduler):
    if not is_json(request, response):
        return response

    data = request.json()

    try:
        sha256, cron = _get_validated_args(data)
    except InvalidArguments:
        logging.info("Given arguments are invalid")
        response.status = "406 Not Acceptable"
        response.body = {
            "error": "Wrong parameters. Check cron or sha256"
        }
        return response

    if not (try_add_job(sha256, cron, scheduler, response)):
        return response

    if not corect_cron(cron, response):
        return response

    try:
        scheduler.remove_job(job_id=sha256)
    except Exception:
        pass

    scheduler.add_job(func=lambda: vt_request.request_to_vt(sha256),
                      trigger='cron', id='control_job',
                      replace_existing=True, **cron)

    logging.info("Cron for " + sha256 + ".html has beed changed.")

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "message": "Your schedule has been created"
    }

    return response


class InvalidArguments(Exception):
    pass


def _get_validated_args(params):
    if len(params) == 2 and "sha256" in params and "cron" in params and isinstance(params["cron"], dict):
        return params["sha256"], params["cron"]
    else:
        raise InvalidArguments


def is_json(request, response):
    try:
        data = request.json()
    except NotJsonError as error:
        logging.error("Given body is not json")
        response.status = "415 Unsupported Media Type"
        response.body = {
            "error": "Given body is not json"
        }
        return False
    return True


# badamy jedynie czy ponade wartosci mieszcza sie w przedzialach
def try_add_job(sha256, cron, scheduler, response):
    try:
        scheduler.add_job(func=lambda: vt_request.request_to_vt(sha256),
                          trigger='cron', id='control_job',
                          replace_existing=True, **cron)
    except Exception as e:
        logging.error("Scheduler reject job")
        response.status = "406 Not Acceptable"
        response.body = {
            "error": "Wrong parameters. Check cron or sha256"
        }
        return False
    return True


def corect_cron(cron, response):
    year = cron.get('year')
    month = cron.get('month')
    day = cron.get('day')
    week = cron.get('week')
    day_of_week = cron.get('day_of_week')
    hour = cron.get('hour')
    minute = cron.get('minute')
    second = cron.get('second')
    start_date = cron.get('start_date')
    end_date = cron.get('end_date')

    if not (year is None or (int(year) > 999 and int(year) < 10000)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong year parameter"}
        return False

    if not (month is None or (int(month) > 0 and int(month) < 13)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong month parameter"}
        return False

    if not (day is None or (int(day) > 0 and int(day) < 32)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong day parameter"}
        return False

    if not (week is None or (int(week) > 0 and int(week) < 54)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong week parameter"}
        return False

    if not (hour is None or (int(hour) > -1 and int(hour) < 24)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong hour parameter"}
        return False

    if not (minute is None or (int(minute) > -1 and int(minute) < 60)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong minute parameter"}
        return False

    if not (second is None or (int(second) > -1 and int(second) < 60)):
        wrong_cron_response(response)
        response.body = {"error": "Wrong second parameter"}
        return False

    return True


def wrong_cron_response(response):
    logging.error("Wrong cron")
    response.status = "400 Invalid time parameters"
    return response
