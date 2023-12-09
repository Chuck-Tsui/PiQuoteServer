README for s12556828final
Author: Xu Xiaochi
Student Number: 1255682

File Description
Project_server.py: 
This script forms the backbone of our Flask-based web application. It features two services - one for estimating Pi using Monte Carlo simulations and another for providing random quotes via TCP/UDP. Key functions include user authentication, input validation for simulation counts and concurrency, and maintaining a thread-safe log of user requests.
quote_server.py: 
This application operates as a quote delivery service over TCP and UDP. It prepares a collection of quotes, listening for requests on designated ports. To reflect real-life scenarios, a brief delay is introduced before dispatching a randomly chosen quote. This server is designed for concurrent client management and allows for flexible host and port configuration.
test.py:
This script encompasses a suite of unit tests for the project's server. It methodically assesses various aspects such as user authentication, the correctness of Pi calculation parameters, concurrency management, and the functionality of the quote service over different protocols. 
Setup and Execution Instructions
Prerequisites
Ensure you have Python 3.11.x installed on your system. You can verify the installation by running ‘python  --version’ in your command-line interface.
Project Server Setup:
1. Required Libraries: 
•	Flask 3.0.0
•	Requests
2. Installation of Required Libraries:
•	Flask:
>>pip install Flask
•	Requests:
>>pip install requests
3. Data Files Initialization:
The ‘request_stats.txt’ file is used to track request statistics for the web services. 
Initialization:
•	File Check and Creation: On the first launch of the Flask application, the init_stats_file() function checks for the existence of the request_stats.txt file.
•	Auto-generation: In cases where request_stats.txt is not found, the function generates it, embedding an empty JSON object {}. This setup prepares the file for subsequent data recording activities.
File Location:
•	‘request_stats.txt’ resides in the same directory as the Flask application, ensuring straightforward access.
No manual steps are required for the initialization of request_stats.txt; the process is fully managed by the application's logic.
4. Execution:
To start the project server and quote server, run the following command:
>>python Project_server.py
>>python quote_server.py
Test Setup:
Running Tests:
•	Ensure the project server and quote server is running.
•	Execute the test script using:
>>python test.py
JSON Request and Response Formats
Pi Calculation Service
Request Format:
Field	Type	Description	Example
username	String	A string of 4-digit user identifier	"0123"
password	String	A string containing the user name followed by ”-pw”	"0123-pw"
simulations	Integer	Number of Monte Carlo simulations to run for calculating Pi	1000
concurrency	Integer	Level of concurrency for the request processing	4
Note: The ‘simulations’ field specifies the number of random points to generate for the Monte Carlo Pi estimation. The ‘concurrency’ field determines the number of parallel processes or threads to use for the calculation.
Response Format:
Field	Type	Description
calculated_value_of_pi	Float	The calculated approximate value of Pi
number_of_simulations	Integer	The number of simulations used for calculation
level_of_concurrency	Integer	The concurrency level used for processing
measured_time_for_processing_request	Float	The time taken to process the request in seconds
Note: The response includes the result of the Pi calculation as well as metadata about the request processing.
Quote Service
Request Format:
Field	Type	Description	Example
username	String	A string of 4-digit user identifier	"0123"
password	String	A string containing the user name followed by ”-pw”	"0123-pw"
protocol	String	The protocol to be used: "tcp" or "udp"	"tcp"
concurrency	Integer	Level of concurrency for the request processing	2
Note: The protocol field specifies the network protocol to use when fetching quotes. The concurrency field determines the number of parallel requests to make to the quote server.
Response Format:
Field	Type	Description
quotes	Array	An array of quotes received from the server
protocol	String	The protocol used for the request
concurrency	Integer	The concurrency level used for processing
processing_time	Float	The time taken to process the request in seconds
Note: The response includes an array of requested quotes along with request processing metadata.
Concurrency Solutions Description and Justification
The project server leverages Python's ‘concurrent.futures.ThreadPoolExecutor’ to implement concurrency for both the Pi calculation and quote retrieval services. This approach is chosen for its simplicity and the fact that it is well-suited to I/O-bound and high-level structured network code.
Pi Calculation Service (‘/pi’)
The Pi calculation service handles concurrent processing of Monte Carlo simulations to estimate the value of Pi. When a client requests Pi calculation, the total number of simulations is divided by the level of concurrency to distribute the workload evenly across multiple threads.
Justification:
The ‘ThreadPoolExecutor’ is utilized here to parallelize CPU-bound operations, specifically the Monte Carlo simulations. By splitting the task into smaller sub-tasks run in parallel, the service can utilize multiple CPU cores, thus reducing the total processing time and improving throughput.
Quote Retrieval Service (‘/quote’)
The quote service, on the other hand, uses concurrency for handling multiple network requests to retrieve quotes. Depending on the client's request, a number of worker threads equal to the specified concurrency level are spawned to fetch quotes concurrently.
Justification:
Given that the quote service is I/O-bound, primarily waiting for network responses, threading is an effective means to allow other operations to continue while a part of the program is waiting on a response. This ensures the service can handle multiple requests efficiently without one blocking the other.
Concurrency Level Handling
Both services validate the ‘concurrency’ parameter to ensure it is within the allowed range (1 to 8). This validation prevents spawning too many threads, which can cause excessive context switching and can potentially degrade performance or lead to resource exhaustion.
Overall Benefit:
Implementing concurrency through ‘ThreadPoolExecutor’ provides a balance between performance and resource utilization. It allows the server to respond to multiple service requests simultaneously, making effective use of server resources while maintaining simplicity in implementation.
Advanced Technologies Discussion
1.	Asynchronous Programming
Benefits: Asynchronous programming is particularly beneficial in I/O-bound operations, such as network requests or file I/O, which are prevalent in web services. By adopting asynchronous programming, our project server could handle a significantly larger number of concurrent operations. This non-blocking I/O model allows for better utilization of server resources, as threads are not idly waiting for I/O operations to complete.
Implementation: In Python, this could be achieved using the ‘asyncio’ library, transforming our web services into coroutines with the ‘async def’ syntax. For instance, the quote retrieval service could be modified to asynchronously wait for network responses, allowing a single thread to manage multiple network I/O operations effectively.
from flask import Flask, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

