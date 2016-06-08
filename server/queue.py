import queue
import logging

class Queuerequest:

    queue_request = queue.Queue()

    @staticmethod
    def push(sha256):
        global queue_request
        try:
            queue_request.put(sha256)
        except queue.Full:
            logging.info("Queue of request is full.")
            raise queue.Full

    @staticmethod
    def pop():
        global queue_request
        try:
            sha256 = queue_request.get()
        except queue.Empty:
            logging.info("Queue of request is empty.")
            raise queue.Empty
        return sha256