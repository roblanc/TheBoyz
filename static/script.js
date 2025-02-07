document.addEventListener('DOMContentLoaded', function() {
    const beldoBtn = document.getElementById('beldo-btn');
    const undeBtn = document.getElementById('unde-btn');
    const mariusBtn = document.getElementById('marius-btn'); // **New: Marius button**
    const chatArea = document.getElementById('chat-area');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const historyDiv = document.getElementById('history');
    let currentChatbot = 'beldo'; // Default chatbot is Beldo

    // Initial greetings for each chatbot
    const initialGreetings = {
        beldo: "I am Beldo zis si Mama Bebe... pe tine cum te numesti?",
        unde: "Nu sunt aryan, sunt pariah, nu paria. Vreau să plec în Spania, spirit de rastafarian. Tu ce te numesti?", // **Updated Unde greeting**
        marius: "Sa pronunt numele Jizzy Boy Lemuriano este activitatea care imi place! Tie ce-ti place sa numesti ca faci?" // **Updated Marius greeting**
    };

    // Function to add message to chat history
    function addMessage(message, sender, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender); // 'user' or 'bot'
        if (isBot) {
            messageDiv.classList.add('bot'); // Keep the general 'bot' class
            if (currentChatbot === 'marius') { /* New: Add 'marius' class if current chatbot is Marius */
                messageDiv.classList.add('marius');
            }
            messageDiv.innerHTML = `<div class='chatbot-name'>${currentChatbot.charAt(0).toUpperCase() + currentChatbot.slice(1)}:</div><div class='message-text'>${message}</div>`;
        } else {
            messageDiv.textContent = message;
        }
        historyDiv.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight; // Scroll to bottom
    }

    // Function to handle sending message
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        userInput.value = '';

        fetch('/chat', { // Changed route to '/chat'
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                chatbot_name: currentChatbot // Send chatbot_name in the request
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot', true); // Indicate it's a bot message
            } else {
                addMessage('Error: Could not get response.', 'bot', true);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Error communicating with chatbot.', 'bot', true);
        });
    }

    // Event listener for send button
    sendBtn.addEventListener('click', sendMessage);

    // Event listener for Enter key in input field
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Chatbot selector buttons
    beldoBtn.addEventListener('click', function() {
        currentChatbot = 'beldo';
        beldoBtn.classList.add('active');
        undeBtn.classList.remove('active');
        mariusBtn.classList.remove('active'); // **New: Deactivate Marius button**
        historyDiv.innerHTML = ''; // Clear chat history
        addMessage(initialGreetings.beldo, 'bot', true); // Add Beldo's greeting
    });

    undeBtn.addEventListener('click', function() {
        currentChatbot = 'unde';
        undeBtn.classList.add('active');
        beldoBtn.classList.remove('active');
        mariusBtn.classList.remove('active'); // **New: Deactivate Marius button**
        historyDiv.innerHTML = ''; // Clear chat history
        addMessage(initialGreetings.unde, 'bot', true); // Add Unde's greeting
    });

    mariusBtn.addEventListener('click', function() { // **New: Marius button click handler**
        currentChatbot = 'marius';
        mariusBtn.classList.add('active');
        beldoBtn.classList.remove('active');
        undeBtn.classList.remove('active'); // **Deactivate Unde button**
        historyDiv.innerHTML = ''; // Clear chat history
        addMessage(initialGreetings.marius, 'bot', true); // Add Marius's greeting
    });


    // Set Beldo as active chatbot and display initial greeting on page load
    beldoBtn.classList.add('active');
    addMessage(initialGreetings.beldo, 'bot', true); // Initial greeting when page loads
});