# Asynchronous function to get a quote
async def get_quote_async(protocol, host, port):
    if protocol == 'tcp':
        # TCP implementation (can be done using libraries like `aiosocket`)
        # ...
        pass
    elif protocol == 'udp':
        # UDP implementation (similarly with `aiosocket`)
        # ...
        pass

@app.route('/quote', methods=['POST'])
async def quote_service_async():
    data = await request.get_json()
    username = data.get('username')
    password = data.get('password')
    protocol = data.get('protocol')
    concurrency = data.get('concurrency', 1)

    # Validate user and other parameters
    # ...

    # Fetch quotes asynchronously
    async with aiohttp.ClientSession() as session:
        tasks = [get_quote_async(protocol, 'localhost', 1700) for _ in range(concurrency)]
        quotes = await asyncio.gather(*tasks)

    return jsonify({
        'protocol': protocol,
        'concurrency': concurrency,
        'quotes': quotes
    })
Improved Functionality: The server's throughput would increase, allowing it to serve more requests per second. Additionally, the server would be more responsive, as the event loop could handle other tasks while waiting for I/O operations to complete.
2.	High Performance Computing: Cython
Cython is a programming enhancement for Python, combining Python's ease with the speed of C/C++. It allows us to write Python code with optional C-style static typing.
Benefits of Using Cython:
1.	Faster Performance: Cython can speed up Python code, especially in repetitive tasks like loops and calculations. It does this by converting Python functions to faster C functions.
2.	Easy C/C++ Use: Cython makes it simpler to use C/C++ code in Python projects, great for when you need the speed or features of these languages.
3.	Static Typing: Cython supports fixed types for variables, unlike Python's flexible types. This helps the code run faster, as it avoids the extra work Python usually does to figure out what type each variable is.
4.	Python-like Code: Cython's code looks a lot like Python, making it easier for Python programmers to use.
5.	Better for Parallel Processing: Cython allows for parallel processing, a method used to run multiple calculations at the same time. This is especially useful for complex tasks that need a lot of computing power.
Implementation
We can use Cython to rewrite the Monte Carlo Pi calculation. This involves defining types for variables and compiling the code into a format that the Flask app can use just like any other Python module. By doing this, we significantly boost the task's efficiency, particularly suitable for calculations that require a lot of processing power.
def monte_carlo_pi_simulation_cython(int samples):
    cdef int i, inside_circle = 0
    cdef double x, y
    for i in range(samples):
        x = rand() / RAND_MAX
        y = rand() / RAND_MAX
        if x * x + y * y <= 1:
            inside_circle += 1
    return (4.0 * inside_circle) / samples

