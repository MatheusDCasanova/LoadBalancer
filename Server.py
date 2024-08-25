import random
from collections import deque
from Request import Request


class Server:
    def __init__(self, env, server_id):
        self.env = env
        self.server_id = server_id
        self.queue = deque()
        self.processed_requests = 0
        self.total_wait_time = 0
        self.env.process(self.run())  # Start the server process

    def run(self):
        while True:
            if self.queue:
                request = self.queue.popleft()  # Get the next request
                # Process the request
                yield self.env.process(self.process_request(request))
            else:
                yield self.env.timeout(0.1)
                # Wait until there is a new request in the queue

    def process_request(self, request: Request):
        print(
            f'Processing Request {request.request_id} in server {self.server_id}')
        start_time = self.env.now
        # Simulate processing time
        yield self.env.timeout(request.CPU_time)
        self.processed_requests += 1
        wait_time = self.env.now - start_time
        self.total_wait_time += wait_time
        print(f'\t wait time: {wait_time}')

    def average_request_time(self):
        if self.processed_requests == 0:
            return 0
        return self.total_wait_time / self.processed_requests
