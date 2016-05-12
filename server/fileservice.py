import os

import server
from server import config
from threading import Lock


### Ex:
# with Fileserver.File(sha256) as file:
#     string = file.read()
#     file.write(string)
# W powyższym przykładzie wszystko w bloku with jest wykonywane atomowo,
# tzn. uzyskanie obiektu file powoduje zajęcie go
# Po wyjściu z zasięgu with plik jest odblokowywany

class Fileservice:
    _locks_lock = Lock()
    _locks = {}

    class File:
        def __init__(self, sha265):
            self.sha256 = sha265

        def __enter__(self):
            Fileservice._lock(self.sha256)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            Fileservice._unlock(self.sha256)

        def read(self):
            return Fileservice._read(self.sha256)

        def write(self, data):
            return Fileservice._write(self.sha256, data)

        def exists(self):
            return Fileservice._exists(self.sha256)

        def remove(self):
            return Fileservice._remove(self.sha256)

    @staticmethod
    def _exists(sha256):
        return os.path.isfile(Fileservice._get_filename(sha256))

    @staticmethod
    def _read(sha256):
        if not Fileservice._exists(sha256):
            raise NoSuchFile
        file = open(Fileservice._get_filename(sha256), 'r')
        temp = file.read()
        file.close()
        return temp

    @staticmethod
    def _write(sha256, data):
        file = open(Fileservice._get_filename(sha256), 'w')
        file.write(data)
        file.close()

    @staticmethod
    def _get_filename(sha265):
        return config.html_dir + str(sha265) + '.html'

    @staticmethod
    def _lock(sha256):
        if not sha256 in Fileservice._locks:
            Fileservice._locks_lock.acquire()
            if not sha256 in Fileservice._locks:
                Fileservice._locks[sha256] = Lock()
            Fileservice._locks_lock.release()
        Fileservice._locks[sha256].acquire()

    @staticmethod
    def _unlock(sha256):
        Fileservice._locks[sha256].release()

    @staticmethod
    def _remove(sha256):
        os.remove(Fileservice._get_filename(sha256))


class NoSuchFile(Exception):
    pass


#### Jak to mówią: deprecated, do not use
def read_from_file(sha256):
    raise NotImplementedError


# sha256 as string, data as string
def write_to_file(sha256, data):
    raise NotImplementedError
