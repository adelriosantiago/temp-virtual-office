import time
import threading
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

LAST_SCENARIO = {
    "justStarted": True,
}

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# --- FLASK ROUTES ---

# Get status
@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify(LAST_SCENARIO)

# Update status
@app.route('/update_status', methods=['POST'])
def update_status():
    global LAST_SCENARIO

    wasUpdated = False
    try:
        # Merge incoming data with LAST_SCENARIO
        incoming_data = request.get_json()
        LAST_SCENARIO.update(incoming_data)

        wasUpdated = True
    except Exception as e:
        LAST_SCENARIO = {"error": str(e)}
        pass

    return jsonify({ "updated": wasUpdated, "status": LAST_SCENARIO })

# Serve public directory
@app.route('/<path:filename>')
def serve_public_file(filename):
    return send_from_directory('public', filename)


# @app.route('/', methods=['GET'])
# def index():
#     """Serve the index.html file."""
#     return send_from_directory('public', 'index.html')



if __name__ == "__main__":
    print("## Starting Flask Server on port 5000...")
    app.run(debug=True, port=5000, use_reloader=True)