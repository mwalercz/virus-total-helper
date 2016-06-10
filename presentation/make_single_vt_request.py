#!/usr/bin/python3
import requests
import json


# żeby zadziałało najpierw należy uruchomić serwer na porcie 5005
def make_single_vt_request(filename):
    sha256_list = get_sha256_list(filename)
    headers = {"Content-Type": "application/json"}
    for sha256 in sha256_list:
        payload = {'sha256': sha256}
        response = requests.post('http://localhost:5005/api/singleVirusTotal',
                                 data=json.dumps(payload),
                                 headers=headers)
        returned_json = json.dumps(response.json(), indent=4, sort_keys=True)
        print("status:" + str(response.status_code) + "\n" + returned_json)


def get_sha256_list(filename):
    sha256_list = []
    with open(filename) as file:
        for line in file:
            splitted_tab = line.split(" ")
            sha256 = splitted_tab[0]
            sha256_list.append(sha256)
    return sha256_list


if __name__ == "__main__":
    make_single_vt_request("crypto.txt")
    make_single_vt_request("locky.txt")
