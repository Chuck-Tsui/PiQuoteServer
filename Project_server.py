from flask import Flask, request, jsonify
import json
import socket
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Use a lock for thread-safe file access
lock = threading.Lock()
STATS_FILE = 'request_stats.txt'

# Initialize the stats file
def init_stats_file():
    with lock:
        try:
            with open(STATS_FILE, 'r') as file:
                pass
        except FileNotFoundError:
            with open(STATS_FILE, 'w') as file:
                json.dump({}, file)

def update_statistics(username):
    with lock:
        with open(STATS_FILE, 'r') as file:
            stats = json.load(file)
        stats[username] = stats.get(username, 0) + 1
        with open(STATS_FILE, 'w') as file:
            json.dump(stats, file)


# Function to validate user credentials
def validate_user(username, password):
    if not username or not password:
        return False
    if len(username) != 4 or not username.isdigit():
        return False
    if password != f"{username}-pw":
        return False
    return True


# Function to perform Monte Carlo simulation of π
def monte_carlo_pi_simulation(samples):
    inside_circle = 0
    for _ in range(samples):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1:
            inside_circle += 1
    return inside_circle / samples * 4

# Function to calculate π using Monte Carlo simulation
@app.route('/pi', methods=['POST'])
def calculate_pi():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    simulations = data.get('simulations')
    concurrency = data.get('concurrency', 1)
    
    # Validate user credentials
    if not validate_user(username, password):
        return jsonify({'error': 'user info error'}), 401
    
    # Validate number of simulations
    if simulations is None:
        return jsonify({'error': 'missing field simulations'}), 400
    if not isinstance(simulations, int) or not 100 <= simulations <= 100000000:
        return jsonify({'error': 'invalid field simulations'}), 400
    
    # Validate concurrency
    if not isinstance(concurrency, int) or not 1 <= concurrency <= 8:
        return jsonify({'error': 'invalid field concurrency'}), 400

    # Start the Monte Carlo simulation
    start_time = time.time()
    samples_per_thread = simulations // concurrency
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(monte_carlo_pi_simulation, samples_per_thread) for _ in range(concurrency)]
        pi_estimates = [future.result() for future in futures]
        avg_pi_estimate = sum(pi_estimates) / concurrency
    elapsed_time = time.time() - start_time

    # Update request statistics
    update_statistics(username)

    # Return the results
    return jsonify({
        'number_of_simulations': simulations,
        'level_of_concurrency': concurrency,
        'calculated_value_of_pi': avg_pi_estimate,
        'measured_time_for_processing_request': elapsed_time
    })


def get_quote(protocol, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM) as sock:
        if protocol == 'tcp':
            sock.connect((host, port))
            return sock.recv(1024).decode()
        else:  # UDP
            sock.sendto(b'', (host, port))
            return sock.recvfrom(1024)[0].decode()
        
@app.route('/quote', methods=['POST'])
def quote_service():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    protocol = data.get('protocol')
    concurrency = data.get('concurrency', 1)
    
    # Validate user credentials (reusing the validation function from previous requirements)
    if not validate_user(username, password):
        return jsonify({'error': 'user info error'}), 401
    
    # Validate protocol
    if protocol not in ['tcp', 'udp'] and protocol is not None:
        return jsonify({'error': 'invalid field protocol'}), 400
    if protocol is None:
        return jsonify({'error': 'missing field protocol'}), 400
    
    # Validate concurrency
    if not isinstance(concurrency, int) or not 1 <= concurrency <= 8:
        return jsonify({'error': 'invalid field concurrency'}), 400

    # Fetch quotes using the requested protocol and concurrency level
    quotes = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_quotes = [executor.submit(get_quote, protocol, 'localhost', 1700) for _ in range(concurrency)]
        quotes = [future.result() for future in future_quotes]
    elapsed_time = time.time() - start_time

    return jsonify({
        'protocol': protocol,
        'concurrency': concurrency,
        'quotes': quotes,
        'processing_time': elapsed_time
    })
# Initialize the stats file
init_stats_file()

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
