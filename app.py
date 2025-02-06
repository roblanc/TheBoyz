from flask import Flask, request, jsonify
from transformers import pipeline
import re

app = Flask(__name__)

# Load the chat data from the TXT file
def load_chat_data():
    with open("baldo_chat.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    messages = []
    for line in lines:
        # Extract messages from the chat
        match = re.match(r"(\d{2}:\d{2}) (.*?): (.*)", line)
        if match:
            timestamp, sender, text = match.groups()
            messages.append({"timestamp": timestamp, "sender": sender, "text": text})

    return messages

# Load the chat messages
chat_data = load_chat_data()

# Load the chatbot model from Hugging Face
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Append the user input to the chat data (if you want to simulate conversation)
    chat_data.append({"timestamp": "00:00", "sender": "User", "text": user_input})

    # Get the last few messages for context (to give some conversational history)
    context = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in chat_data[-5:]])

    # Generate a response from the chatbot
    response = chatbot(f"{context}\nFriend:", max_length=100, num_return_sequences=1)
    bot_reply = response[0]["generated_text"].split("Friend:")[-1].strip()

    # Append the bot's reply to the chat data
    chat_data.append({"timestamp": "00:00", "sender": "Friend", "text": bot_reply})

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)