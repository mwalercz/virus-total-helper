# @author: Marek B
# pojdeyncze zapytanie do VT

import hashlib
import logging

from server.fileservice import Fileservice


def single_handler(request, response):
    if request.is_content_app_json() and request.is_json():
        sha256 = _get_validated_sha256(request.json())
    else:
        binary = request.binary()
        sha = hashlib.sha256(binary)
        sha256 = sha.hexdigest()

    # sprawdzamy czy plik istnieje
    create_processing_file(sha256)
    request.deque.append(sha256)

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }
    return response


def create_processing_file(sha256):
    with Fileservice.File(sha256) as file:
        if not file.exists():
            file.write("PROCESSING")
            logging.info("File " + sha256 + ".html created.")


def _get_validated_sha256(params):
    if len(params) == 1 and "sha256" in params:
        return params["sha256"]
