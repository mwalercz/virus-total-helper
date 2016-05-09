# @author: Marek
# cykliczne zapytanie do VT

#TODO: czy dodatnie nowego zadania z poprzednim SHA256, nadpisze corna czy tylko doda nowe zadanie?

import logging
import hashlib
from server.customhttp import WrongHeader
from server.requesthandlers import vt_request
from server.fileservice import read_from_file, write_to_file ,NoSuchFile

def cycle_handler(request, response, scheduler):
    # obliczamy sha256 dla pliku binarnego
    headers = request.headers
    data = request.json()
    sha256 = data.get('sha256')
    cron = data.get('cron')

    #TODO: sprawdzic, czy conr ma odpowiedni format
    #TODO: sprawdzic czy mamy juz takie SHA w bazie
    #TODO: sprawdzic czy istnieje plik o zadanym SHA i jesli nie to stworzyc go z zawartoscia "Processing..."

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": ""
    }

    # pojedyncze zapytanie do VT
    #scheduler.add_job(lambda: vt_request.request_to_vt(sha256))

    return response