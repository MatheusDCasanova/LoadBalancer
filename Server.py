import random
from collections import deque


class Server:
    def __init__(self, env, server_id):
        self.env = env
        self.server_id = server_id
        self.queue = deque()
        self.processed_requests = 0
        self.total_wait_time = 0

    def process_request(self, request):
        start_time = self.env.now
        yield self.env.timeout(random.expovariate(1.0))  # Simulate processing time
        self.processed_requests += 1
        self.total_wait_time += self.env.now - start_time

    def average_request_time(self):
        if self.processed_requests == 0:
            return 0
        return self.total_wait_time / self.processed_requests