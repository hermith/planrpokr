import uuid


class User:
    def __init__(self, queue):
        self.queue = queue
        self.uuid = uuid.uuid4()
