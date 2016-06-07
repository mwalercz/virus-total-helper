#!/usr/bin/python3.4
import requests
import json
import time

# żeby zadziałało najpierw należy uruchomić serwer na porcie 5005
def test_plenty_sha256(filename):
    sha256_list = get_sha256_list(filename)
    for sha256 in sha256_list:
        time.sleep(1)
        payload = {'sha256': sha256}
        response = requests.post('http://localhost:5005/api/singleVirusTotal',
                                 data=json.dumps(payload))

    for sha256 in sha256_list:
        payload = {'sha256': sha256}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        write_to_file(sha256, str(response.json()))

def write_to_file(sha256, text):
    with open("results/" + sha256 + ".json", 'w+') as file:
        file.write(text)

def get_sha256_list(filename):
    sha256_list = []
    with open(filename) as file:
        for line in file:
            splitted_tab = line.split(" ")
            sha256 = splitted_tab[0]
            sha256_list.append(sha256)
    return sha256_list

test_plenty_sha256("crypto.txt")
test_plenty_sha256("locky.txt")
