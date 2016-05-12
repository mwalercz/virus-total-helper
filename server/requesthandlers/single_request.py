# @author: Marek B
# pojdeyncze zapytanie do VT

import hashlib
import logging

from server.requesthandlers import vt_request
from server.fileservice import Fileservice


def single_handler(request, response, scheduler):

    binary = request.binary()

    # obliczamy sha256 dla pliku binarnego
    sha = hashlib.sha256(binary)
    sha256 = sha.hexdigest()

    #sprawdzamy czy plik istnieje
    create_processingg_file(sha256)

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }
    # pojedyncze zapytanie do VT
    scheduler.add_job(lambda: vt_request.request_to_vt(sha256))
    return response

def create_processingg_file(sha256):
    with Fileservice.File(sha256) as file:
        if not file.exists():
            file.write("PROCESSING")
            logging.info("File " + sha256 + ".html created.")