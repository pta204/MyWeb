# =========================================================
# PHẦN ĐẦU ĐÃ ĐƯỢC SỬA LẠI ĐỂ TÍCH HỢP GEMINI
# =========================================================
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv, find_dotenv # <-- THÊM find_dotenv VÀO ĐÂY
import os
import google.generativeai as genai
import markdown

# --- ĐOẠN CODE DEBUG ---
# Thêm đoạn này vào để kiểm tra
print("================ DEBUGGING ================")
# 1. Tìm kiếm file .env
dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Đã tìm thấy file .env tại đường dẫn: {dotenv_path}")
else:
    print("!!! CẢNH BÁO: Không tìm thấy file .env ở đâu cả!")
    print(f"Thư mục làm việc hiện tại là: {os.getcwd()}")

# 2. Nạp file .env
load_dotenv() 
print("Đã thực thi lệnh load_dotenv()")
print("============================================")
# --- HẾT ĐOẠN CODE DEBUG ---


# --- Khởi tạo ứng dụng Flask ---
app = Flask(__name__)

# --- CẤU HÌNH BẢO MẬT VÀ API KEYS (Cách làm đúng) ---
# 1. API Key bí mật để bảo vệ endpoint /chat của bạn
SECRET_API_KEY = os.environ.get('SECRET_API_KEY', 'local-secret-key-for-testing')

# 2. Lấy API Key của Gemini từ biến môi trường
#    Trên Render, bạn cần tạo một biến môi trường tên là 'GEMINI_API_KEY'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    # Nếu không có key, chatbot sẽ không hoạt động. Cần báo lỗi rõ ràng.
    # Thêm một print nữa ở đây để xác nhận
    print("\n!!! LỖI CUỐI CÙNG: Biến GEMINI_API_KEY vẫn là None sau khi load .env\n")
    raise ValueError("Không tìm thấy GEMINI_API_KEY. Vui lòng thiết lập key.")

# Cấu hình thư viện Gemini với API Key
genai.configure(api_key=GEMINI_API_KEY)

# ... (phần còn lại của code giữ nguyên) ...
# =========================================================
# PHẦN 1: DỮ LIỆU THỰC ĐƠN MẪU -> ĐÃ BỊ XÓA
# Chúng ta không cần THUC_DON_MAU nữa vì Gemini sẽ tạo nội dung động.
# Việc này giúp mã nguồn gọn hơn và chatbot thông minh hơn.
# =========================================================


# =========================================================
# PHẦN 2: LOGIC PYTHON VÀ NỘI DUNG GIAO DIỆN
# =========================================================

# --- Cấu hình cho mô hình Gemini ---
# Chọn mô hình phù hợp. 'gemini-1.5-flash' nhanh và hiệu quả.
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# --- Các nội dung HTML, CSS, JS giữ nguyên ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Thực Đơn Dinh Dưỡng</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>AI Tư Vấn Dinh Dưỡng (Gemini)</h2>
        </div>
        <div class="chat-messages" id="chat-messages">
             <div class="message bot-message">
                Xin chào! Tôi là chuyên gia dinh dưỡng AI. Bạn hãy cho tôi biết mục tiêu của bạn là gì? Ví dụ: "tạo thực đơn giảm cân 1500 calo trong 1 ngày", "thực đơn eat clean cho người bận rộn", "các món ăn tốt cho trí não"...
            </div>
        </div>
        <form class="chat-input-form" id="chat-form">
            <input type="text" id="user-input" placeholder="Nhập yêu cầu của bạn...">
            <button type="submit">Gửi</button>
        </form>
    </div>
    <script src="/script.js"></script>
