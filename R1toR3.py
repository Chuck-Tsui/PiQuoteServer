from flask import Flask, request, jsonify
import threading
import sqlite3
import json

app = Flask(__name__)

# Mutex for thread-safe operations
mutex = threading.Lock()

# Database setup for storing statistics
# Assuming a table 'statistics' with columns 'username' and 'request_count'
DATABASE = 'server.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS statistics
                     (username TEXT PRIMARY KEY, request_count INTEGER)''')
    print("Database initialized")

# Helper function to update statistics
def update_statistics(username):
    with mutex:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            # Check if user exists
            cur.execute('SELECT request_count FROM statistics WHERE username = ?', (username,))
            result = cur.fetchone()
            if result:
                # Update existing user's count
                cur.execute('UPDATE statistics SET request_count = request_count + 1 WHERE username = ?', (username,))
            else:
                # Insert new user with a count of 1
                cur.execute('INSERT INTO statistics (username, request_count) VALUES (?, 1)', (username,))
            conn.commit()

# Route for the pi service
@app.route('/quote', methods=['POST'])
@app.route('/pi', methods=['POST'])
def pi_service():
    # Parse and validate request JSON
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # Add more validation as per your requirements
    simulations = data.get('simulations')
    concurrency = data.get('concurrency', 1)  # Default to 1 if not provided

    # Update statistics
    update_statistics(username)

    # Perform Monte Carlo simulation to calculate pi
    # Implement the Monte Carlo simulation logic here
    calculated_pi = 3.14  # Placeholder for the actual calculated value

    response_data = {
        'username': username,
        'simulations': simulations,
        'concurrency': concurrency,
        'calculated_pi': calculated_pi,
        # Add more fields as required
    }
    return jsonify(response_data)
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

    # User info is valid, proceed to R3 and R4
    # This is a placeholder response 
    return jsonify({'message': 'User is authenticated, further implementation pending.'})

# Route for the quote service
# @app.route('/quote', methods=['POST'])
# def quote_service():
#     # Parse and validate request JSON
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')  # Add more validation as per your requirements
#     protocol = data.get('protocol')
#     concurrency = data.get('concurrency', 1)  # Default to 1 if not provided

#     # Update statistics
#     update_statistics(username)

#     # Retrieve quotes using the provided quote_server.py logic
#     # You need to implement the logic to interact with the quote server
#     quotes = ["Life is what happens when you're busy making other plans."]  # Placeholder for actual quotes

#     response_data = {
#         'username': username,
#         'protocol': protocol,
#         'concurrency': concurrency,
#         'quotes': quotes,
#         # Add more fields as required
#     }
#     return jsonify(response_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
