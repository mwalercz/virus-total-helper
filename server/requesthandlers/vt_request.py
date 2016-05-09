import requests
from server.fileservice import write_to_file

def request_to_vt(sha256):
    url = 'https://www.virustotal.com/en/file/' + (sha256) + '/analysis/'
    responseVT = requests.get(url)
    data = responseVT.content
    empty_file = b''

    if(data == empty_file):
        #TODO: sprawdzic czy nie nadpisujemy istniejacego pliku (Ale czy to ma sens?)
        write_to_file(sha256, "404 Not Found")
    else:
        write_to_file(sha256, data)