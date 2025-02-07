from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face API Configuration
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # **Using gpt2 model**
API_TOKEN = "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"  # **Your Hugging Face API key is set!**
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_response(prompt):
    """Generate a response from the Hugging Face API."""
    print(f"Debug: generate_response called with prompt: '{prompt}'") # Debug print: Prompt

    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        api_response = response.json() # Parse JSON response

        if api_response and isinstance(api_response, list) and len(api_response) > 0 and 'generated_text' in api_response[0]:
            generated_text = api_response[0]['generated_text']
            print(f"Debug: generate_response - Model response: '{generated_text}'") # Debug print: Model response
            return generated_text
        else:
            error_message = "Error: Unexpected response format from Hugging Face API."
            print(f"Debug: API Response Error: {error_message}. API Response: {api_response}") # Debug print: API Response Error
            return error_message

    except requests.exceptions.RequestException as e: # Catch request exceptions (e.g., connection errors, timeouts)
        error_message = f"Error generating response from Hugging Face API: {e}"
        print(f"Debug: Request Error: {error_message}") # Debug print: Request Error
        return error_message
    except KeyError: # Catch KeyError if 'generated_text' is missing
        error_message = "Error: 'generated_text' key not found in Hugging Face API response."
        print(f"Debug: Key Error: {error_message}") # Debug print: Key Error
        return error_message


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    data = request.json
    user_message = data.get('message', '')
    chatbot_name = data.get('chatbot_name', 'Chatbot')  # Default to 'Chatbot' if not specified

    if not user_message:
        return jsonify({"response": "Error: No message provided."})

    # Minimal Prompts - Just user message (for gpt2)
    if chatbot_name == 'beldo':
        prompt = f"{user_message}"
    elif chatbot_name == 'unde':
        prompt =  f"{user_message}"
    elif chatbot_name == 'marius': # New: Marius persona
        prompt = f"{user_message}"
    else:
        prompt = f"{user_message}"

    response_text = generate_response(prompt)
    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True, port=5002)