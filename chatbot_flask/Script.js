JS_CONTENT = """
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const quickRepliesContainer = document.getElementById('quick-replies');
    const quickReplyButtons = document.querySelectorAll('.quick-reply-btn');

    const API_KEY = "local-secret-key-for-testing"; // <-- QUAN TRỌNG: Key này phải khớp với SECRET_API_KEY trên server.

    // Hàm xử lý việc gửi tin nhắn và nhận phản hồi
    async function sendMessage(message) {
        if (!message) return;

        // Ẩn các nút chọn nhanh sau khi bắt đầu chat
        if (quickRepliesContainer) {
            quickRepliesContainer.style.display = 'none';
        }

        // Hiển thị tin nhắn của người dùng
        appendMessage(message, 'user-message');
        
        // Hiển thị trạng thái "Bot đang gõ..."
        const loadingMessageElem = appendMessage("<em>AI đang suy nghĩ...</em>", 'bot-message', true);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': API_KEY
                },
                body: JSON.stringify({ message: message })
            });

            // Xóa tin nhắn "đang gõ"
            chatMessages.removeChild(loadingMessageElem);

            let replyHtml = '';
            if (response.status === 401) {
                replyHtml = "Lỗi: API Key không hợp lệ. Vui lòng kiểm tra lại.";
            } else if (!response.ok) {
                const errorData = await response.json();
                replyHtml = `Lỗi từ server: ${errorData.error || 'Có lỗi xảy ra'}`;
            } else {
                const data = await response.json();
                replyHtml = data.reply;
            }
            appendMessage(replyHtml, 'bot-message');

        } catch (error) {
            chatMessages.removeChild(loadingMessageElem);
            appendMessage("Không thể kết nối đến server. Vui lòng thử lại.", 'bot-message');
        }
    }

    // Hàm để thêm tin nhắn vào giao diện
    function appendMessage(html, type, returnElement = false) {
        const messageElem = document.createElement('div');
        messageElem.className = `message ${type}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = html;
        
        messageElem.appendChild(messageContent);
        chatMessages.appendChild(messageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        if (returnElement) {
            return messageElem;
        }
    }

    // Lắng nghe sự kiện submit form
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        sendMessage(message);
        userInput.value = '';
    });

    // Lắng nghe sự kiện click vào các nút chọn nhanh
    quickReplyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const message = button.textContent;
            sendMessage(message);
        });
    });
});
"""