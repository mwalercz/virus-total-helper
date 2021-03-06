# @author: Marek
# cykliczne zapytanie do VT

import logging

from server.customhttp import NotJsonError


def cycle_handler(request, response):
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

    # if not (try_add_job(sha256, cron, request.scheduler, response)):
    #     return response

    # try:
    #     request.scheduler.remove_job(job_id=sha256)
    # except Exception:
    #     pass

    request.scheduler.add_job(func=lambda: request.deque.append(sha256),
                              trigger='cron', id=sha256,
                              replace_existing=True, **cron)
    logging.info("Cron for " + sha256 + ".html has beed created/changed.")

    response.status = "202 Accepted"
    response.body = {"message": "Your schedule has been created"}
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


# def try_add_job(sha256, cron, scheduler, response):
#     try:
#         scheduler.add_job(func=lambda: vt_request.make_request_to_vt(sha256),
#                           trigger='cron', id='control_job',
#                           replace_existing=True, **cron)
#     except Exception as e:
#         logging.error("Scheduler reject job")
#         response.status = "406 Not Acceptable"
#         response.body = {
#             "error": "Wrong parameters. Check cron or sha256"
#         }
#         return False
#     return True
#
#
# def wrong_cron_response(response):
#     logging.error("Wrong cron")
#     response.status = "400 Invalid time parameters"
#     return response
