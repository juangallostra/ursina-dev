from ursina import *

class Logger(Entity):
    def __init__(self, messages_to_display=5):
        super().__init__()
        self._message_queue = []
        self._messages_to_display = messages_to_display

    def log(self, message):
        # check log count
        if len(self.message_queue) = self._messages_to_display:
            # remove first message
            to_remove = self.message_queue.pop(0)
            destroy(to_remove)


