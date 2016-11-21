import threading

import requests
import urllib.parse

baseURL = "https://docs.google.com/forms/d/e/1FAIpQLSeWIBYU_Cv3Bbg3RMXyUdjE-aK3DW3yeEm443wl1JVnFGHb8A/formResponse?"
sessionIDField = "entry.109028851"
logField = "entry.284069394"
threadLock = threading.Lock()


def log(log, sessionID):
    encoded_session_id = urllib.parse.quote(sessionID)
    encoded_log = urllib.parse.quote(log)
    request = baseURL + sessionIDField + "=" + encoded_session_id + "&" + logField + "=" + encoded_log + "&submit=Submit"
    try:
        log_thread = logThread(request)
        log_thread.start()
    except RuntimeError:
        pass


def send_log(request):
    requests.get(request)


class logThread(threading.Thread):
    def __init__(self, request):
        self.request = request
        threading.Thread.__init__(self)

    def run(self):
        # Get lock to synchronize threads
        threadLock.acquire()
        send_log(self.request)
        # Free lock to release next thread
        threadLock.release()
