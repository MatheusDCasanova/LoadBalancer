import random


class Request:
    def __init__(self, request_id):
        self.CPU_time = random.randint(5, 20)
        self.request_id = request_id
