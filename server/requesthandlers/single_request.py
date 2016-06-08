# @author: Marek B
# pojdeyncze zapytanie do VT

import hashlib
import logging

from server.requesthandlers import vt_request
from server.fileservice import Fileservice
from server.queue import Queuerequest

def single_handler(request, response, scheduler):

    if request.is_json():
        sha256 = _get_validated_sha256(request.json())
    else:
        binary = request.binary()
        sha = hashlib.sha256(binary)
        sha256 = sha.hexdigest()

    #sprawdzamy czy plik istnieje
    create_processing_file(sha256)

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }
    # pojedyncze zapytanie do VT
    #scheduler.add_job(lambda: vt_request.request_to_vt(sha256), misfire_grace_time=60, max_instances=250)
    Queuerequest.push(sha256)
    return response

def create_processing_file(sha256):
    with Fileservice.File(sha256) as file:
        if not file.exists():
            file.write("PROCESSING")
            logging.info("File " + sha256 + ".html created.")

def _get_validated_sha256(params):
    if len(params) == 1 and "sha256" in params:
        return params["sha256"]