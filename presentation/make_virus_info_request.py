#!/usr/bin/python3
import json
import requests


def make_virus_info_request(filename):
    sha256_list = get_sha256_list(filename)
    for sha256 in sha256_list:
        payload = {'sha256': sha256}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        returned_json = json.dumps(response.json(), indent=4, sort_keys=True)
        if response.status_code != 200:
            print("status: " + str(response.status_code) +
                  "\n sha256: " + sha256 + "\n" + returned_json )
        write_to_file(sha256, returned_json)


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


if __name__ == "__main__":
    make_virus_info_request("crypto.txt")
    make_virus_info_request("locky.txt")
