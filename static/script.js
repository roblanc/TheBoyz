document.addEventListener('DOMContentLoaded', function() {
    const beldoBtn = document.getElementById('beldo-btn');
    const undeBtn = document.getElementById('unde-btn');
    const mariusBtn = document.getElementById('marius-btn');
    const chatArea = document.getElementById('chat-area');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const historyDiv = document.getElementById('history');
    let currentChatbot = 'beldo';
    const body = document.body;

    // Initial greetings
    const initialGreetings = {
        beldo: "I am Beldo zis si Mama Bebe... pe tine cum te numesti?",
        unde: "Nu sunt aryan, sunt pariah, nu paria. Vreau să plec în Spania, spirit de rastafarian. Tu ce te numesti?",
        marius: "Sa pronunt numele Jizzy Boy Lemuriano este activitatea care imi place! Tie ce-ti place sa numesti ca faci?"
    };

    // Function to add message
    function addMessage(message, sender, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender);
        if (isBot) {
            messageDiv.classList.add('bot');
            if (currentChatbot === 'marius') {
                messageDiv.classList.add('marius');
            }
            messageDiv.innerHTML = `<div class='chatbot-name'>${currentChatbot.charAt(0).toUpperCase() + currentChatbot.slice(1)}:</div><div class='message-text'>${message}</div>`;
        } else {
            messageDiv.textContent = message;
        }
        historyDiv.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    // Function to send message
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        userInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                chatbot_name: currentChatbot
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot', true);
            } else {
                addMessage('Error: Could not get response.', 'bot', true);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Error communicating with chatbot.', 'bot', true);
        });
    }

    // Send button event listener
    sendBtn.addEventListener('click', sendMessage);

    // Enter key event listener
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
        mariusBtn.classList.remove('active');
        body.classList.remove('rastafarian-bg');
        body.classList.remove('david-lynch-bg');
        body.classList.add('beldo-bg'); // Add beldo-bg for Beldo
        historyDiv.innerHTML = '';
        addMessage(initialGreetings.beldo, 'bot', true);
    });

    undeBtn.addEventListener('click', function() {
        currentChatbot = 'unde';
        undeBtn.classList.add('active');
        beldoBtn.classList.remove('active');
        mariusBtn.classList.remove('active');
        body.classList.add('rastafarian-bg');
        body.classList.remove('david-lynch-bg');
        body.classList.remove('beldo-bg'); // Remove beldo-bg
        historyDiv.innerHTML = '';
        addMessage(initialGreetings.unde, 'bot', true);
    });

    mariusBtn.addEventListener('click', function() {
        currentChatbot = 'marius';
        mariusBtn.classList.add('active');
        beldoBtn.classList.remove('active');
        undeBtn.classList.remove('active');
        body.classList.remove('rastafarian-bg');
        body.classList.add('david-lynch-bg'); // Add david-lynch-bg for Marius
        body.classList.remove('beldo-bg'); // Remove beldo-bg
        historyDiv.innerHTML = '';
        addMessage(initialGreetings.marius, 'bot', true);
    });

    // Initial chatbot and greeting
    beldoBtn.classList.add('active');
    body.classList.add('beldo-bg'); // Set Beldo background on load
    addMessage(initialGreetings.beldo, 'bot', true);
});