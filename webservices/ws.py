import os
from flask import Flask, jsonify, send_from_directory # Updated import

# Tell Flask where to find the static files (optional, but good for clarity)
# The static_folder defaults to 'static'
app = Flask(__name__, static_folder='static') 

# Serve the index.html from the root path
@app.route('/')
def index():
    # Use send_from_directory to explicitly serve a file from the static folder
    # This correctly points to your 'static/index.html'
    return send_from_directory(app.static_folder, 'index.html')


# Simple API endpoint for the frontend to call
@app.route('/api/data')
def get_data():
    return jsonify({
        "message": "Hello from the Python Web Service (ws.py)!",
        "status": "success",
        "service_port": 5000
    })

if __name__ == '__main__':
    # Flask runs on port 5000 by default. 
    app.run(host='0.0.0.0', port=5000, debug=True)
