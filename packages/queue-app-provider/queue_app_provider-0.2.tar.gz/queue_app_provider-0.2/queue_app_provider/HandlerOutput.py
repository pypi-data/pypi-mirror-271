import logging

import requests

logger = logging.getLogger('HandlerOutput')


# This class is a holder for all information regarding the processing
# of a handler, a handler is the function accountable of working on
# a image or binary data to create proper output.
#
# It's just a wrapper of a `success` a `text` or a `file` if the
# output of processor is a file.
#
# This information is used within the `notify` method (which receives a
# callback function) to report source of the translation of the
# issue.
#
# Created by: David Rodríguez Alfayate
# Version: 1.0
class HandlerOutput:
    def __init__(self, success: bool, text: str, file=""):
        self.success = success
        self.file = file
        self.text = text

    # As stated above the notify method receives the callback url, and according to its
    # object internal state it sends the proper response to the origin.
    def notify(self, callback: str):
        try:
            # On fail
            if not self.success:
                logger.debug('Sending fail message %s to % endpoint', self.text, callback)
                requests.post(callback, json={"success": False, "error": self.text})
                return
            # On success, but a file
            if self.file:
                logger.debug('Sending success file to % endpoint', callback)
                requests.post(callback, json={"success": True}, files={'file': open(self.file, 'rb')})
                return
            # Normal text
            requests.post(callback, json={"success": True, "data": self.text})
        except requests.exceptions.RequestException as e:
            # In a more complex scenario we should, perhaps, enqueue this callback response, expecting
            # than in the near future the remote server could be up again. For this simple example,
            # we are just ignoring the request, logging the error event
            logger.exception(e, exc_info=True)
            return
