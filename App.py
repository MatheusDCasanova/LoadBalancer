import simpy
import random
import numpy as np
from Server import Server
from LoadBalancer import LoadBalancer
import matplotlib.pyplot as plt
from Request import Request

POLICY = "shortest_queue"
DURATION = 150000
NUM_REQUESTS = 10000


def generate_requests(env, load_balancer, request_timeout_intervals):
    """Generates requests based on an array of time intervals."""
    request_id = 0
    print('Starting request generation...')
    for request_timeout in request_timeout_intervals:
        yield env.timeout(request_timeout)  # Wait for the next time interval
        request_id += 1
        load_balancer.route_request(Request(request_id=request_id))
    print(f"Finished generating {len(request_timeout_intervals)} requests.")


def create_gaussian_request_times(duration):

    # Parameters for the Gaussian function
    mu = DURATION / 2     # Mean
    sigma = DURATION/20   # Standard deviation
    size = NUM_REQUESTS

    # Generate the x values
    x = np.linspace(0, DURATION, size)

    # Gaussian function
    gaussian = (1/(sigma * np.sqrt(2 * np.pi))) * \
        np.exp(-0.5 * ((x - mu)/sigma)**2)

    # Normalize the values to fit between 1 and 10
    gaussian_normalized = 1 + (gaussian - gaussian.min()) * \
        (10 - 1) / (gaussian.max() - gaussian.min())

    return gaussian_normalized


def plot_intervals(inverted_intervals):
    """Plot the generated time intervals."""
    # Generate the x values
    x = np.linspace(0, DURATION, NUM_REQUESTS)
    # Plot the normalized Gaussian function
    plt.plot(x, inverted_intervals)
    plt.xlabel("Time")
    plt.ylabel("Time between requests")
    plt.title("Request Generation Pattern (Low -> Peak -> Low)")
    # plt.legend()
    plt.grid(True)
    plt.show()


def main():
    env = simpy.Environment()
    servers = [Server(env, i) for i in range(3)]
    load_balancer = LoadBalancer(env, servers, policy=POLICY)

    request_timeout_intervals = 10 / \
        create_gaussian_request_times(duration=DURATION)

    plot_intervals(request_timeout_intervals)

    env.process(generate_requests(
        env, load_balancer, request_timeout_intervals))
    env.run(until=DURATION*2)

    for server in servers:
        print(f"Server {server.server_id} - Processed: {server.processed_requests}, "
              f"Average Request Time: {server.average_request_time():.2f}")


if __name__ == "__main__":
    main()


# TODO pegar o tempo total de processamento - usar env now
# - tempo constante timeout entre requests
# - graficos do tamanho da fila de cada server no tempo
# - atualizar requirements.txt
# - O estado do servidor (ocupado, inativo) e o comprimento da fila devem ser monitorados.
