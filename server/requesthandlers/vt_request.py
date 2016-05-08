import requests
from server.fileservice import write_to_file

def request_to_VT(sha256):
    url = 'https://www.virustotal.com/en/file/' + (sha256) + '/analysis/'
    responseVT = requests.get(url)
    data = responseVT.json()
    write_to_file(sha256, data)
