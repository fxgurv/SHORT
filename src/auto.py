from flask import Flask, request, jsonify
from classes.YouTube import YouTube

app = Flask(__name__)

@app.route('/api/account', methods=['POST'])
def create_account():
    data = request.json
    # Initialize YouTube class with data
    return jsonify({"status": "success"})

@app.route('/api/generate', methods=['POST'])
def generate_video():
    data = request.json
    # Call video generation method
    return jsonify({"status": "processing"})

if __name__ == '__main__':
    app.run(debug=True)