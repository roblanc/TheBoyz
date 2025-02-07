import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS

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


# Netlify function handler (needed for deployment on Netlify Functions)
def handler(event, context):
    with app.test_request_context(event['path'], method=event['httpMethod'], query_string=event['queryStringParameters'], json=event.get('body')):
        try:
            # Dispatch the request to Flask and get the response
            response = app.full_dispatch_request()
        except Exception as e:
            # Handle exceptions if any
            return {
                'statusCode': 500,
                'body': str(e)
            }
        # Convert Flask response to Netlify function response format
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.data.decode('utf-8') # or response.get_data(as_text=True)
        }


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)