</body>
</html>
"""

CSS_CONTENT = """
body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
.chat-container { max-width: 600px; margin: 50px auto; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
.chat-header { background-color: #4A90E2; color: white; padding: 15px; text-align: center; } /* Đổi màu cho mới */
.chat-messages { padding: 20px; height: 400px; overflow-y: auto; background-color: #fff; }
.message { margin-bottom: 15px; padding: 10px 15px; border-radius: 18px; line-height: 1.5; max-width: 80%; }
.user-message { background-color: #DCF8C6; text-align: left; margin-left: auto; }
.bot-message { background-color: #f1f0f0; text-align: left; }
.chat-input-form { display: flex; padding: 10px; border-top: 1px solid #ccc; background-color: #f9f9f9; }
#user-input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 20px; }
button { padding: 10px 15px; border: none; background-color: #4A90E2; color: white; border-radius: 20px; cursor: pointer; margin-left: 10px; }
h3 { color: #4A90E2; }
h4 { margin-bottom: 5px; }
ul { padding-left: 20px; margin-top: 5px; }
li > em { color: #555; font-size: 0.9em; }
/* Thêm style cho bảng nếu Gemini trả về bảng */
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
"""

# Chú ý: Cần cập nhật API_KEY trong JS cho khớp với SECRET_API_KEY
# Ví dụ: os.environ.get('SECRET_API_KEY', 'local-key') thì ở đây cũng phải là 'local-key'
# Để đơn giản, tôi sẽ giữ nguyên key tạm thời bạn đang dùng.
JS_CONTENT = """
document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const API_KEY = "local-secret-key-for-testing"; // <-- QUAN TRỌNG: Key này phải khớp với SECRET_API_KEY trên server.
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message === "") return;

    const chatMessages = document.getElementById('chat-messages');
    
    // Hiển thị tin nhắn người dùng
    const userMessageElem = document.createElement('div');
    userMessageElem.className = 'message user-message';
    userMessageElem.textContent = message;
    chatMessages.appendChild(userMessageElem);
    userInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Hiển thị trạng thái "Bot đang gõ..."
    const loadingMessageElem = document.createElement('div');
    loadingMessageElem.className = 'message bot-message';
    loadingMessageElem.innerHTML = "<em>AI đang suy nghĩ...</em>";
    chatMessages.appendChild(loadingMessageElem);
    chatMessages.scrollTop = chatMessages.scrollHeight;


    // Gửi yêu cầu đến server
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
        
        const botMessageElem = document.createElement('div');
        botMessageElem.className = 'message bot-message';

        if (response.status === 401) {
            botMessageElem.innerHTML = "Lỗi: API Key không hợp lệ. Vui lòng kiểm tra lại.";
        } else if (!response.ok) {
            const errorData = await response.json();
            botMessageElem.innerHTML = `Lỗi từ server: ${errorData.error || 'Có lỗi xảy ra'}`;
        } else {
            const data = await response.json();
            botMessageElem.innerHTML = data.reply;
        }
        
        chatMessages.appendChild(botMessageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;

    } catch (error) {
        chatMessages.removeChild(loadingMessageElem);
        const errorMessageElem = document.createElement('div');
        errorMessageElem.className = 'message bot-message';
        errorMessageElem.innerHTML = "Không thể kết nối đến server. Vui lòng thử lại.";
        chatMessages.appendChild(errorMessageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
"""

# =========================================================
# PHẦN 3: CÁC ROUTE CỦA FLASK (ĐÃ SỬA LẠI ROUTE /CHAT)
# =========================================================

@app.route("/")
def index():
    return HTML_CONTENT

@app.route("/style.css")
def style():
    return Response(CSS_CONTENT, mimetype='text/css')

@app.route("/script.js")
def script():
    return Response(JS_CONTENT, mimetype='application/javascript')

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Xác thực API Key của client (giữ nguyên)
    client_api_key = request.headers.get('X-API-Key')
    if not client_api_key or client_api_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Vui lòng nhập yêu cầu của bạn."})

    # 2. Tạo prompt (câu lệnh) cho Gemini
    # Đây là phần quan trọng nhất để điều khiển AI
    prompt = f"""
    Bạn là một chuyên gia dinh dưỡng AI tên là NutriAI, rất thân thiện và chuyên nghiệp.
    Nhiệm vụ của bạn là tạo ra các thực đơn và đưa ra lời khuyên dinh dưỡng dựa trên yêu cầu của người dùng.
    Luôn trả lời bằng tiếng Việt.
    Hãy định dạng câu trả lời bằng Markdown để dễ đọc, bao gồm tiêu đề, danh sách, in đậm.
    
    YÊU CẦU CỦA NGƯỜI DÙNG: "{user_message}"
    
    DỰA VÀO YÊU CẦU TRÊN, HÃY CUNG CẤP CÂU TRẢ LỜI.
    Nếu người dùng yêu cầu tạo thực đơn, hãy bao gồm:
    - Một mô tả ngắn về thực đơn.
    - Ước tính lượng calo tổng (nếu có thể).
    - Chi tiết các bữa ăn (Sáng, Trưa, Tối, và có thể có bữa Phụ).
    - Một vài hướng dẫn nấu ăn đơn giản hoặc mẹo nhỏ.
    
    Nếu yêu cầu không liên quan đến dinh dưỡng, sức khỏe, hoặc nấu ăn, hãy từ chối một cách lịch sự.
    """

    try:
        # 3. Gửi prompt đến API của Gemini
        response = model.generate_content(prompt)
        
        # 4. Xử lý và trả về kết quả
        # Chuyển đổi văn bản Markdown từ Gemini sang HTML
        html_reply = markdown.markdown(response.text)
        return jsonify({"reply": html_reply})
        
    except Exception as e:
        # Ghi lại lỗi để debug trên server
        print(f"Lỗi khi gọi Gemini API: {e}")
        # Trả về thông báo lỗi cho người dùng
        return jsonify({"error": "Xin lỗi, tôi đang gặp sự cố khi kết nối đến bộ não AI. Vui lòng thử lại sau."}), 500


# Dòng này chỉ dùng khi chạy ở máy bạn
if __name__ == "__main__":
    # Nhắc nhở người dùng thiết lập key khi chạy local
    if not os.environ.get('GEMINI_API_KEY'):
        print("CẢNH BÁO: Biến môi trường 'GEMINI_API_KEY' chưa được thiết lập.")
        print("Chatbot có thể sẽ không hoạt động. Hãy tạo file .env hoặc export biến môi trường.")
    app.run(host="0.0.0.0", port=5000, debug=True)