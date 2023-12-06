from flask import Flask, request, jsonify
import threading
import json

app = Flask(__name__)

# Use a lock for thread-safe file access
lock = threading.Lock()
STATS_FILE = 'request_stats.txt'

def init_stats_file():
    with lock:
        try:
            # Open the file in read mode to check if it exists
            with open(STATS_FILE, 'r') as file:
                pass
        except FileNotFoundError:
            # If the file does not exist, create it and initialize an empty dictionary
            with open(STATS_FILE, 'w') as file:
                json.dump({}, file)

def update_statistics(username):
    with lock:
        # Read the current statistics from the file
        with open(STATS_FILE, 'r') as file:
            stats = json.load(file)
        
        # Update the statistics
        if username in stats:
            stats[username] += 1
        else:
            stats[username] = 1
        
        # Write the updated statistics back to the file
        with open(STATS_FILE, 'w') as file:
            json.dump(stats, file)

@app.route('/pi', methods=['POST'])
@app.route('/quote', methods=['POST'])
def handle_request():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'user info error'}), 401

    if len(username) != 4 or not username.isdigit():
        return jsonify({'error': 'user info error'}), 401 

    if password != f"{username}-pw":
        return jsonify({'error': 'user info error'}), 401

    # Update request statistics
    update_statistics(username)

    # Further implementation pending
    return jsonify({'message': 'User is authenticated, further implementation pending.'})

if __name__ == '__main__':
    init_stats_file()  # Initialize the stats file
    app.run(host='0.0.0.0', port=5000)
