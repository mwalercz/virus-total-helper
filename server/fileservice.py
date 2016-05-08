# sha256 as string, returns string
# raises exception NoSuchFile if it doesn't find file on filesystem
import os

import server
from server import config
from threading import Lock


class Fileserver:
    _locks_lock = Lock()
    _locks = {}

    @staticmethod
    def read(sha256):
        Fileserver._lock(sha256)
        if not os.path.isfile(Fileserver._get_filename(sha256)):
            raise NoSuchFile
        file = open(Fileserver._get_filename(sha256), 'r')
        temp = file.read(), sha256
        file.close()
        Fileserver._unlock(sha256)
        return temp

    @staticmethod
    def write(sha256, data):
        Fileserver._lock(sha256)
        file = open(Fileserver._get_filename(sha256), 'w')
        file.write(data)
        file.close()
        Fileserver._unlock(sha256)

    @staticmethod
    def _get_filename(sha265):
        return config.html_dir + str(sha265) + '.html'

    @staticmethod
    def _lock(sha256):
        if not sha256 in Fileserver._locks:
            Fileserver._locks_lock.acquire()
            if not sha256 in Fileserver._locks:
                Fileserver._locks[sha256] = Lock()
            Fileserver._locks_lock.release()
        Fileserver._locks[sha256].acquire()

    @staticmethod
    def _unlock(sha256):
        Fileserver._locks[sha256].release()


def read_from_file(sha256):
    try:
        return Fileserver.read(sha256)
    except NoSuchFile:
        raise


# sha256 as string, data as string
def write_to_file(sha256, data):
    return Fileserver.write(sha256, data)


class NoSuchFile(Exception):
    pass
