#author: Marek
import requests
from server.fileservice import write_to_file

def request_to_vt(sha256):
    url = 'https://www.virustotal.com/en/file/' + (sha256) + '/analysis/'
    responseVT = requests.get(url)
    data = responseVT.content
    empty_file = b''

    if(data == empty_file):
        return
    else:
        write_to_file(sha256, data)