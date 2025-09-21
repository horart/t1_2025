// Функционал чата

async function sendPromptToEmployee(promptData) {
    try {
        const response = await fetch("/api/user/prompt", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: promptData
        });

        if (!response.ok) {
                return "Извините, что-то пошло не так! Попробуйте обратиться позже!"
        }

        const result = await response.json();
        return result;
    } catch (error) {
        return "Извините, что-то пошло не так! Попробуйте обратиться позже!";
    }
}



// Функционал чата
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const typingIndicator = document.getElementById('typingIndicator');

    // Пример начальных сообщений
    const initialMessages = [
        {
            text: "Добро пожаловать в чат с HR-консультантом! Чем я могу вам помочь?",
            sender: "HR Консультант",
            time: "10:00",
            type: "incoming"
        },
    ];

    // Загрузка начальных сообщений
    initialMessages.forEach(message => {
        addMessageToChat(message.text, message.sender, message.time, message.type);
    });

    // Прокрутка вниз при загрузке
    scrollToBottom();

    // Отправка сообщения по клику на кнопку
    sendMessageBtn.addEventListener('click', sendMessage);

    // Отправка сообщения по нажатию Enter
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Функция отправки сообщения
    function sendMessage() {
        const messageText = messageInput.value.trim();

        if (messageText === '') return;

        // Добавляем исходящее сообщение
        const now = new Date();
        const timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();

        addMessageToChat(messageText, 'Вы', timeString, 'outgoing');
        messageInput.value = '';
        scrollToBottom();

        // Имитация набора текста консультантом
        result = simulateTyping(messageText);
        const now = new Date();
        const timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        addMessageToChat(result, 'HR Консультант', timeString, 'incoming');
    }

    // Функция добавления сообщения в чат
    function addMessageToChat(text, sender, time, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `message-${type}`);

        messageElement.innerHTML = `
            <div class="message-text">${text}</div>
            <div class="message-info">
                <span class="message-sender">${sender}</span>
                <span class="message-time">${time}</span>
            </div>
        `;

        chatMessages.appendChild(messageElement);
    }

    // Функция прокрутки вниз
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Имитация набора текста и ответа
    function simulateTyping(messageText) {
        // Показываем индикатор набора текста
        typingIndicator.classList.add('active');
        sendMessageBtn.disabled = true;

        // Случайная задержка для имитации реального ответа
        const delay = Math.floor(Math.random() * 3000) + 1000;
        result = sendPromptToEmployee(messageText);

        setTimeout(() => {
            typingIndicator.classList.remove('active');
            sendMessageBtn.disabled = false;
            return result

        }, delay);
    }

    // Фокус на поле ввода при загрузке
    messageInput.focus();
});