from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# --- Hugging Face API Configuration (Using google/flan-t5-small - Smallest and fastest) ---
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"  # ⚠️ UPDATED to google/flan-t5-small - Smallest model for faster loading
API_TOKEN = "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" # YOUR API TOKEN - REMEMBER TO KEEP IT SECRET and use secure methods in production
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}", # Use f-string for token injection
    "Content-Type": "application/json"
}
MAX_CONTEXT_LINES = 100  # Define a constant for max history lines

# --- Helper Functions ---
def load_chat_history(filename, max_lines=MAX_CONTEXT_LINES):
    """Reads the last 'max_lines' from a TXT file and returns the content as a string."""
    if filename == "baldo_chat.txt": # Condition to use the test file for Baldo
        filename = "baldo_chat_test.txt" #  Use the empty test file for Baldo for now
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            last_lines = lines[-max_lines:]
            return "".join(last_lines)
    except FileNotFoundError:
        return ""

def query_huggingface(user_input, chatbot, max_new_tokens=100, temperature=0.7):
    """Sends user input to Hugging Face API with persona-specific history and parameters."""
    chat_history = load_chat_history(f"{chatbot.lower()}_chat.txt")
    prompt = f"Previous conversation:\n{chat_history}\nUser: {user_input}\n{chatbot}:"

    print(f"--- PROMPT SENT TO MODEL ({chatbot}): ---\n{prompt}\n--- END PROMPT ---")

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": temperature, "max_new_tokens": max_new_tokens}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        output = response.json()
        print(f"--- RAW MODEL RESPONSE ({chatbot}): ---\n{output}\n--- END RAW RESPONSE ---") # ADDED: Print raw JSON response
        if isinstance(output, list) and output: # CHECK: Ensure output is a list and not empty
            first_item = output[0] # Get the first item from the list
            if isinstance(first_item, dict) and "generated_text" in first_item: # CHECK: Ensure first item is a dict and has 'generated_text'
                generated_text = first_item["generated_text"] # Now access 'generated_text' safely
                print(f"--- MODEL RESPONSE ({chatbot}): ---\n{generated_text}\n--- END RESPONSE ---")
                return generated_text
            else:
                error_message = "Unexpected response format: 'generated_text' not found in the first item of the output list."
                print(f"--- MODEL RESPONSE ERROR ({chatbot}): ---\n{error_message}\n--- END RESPONSE ERROR ---")
                return error_message
        else:
            error_message = "Unexpected response format: Output is not a non-empty list."
            print(f"--- MODEL RESPONSE ERROR ({chatbot}): ---\n{error_message}\n--- END RESPONSE ERROR ---")
            return error_message

    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Flask Routes ---
@app.route("/")
def index():
    """Renders the chatbot interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat requests from the frontend."""
    data = request.json
    if not data or "user_input" not in data or "chatbot" not in data:
        return jsonify({"response": "Error: Input must include 'user_input' and 'chatbot'."}), 400 # Return 400 for bad request

    user_input = data["user_input"]
    chatbot = data["chatbot"]

    try: # Use try-except for error handling in API call
        response = query_huggingface(user_input, chatbot)
        return jsonify({"response": response})
    except requests.exceptions.RequestException as e: # Catch network errors
        return jsonify({"response": f"Error: Could not connect to model API. {e}"}), 500 # Return 500 for server error

# --- Main App Execution ---
if __name__ == "__main__": # CORRECTED LINE - using __name__
    app.run(debug=True, port=5002)