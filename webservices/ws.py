import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Serve the index.html from the root path
@app.route('/')
def index():
    # Looks for index.html in the 'templates' folder, 
    # but since it's in the root, we can just render it if we configure Flask.
    # For a simple setup, we'll place index.html in the project root 
    # and return it directly. 
    # A more idiomatic Flask app would put it in a 'templates' folder.

    # Option 1: Serve a static file directly from the root for simplicity in this dev setup
    return app.send_static_file('index.html')


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
    # Setting host to '0.0.0.0' makes it accessible inside the container
    # so Codespaces can forward it.
    app.run(host='0.0.0.0', port=5000, debug=True)
