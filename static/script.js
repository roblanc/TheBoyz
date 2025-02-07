document.addEventListener('DOMContentLoaded', function() {
    const chatbotButtons = document.querySelectorAll('.chatbot-button');
    const chatArea = document.querySelector('.chat-area .history');
    const userInputField = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    let currentChatbot = 'beldo'; // Default chatbot

    // ... (rest of your Javascript code - chatbot selection, message display, etc.) ...


    sendButton.addEventListener('click', () => {
        const messageText = userInputField.value;
        if (messageText.trim() === '') return;

        addUserMessage(messageText);
        userInputField.value = '';

        // --- Modified fetch URL for Netlify Functions ---
        fetch('/.netlify/functions/handler/get_response', { // Call Netlify Function URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText, chatbot_type: currentChatbot })
        })
        .then(response => response.json())
        .then(data => {
            addBotMessage(data.response, currentChatbot);
        });
    });

    // ... (rest of your Javascript code - addUserMessage, addBotMessage, etc.) ...

});