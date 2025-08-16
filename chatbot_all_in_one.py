# =========================================================
# PHẦN ĐẦU ĐÃ ĐƯỢC SỬA LẠI ĐỂ TÍCH HỢP GEMINI
# =========================================================
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
import os
import google.generativeai as genai
import markdown

# --- KHỞI TẠO VÀ CẤU HÌNH AN TOÀN ---
try:
    print("==> Bắt đầu quá trình khởi tạo và cấu hình...") # <-- LOG MỚI
    
    # Nạp biến môi trường từ file .env (chỉ có tác dụng khi chạy local)
    load_dotenv()
    
    # --- Khởi tạo ứng dụng Flask ---
    app = Flask(__name__)
    
    # --- CẤU HÌNH BẢO MẬT VÀ API KEYS ---
    SECRET_API_KEY = os.environ.get('SECRET_API_KEY', 'local-secret-key-for-testing')
    
    print("==> Đang đọc biến môi trường GEMINI_API_KEY...") # <-- LOG MỚI
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        # Nếu không có key, ném ra lỗi để bắt ở dưới
        raise ValueError("LỖI NGHIÊM TRỌNG: Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
    
    # In ra vài ký tự đầu của key để xác nhận (nhưng không in ra toàn bộ)
    print(f"==> Đã tìm thấy API Key, bắt đầu bằng: '{GEMINI_API_KEY[:4]}...'") # <-- LOG MỚI
    
    # Cấu hình thư viện Gemini với API Key
    print("==> Đang cấu hình genai với API Key...") # <-- LOG MỚI
    genai.configure(api_key=GEMINI_API_KEY)
    
    # --- Cấu hình cho mô hình Gemini ---
    print("==> Đang tạo model Gemini...") # <-- LOG MỚI
    generation_config = { "temperature": 0.7, "top_p": 1, "top_k": 1, "max_output_tokens": 2048 }
    safety_settings = [
      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)
    
    print("==> Quá trình khởi tạo và cấu hình THÀNH CÔNG!") # <-- LOG MỚI

except Exception as e:
    # Đây là phần quan trọng nhất: Bắt lỗi và in ra chi tiết
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!    ĐÃ XẢY RA LỖI NGHIÊM TRỌNG KHI KHỞI ĐỘNG ỨNG DỤNG    !!!")
    print(f"!!!    LOẠI LỖI: {type(e).__name__}")
    print(f"!!!    CHI TIẾT LỖI: {e}")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # Ném lại lỗi để ứng dụng vẫn dừng lại như bình thường
    raise e

# =========================================================
# PHẦN 2: NỘI DUNG GIAO DIỆN (Giữ nguyên)
# =========================================================

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tư Vấn Dinh Dưỡng</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-content">
                <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L8.3 14.3c.11.18.28.3.47.35.32.09.66-.04.86-.31l1.37-1.92c.19-.27.53-.35.8-.16.27.19.35.53.16.8l-1.37 1.92c-.39.55-.22 1.31.33 1.7.39.28.89.28 1.28 0l4.35-3.05c.39-.27.89-.27 1.28 0l.98.68c.27.19.35.53.16.8l-1.37 1.92c-.2.27-.12.65.19.81.31.16.68.04.88-.23l1.89-2.65c.49.61.89 1.31 1.17 2.07H11z"/></svg>
                <div class="header-text">
                    <h3>NutriAI</h3>
                    <p>Trợ lý Dinh dưỡng</p>
                </div>
            </div>
        </div>
        <div class="chat-messages" id="chat-messages">
             <div class="message bot-message">
                <div class="message-content">
                    Xin chào! Tôi là NutriAI. Bạn cần tôi giúp gì về dinh dưỡng hôm nay?
                </div>
            </div>
            <div class="quick-replies" id="quick-replies">
                <button class="quick-reply-btn">Thực đơn giảm cân</button>
                <button class="quick-reply-btn">Tăng chiều cao và cân nặng</button>
                <button class="quick-reply-btn">Món ăn cho người tiểu đường</button>
            </div>
        </div>
        <div class="chat-input-area">
            <form class="chat-input-form" id="chat-form">
                <input type="text" id="user-input" placeholder="Ví dụ tăng chiều cao" autocomplete="off">
                <button type="submit" aria-label="Gửi">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </form>
        </div>
    </div>
    <script src="/script.js"></script>
</body>
</html>
"""

CSS_CONTENT = """
:root {
    --background-color: #f0f2f5;
    --container-bg: #ffffff;
    --header-bg: #007bff;
    --header-bg-hover: #0056b3;
    --user-message-bg: #007bff;
    --bot-message-bg: #e9e9eb;
    --text-color-primary: #1c1e21;
    --text-color-secondary: #ffffff;
    --text-color-light: #65676b;
    --border-color: #dcdfe3;
    --font-family: 'Nunito', sans-serif;
}
html { scroll-behavior: smooth; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: var(--font-family);
    background-color: var(--background-color);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: var(--text-color-primary);
    padding: 10px;
}
.chat-container {
    width: 100%;
    max-width: 700px; /* Kích thước tối đa trên PC */
    height: 95vh; /* Chiều cao tương đối trên PC/Laptop */
    max-height: 850px;
    background-color: var(--container-bg);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.chat-header {
    background-color: var(--header-bg);
    color: var(--text-color-secondary);
    padding: 16px 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    flex-shrink: 0;
    z-index: 10;
}
.header-content { display: flex; align-items: center; }
.header-icon { width: 40px; height: 40px; margin-right: 12px; }
.header-text h3 { font-size: 1.1rem; font-weight: 700; margin: 0; }
.header-text p { font-size: 0.8rem; opacity: 0.9; margin: 0; }
.chat-messages {
    flex-grow: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.message {
    display: flex;
    max-width: 80%;
    line-height: 1.5;
    animation: slideIn 0.3s ease-out;
}
.message-content {
    padding: 10px 15px;
    border-radius: 18px;
    word-wrap: break-word;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}
.user-message { align-self: flex-end; }
.user-message .message-content {
    background-color: var(--user-message-bg);
    color: var(--text-color-secondary);
    border-bottom-right-radius: 4px;
}
.bot-message { align-self: flex-start; }
.bot-message .message-content {
    background-color: var(--bot-message-bg);
    color: var(--text-color-primary);
    border-bottom-left-radius: 4px;
}
/* HIỆU ỨNG ĐANG GÕ... */
.typing-indicator { display: flex; align-items: center; gap: 5px; padding-top: 8px; }
.typing-indicator span {
    height: 8px; width: 8px;
    background-color: #9db2c2;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0% { opacity: 0.2; } 20% { opacity: 1; } 100% { opacity: 0.2; } }
.quick-replies { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 0; justify-content: flex-start; }
.quick-reply-btn {
    background-color: var(--container-bg);
    border: 1px solid var(--header-bg);
    color: var(--header-bg);
    padding: 8px 14px;
    border-radius: 16px;
    cursor: pointer;
    font-family: var(--font-family);
    font-size: 0.9rem;
    transition: all 0.2s ease;
}
.quick-reply-btn:hover { background-color: var(--header-bg); color: var(--text-color-secondary); transform: translateY(-2px); }
.chat-input-area {
    padding: 15px 20px;
    border-top: 1px solid var(--border-color);
    background-color: #f9fafb;
    flex-shrink: 0;
}
.chat-input-form { display: flex; align-items: center; gap: 10px; }
#user-input {
    flex: 1;
    padding: 12px 18px;
    border: 1px solid var(--border-color);
    border-radius: 22px;
    font-size: 1rem;
    font-family: var(--font-family);
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
}
#user-input:focus { border-color: var(--header-bg); box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15); }
button[type="submit"] {
    width: 44px; height: 44px;
    border: none; background-color: var(--header-bg);
    color: var(--text-color-secondary);
    border-radius: 50%; cursor: pointer;
    display: flex; justify-content: center; align-items: center;
    transition: background-color 0.2s;
}
button[type="submit"]:hover { background-color: var(--header-bg-hover); }
button[type="submit"] svg { width: 24px; height: 24px; }
.chat-messages::-webkit-scrollbar { width: 6px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
.chat-messages::-webkit-scrollbar-thumb:hover { background: #aaa; }

/* === TỐI ƯU RESPONSIVE === */

/* Cho Tablet */
@media (max-width: 768px) {
    .chat-messages { padding: 15px; }
    .quick-reply-btn { font-size: 0.85rem; padding: 7px 12px; }
}

/* Cho Mobile */
@media (max-width: 500px) {
    body { padding: 0; }
    .chat-container {
        height: 100vh;
        width: 100vw;
        border-radius: 0;
        max-height: none;
    }
    .chat-header { padding: 12px 15px; }
    .chat-input-area { padding: 10px 15px; }
    .message { max-width: 90%; }
}
"""

JS_CONTENT = """
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const quickRepliesContainer = document.getElementById('quick-replies');
    const quickReplyButtons = document.querySelectorAll('.quick-reply-btn');
    const API_KEY = "local-secret-key-for-testing";

    async function sendMessage(message) {
        if (!message) return;
        if (quickRepliesContainer) { quickRepliesContainer.style.display = 'none'; }
        appendMessage(message, 'user-message');
        const loadingMessageElem = showTypingIndicator();
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
                body: JSON.stringify({ message: message })
            });
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
            if (chatMessages.contains(loadingMessageElem)) {
                chatMessages.removeChild(loadingMessageElem);
            }
            appendMessage("Không thể kết nối đến server. Vui lòng thử lại.", 'bot-message');
        }
    }

    function appendMessage(html, type) {
        const messageElem = document.createElement('div');
        messageElem.className = `message ${type}`;
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = html;
        messageElem.appendChild(messageContent);
        chatMessages.appendChild(messageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const indicatorHtml = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>`;
        const loadingMessageElem = document.createElement('div');
        loadingMessageElem.className = 'message bot-message';
        loadingMessageElem.innerHTML = indicatorHtml;
        chatMessages.appendChild(loadingMessageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return loadingMessageElem;
    }

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        sendMessage(message);
        userInput.value = '';
    });

    quickReplyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const message = button.textContent;
            sendMessage(message);
        });
    });
});
"""
# =========================================================
# PHẦN 3: CÁC ROUTE CỦA FLASK
# =========================================================

@app.route("/")
def index(): return HTML_CONTENT
@app.route("/style.css")
def style(): return Response(CSS_CONTENT, mimetype='text/css')
@app.route("/script.js")
def script(): return Response(JS_CONTENT, mimetype='application/javascript')

@app.route("/chat", methods=["POST"])
def chat():
    client_api_key = request.headers.get('X-API-Key')
    if not client_api_key or client_api_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Vui lòng nhập yêu cầu của bạn."})

    prompt = f"""
    ### BỐI CẢNH ###
    Bạn là một trợ lý AI tên là NutriAI, một chuyên gia dinh dưỡng ảo. Sứ mệnh của bạn là cung cấp thông tin dinh dưỡng chính xác, hữu ích và an toàn cho người dùng.
    
    ### QUY TẮC BẮT BUỘC ###
    1.  **Chính xác & Ngắn gọn:** Luôn trả lời đi thẳng vào vấn đề, sử dụng ngôn ngữ tự nhiên, dễ hiểu. Thông tin phải chính xác.
    2.  **Thân thiện & Chuyên nghiệp:** Giữ giọng văn thân thiện, tích cực và chuyên nghiệp.
    3.  **Duy trì ngữ cảnh:** Luôn ghi nhớ các phần trước của cuộc trò chuyện để câu trả lời được liền mạch.
    4.  **BẢO MẬT LÀ TRÊN HẾT:** Tuyệt đối không bao giờ yêu cầu người dùng cung cấp thông tin cá nhân nhạy cảm như email, số điện thoại, mật khẩu, địa chỉ nhà.
    5.  **An toàn y tế:** Nếu yêu cầu của người dùng liên quan đến bệnh lý nghiêm trọng, tình trạng y tế phức tạp, hoặc cần chẩn đoán, bạn PHẢI từ chối một cách lịch sự và nhấn mạnh rằng "Tôi chỉ là một AI, tôi không thể thay thế cho bác sĩ hay chuyên gia y tế. Bạn nên tham khảo ý kiến của chuyên gia thực thụ để có lời khuyên chính xác nhất."
    6.  **Khi không biết:** Nếu bạn không biết câu trả lời, hãy thừa nhận một cách trung thực. Ví dụ: "Đây là một câu hỏi rất hay, nhưng thông tin này nằm ngoài tầm hiểu biết hiện tại của tôi." Đừng bịa đặt thông tin.

    ### ĐỊNH DẠNG ĐẦU RA ###
    -   Sử dụng Markdown để định dạng câu trả lời (tiêu đề, danh sách, in đậm) cho dễ đọc.
    -   Nếu tạo thực đơn, hãy bao gồm: mô tả ngắn, ước tính calo, chi tiết các bữa ăn, và mẹo nhỏ.
    
    ### YÊU CẦU CỦA NGƯỜI DÙNG ###
    "{user_message}"
    
    ### CÂU TRẢ LỜI CỦA BẠN ###
    """

    try:
        response = model.generate_content(prompt)
        html_reply = markdown.markdown(response.text)
        return jsonify({"reply": html_reply})
    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")
        return jsonify({"error": "Xin lỗi, tôi đang gặp sự cố khi kết nối đến bộ não AI. Vui lòng thử lại sau."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)