from ursina import *
import datetime

class Logger(Entity):
    def __init__(self, messages_to_display, x_0, y_0, dy, write_to_log = True):
        super().__init__()
        self._message_queue = []
        self._messages_to_display = messages_to_display
        self._x0 = x_0 # -.85
        self._y0 = y_0 # .45
        self._dy = dy # -.05
        self._log_type = "LOG"
        self._write_to_log = write_to_log

    def _log_to_file(self, message):
        if not self._write_to_log:
            return
        with open(f'run.log', 'a') as f:
            f.write(f'{message}\n')


    def log(self, message):
        # if max log messages
        if len(self._message_queue) == self._messages_to_display:
            # remove first message
            to_remove = self._message_queue.pop(0)
            destroy(to_remove)
            # Add new message
        # update positions of each message
        for msg in self._message_queue:
            msg.y += self._dy
        # enqueue and show new message
        log_message = f'{self._log_type} [{datetime.datetime.now()}]: {message}'
        self._message_queue.append(Text(text=log_message, x=self._x0, y=self._y0))
        self._log_to_file(log_message)

