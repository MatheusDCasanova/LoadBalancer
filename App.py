import simpy
import random
from Server import Server
from LoadBalancer import LoadBalancer
from Request import Request


def generate_requests(env, load_balancer):
    request_id = 0
    while True:
        yield env.timeout(3)  # Time between requests
        request_id += 1
        load_balancer.route_request(Request(request_id=request_id))


def main():
    env = simpy.Environment()
    servers = [Server(env, i) for i in range(3)]
    load_balancer = LoadBalancer(
        env, servers, policy="shortest_queue")  # Change policy here

    env.process(generate_requests(env, load_balancer))
    env.run(until=100)  # Run simulation for 100 units of time

    for server in servers:
        print(f"Server {server.server_id} - Processed: {server.processed_requests}, "
              f"Average Request Time: {server.average_request_time():.2f}")


if __name__ == "__main__":
    main()
