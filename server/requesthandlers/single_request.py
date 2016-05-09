# @author: Marek
# pojdeyncze zapytanie do VT

import logging
import hashlib
from server.customhttp import WrongHeader
from server.requesthandlers import vt_request
from server.fileservice import read_from_file, write_to_file ,NoSuchFile

def single_handler(request, response, scheduler):
    # obliczamy sha256 dla pliku binarnego
    try:
        binary = request.binary()
    except WrongHeader:
        logging.error("Wrong Header! Expected: octet-stream")
        response.status = "415 Unsupported Media Type"
        response.body = {
            "error": "Please use content_type: application/octet-stream"
        }
        return response


    sha = hashlib.sha256(binary)
    sha256 = sha.hexdigest()

    #TODO: sprawdzic czy istnieje plik o zadanym SHA i jesli nie to stworzyc go z zawartoscia "Processing..."

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }

    # pojedyncze zapytanie do VT
    scheduler.add_job(lambda: vt_request.request_to_vt(sha256))

    return response