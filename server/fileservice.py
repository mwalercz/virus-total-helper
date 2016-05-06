# sha256 as int, returns string
# raises exception NoSuchFile if it doesn't find file on filesystem
def read_from_file(sha256):
    #raise NotImplemented
    temp = "read from file %d", sha256
    return temp


# sha256 as int, data as string
def write_to_file(sha256, data):
    raise NotImplemented


class NoSuchFile(Exception):
    def __init__(self, sha256):
        self.sha256 = sha256
