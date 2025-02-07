import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS   # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes and origins


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json['message']
    chatbot_type = request.json['chatbot_type']

    if chatbot_type == 'beldo':
        response_text = "Beldo says: Nu stiu ce sa zic."
    elif chatbot_type == 'unde':
        response_text = "Unde says: ...unde?"
    elif chatbot_type == 'marius':
        response_text = "Marius says: Sa moaraিলি!"
    else:
        response_text = "Chatbot type not recognized."

    return jsonify({"response": response_text})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))  # Changed from 5000 to 5001
    app.run(host='0.0.0.0', port=port, debug=True)