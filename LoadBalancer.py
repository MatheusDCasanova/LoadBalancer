import random

class LoadBalancer:
    def __init__(self, env, servers, policy="round_robin"):
        self.env = env
        self.servers = servers
        self.policy = policy
        self.round_robin_index = 0

    def choose_server(self):
        if self.policy == "random":
            return random.choice(self.servers)
        elif self.policy == "round_robin":
            server = self.servers[self.round_robin_index]
            self.round_robin_index = (self.round_robin_index + 1) % len(self.servers)
            return server
        elif self.policy == "shortest_queue":
            return min(self.servers, key=lambda server: len(server.queue))
        else:
            raise ValueError("Unknown policy: {}".format(self.policy))

    def route_request(self, request):
        server = self.choose_server()
        server.queue.append(request)
        self.env.process(server.process_request(request))