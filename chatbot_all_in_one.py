# =========================================================
# PHẦN ĐẦU ĐÃ ĐƯỢC SỬA LẠI
# =========================================================
from flask import Flask, request, jsonify, Response
import os # Thư viện os để đọc biến môi trường

# --- Khởi tạo ứng dụng Flask (Chỉ cần 1 dòng) ---
app = Flask(__name__)

# --- CẤU HÌNH BẢO MẬT (Cách làm đúng) ---
# Lấy API Key từ biến môi trường trên Render.
# Nếu chạy ở máy bạn, nó sẽ dùng key tạm thời.
SECRET_API_KEY = os.environ.get('SECRET_API_KEY', 'local-secret-key-for-testing')
# =========================================================


# =========================================================
# PHẦN 1: DỮ LIỆU THỰC ĐƠN (CHỈ CẦN MỘT LẦN)
# =========================================================
THUC_DON_MAU = {
    "giảm cân": {
        "mô tả": "Thực đơn này tập trung vào việc giảm calo nhưng vẫn đảm bảo đủ chất, giàu protein và chất xơ để bạn no lâu hơn.",
        "calo_ước_tính": "1500-1700 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "2 trứng luộc và 1 quả táo. (250 kcal)", "Trưa": "Ức gà luộc (150g) với salad rau xanh. (400 kcal)", "Tối": "Cá diêu hồng hấp gừng (200g) và rau củ luộc. (500 kcal)", "Hướng dẫn": "<b>Trứng luộc:</b> Luộc sôi trong 8-10 phút. <b>Ức gà luộc:</b> Luộc với vài lát gừng cho thơm. <b>Cá hấp gừng:</b> Khứa nhẹ cá, hấp với gừng thái sợi, hành lá và một chút nước tương."},
            "Thứ Ba": {"Sáng": "Yến mạch (40g) nấu với sữa tươi không đường và chuối. (350 kcal)", "Trưa": "Thịt bò xào bông cải xanh (100g thịt). (450 kcal)", "Tối": "Canh bí đao nấu tôm (100g tôm) và cơm gạo lứt. (400 kcal)", "Hướng dẫn": "<b>Yến mạch:</b> Cho yến mạch và sữa vào nồi, đun nhỏ lửa 5 phút đến khi đặc lại. <b>Bò xào:</b> Ướp bò với tỏi, xào nhanh trên lửa lớn rồi cho bông cải xanh đã luộc sơ vào đảo đều."},
            # ... (Các ngày còn lại cho giảm cân) ...
        }
    },
    "tăng cân lành mạnh": {
        "mô tả": "Thực đơn này tập trung vào việc tạo ra thặng dư calo từ các nguồn thực phẩm bổ dưỡng, giàu năng lượng để giúp bạn tăng cân một cách khỏe mạnh.",
        "calo_ước_tính": "2800-3200 kcal/ngày",
        "chi_tiết": {
             "Thứ Hai": {"Sáng": "Yến mạch (80g) nấu sữa nguyên kem, chuối, hạt óc chó, mật ong. (700 kcal)", "Trưa": "Cơm trắng (2 chén), thịt kho trứng (2 quả, 100g thịt). (850 kcal)", "Tối": "Cơm (1.5 chén), đùi gà chiên mắm (200g). (800 kcal)", "Phụ": "Sinh tố bơ chuối và bơ đậu phộng. (500 kcal)", "Hướng dẫn": "<b>Thịt kho trứng:</b> Thắng nước màu, cho thịt ba chỉ vào xào săn, thêm nước mắm, đường, nước dừa và trứng luộc, kho nhỏ lửa. <b>Gà chiên mắm:</b> Chiên vàng gà, vớt ra. Pha sốt mắm tỏi ớt đường rồi cho gà vào đảo đều."},
             # ... (Các ngày còn lại cho tăng cân) ...
        }
    },
    # ... (TẤT CẢ CÁC THỰC ĐƠN KHÁC CỦA BẠN) ...
    "chống viêm": {
        "mô tả": "Giảm viêm trong cơ thể bằng cách tập trung vào thực phẩm giàu chất chống oxy hóa. Hạn chế thực phẩm chế biến sẵn và đường.",
        "calo_ước_tính": "1700-2000 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Sinh tố cải bó xôi, dứa, gừng, nước cốt dừa. (350 kcal)", "Trưa": "Salad lớn với cá ngừ, bơ, cà chua, sốt dầu oliu. (550 kcal)", "Tối": "Cà ri gà với nghệ, rau củ, gạo lứt. (600 kcal)", "Hướng dẫn": "<b>Cà ri nghệ:</b> Nghệ chứa curcumin là chất chống viêm cực mạnh. Luôn dùng kèm một ít tiêu đen để tăng hấp thu."},
            # ... (Các ngày còn lại cho chống viêm) ...
        }
    }
}


# =========================================================
# PHẦN 2: LOGIC PYTHON VÀ NỘI DUNG GIAO DIỆN
# =========================================================

def tao_thuc_don(muc_tieu):
    muc_tieu = muc_tieu.lower().strip()
    if muc_tieu in THUC_DON_MAU:
        return THUC_DON_MAU[muc_tieu]
    else:
        return None

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
            <h2>AI Tư Vấn Dinh Dưỡng</h2>
        </div>
        <div class="chat-messages" id="chat-messages">
             <div class="message bot-message">
                Xin chào! Mục tiêu của bạn là gì? (vd: giảm cân, tăng cân, tăng cơ, ăn chay, eat clean, keto, tiểu đường, bận rộn, tim mạch, trí não, tiêu hóa, chống viêm...)
            </div>
        </div>
        <form class="chat-input-form" id="chat-form">
            <input type="text" id="user-input" placeholder="Nhập mục tiêu của bạn...">
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
.chat-header { background-color: #4CAF50; color: white; padding: 15px; text-align: center; }
.chat-messages { padding: 20px; height: 400px; overflow-y: auto; background-color: #fff; }
.message { margin-bottom: 15px; padding: 10px 15px; border-radius: 18px; line-height: 1.5; max-width: 80%; }
.user-message { background-color: #DCF8C6; text-align: left; margin-left: auto; }
.bot-message { background-color: #f1f0f0; text-align: left; }
.chat-input-form { display: flex; padding: 10px; border-top: 1px solid #ccc; background-color: #f9f9f9; }
#user-input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 20px; }
button { padding: 10px 15px; border: none; background-color: #4CAF50; color: white; border-radius: 20px; cursor: pointer; margin-left: 10px; }
h3 { color: #4CAF50; }
h4 { margin-bottom: 5px; }
ul { padding-left: 20px; margin-top: 5px; }
li > em { color: #555; font-size: 0.9em; }
"""

JS_CONTENT = """
document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    // Đảm bảo API Key này khớp với giá trị bạn đặt trên Render
    const API_KEY = "MySuperSecretChatbotKey123!@#"; 
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

    // Gửi yêu cầu đến server
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        },
        body: JSON.stringify({ message: message })
    });

    // Xử lý phản hồi từ server
    const botMessageElem = document.createElement('div');
    botMessageElem.className = 'message bot-message';

    if (response.status === 401) {
        botMessageElem.innerHTML = "Lỗi: API Key không hợp lệ. Vui lòng kiểm tra lại.";
    } else {
        const data = await response.json();
        botMessageElem.innerHTML = data.reply;
    }
    
    chatMessages.appendChild(botMessageElem);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
"""

# =========================================================
# PHẦN 3: CÁC ROUTE CỦA FLASK
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
    client_api_key = request.headers.get('X-API-Key')
    if not client_api_key or client_api_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
        
    user_message = request.json.get("message").lower()
    if not user_message:
        return jsonify({"reply": "Vui lòng nhập mục tiêu của bạn."})
        
    muc_tieu_tim_thay = None
    if "giảm cân" in user_message: muc_tieu_tim_thay = "giảm cân"
    elif "tăng cơ" in user_message: muc_tieu_tim_thay = "tăng cơ"
    elif "tăng cân" in user_message: muc_tieu_tim_thay = "tăng cân lành mạnh"
    elif "ăn chay" in user_message: muc_tieu_tim_thay = "ăn chay"
    elif "eat clean" in user_message or "lành mạnh" in user_message: muc_tieu_tim_thay = "eat clean"
    elif "keto" in user_message: muc_tieu_tim_thay = "keto"
    elif "tiểu đường" in user_message: muc_tieu_tim_thay = "tiểu đường"
    elif "bận rộn" in user_message or "nhanh" in user_message: muc_tieu_tim_thay = "bận rộn"
    elif "tim mạch" in user_message: muc_tieu_tim_thay = "tốt cho tim mạch"
    elif "trí não" in user_message or "minh mẫn" in user_message: muc_tieu_tim_thay = "tăng cường trí não"
    elif "tiêu hóa" in user_message: muc_tieu_tim_thay = "cải thiện tiêu hóa"
    elif "chống viêm" in user_message or "đề kháng" in user_message: muc_tieu_tim_thay = "chống viêm"
    
    if muc_tieu_tim_thay:
        thuc_don = tao_thuc_don(muc_tieu_tim_thay)
        reply_text = f"<h3>Thực đơn gợi ý cho mục tiêu '{muc_tieu_tim_thay.upper()}'</h3>"
        reply_text += f"<p><em>{thuc_don['mô tả']}</em></p>"
        reply_text += f"<p><strong>Lượng calo ước tính:</strong> {thuc_don['calo_ước_tính']}</p>"
        for ngay, bua_an in thuc_don['chi_tiết'].items():
            reply_text += f"<h4>{ngay}</h4><ul>"
            for bua, mon in bua_an.items():
                if bua != "Hướng dẫn":
                    reply_text += f"<li><strong>{bua}:</strong> {mon}</li>"
            reply_text += f"<li><em>Hướng dẫn: {bua_an['Hướng dẫn']}</em></li>"
            reply_text += "</ul>"
    else:
        reply_text = "Xin lỗi, tôi chưa có thực đơn cho mục tiêu này. Bạn vui lòng thử lại với các từ khóa được gợi ý."
        
    return jsonify({"reply": reply_text})

# Dòng này chỉ dùng khi chạy ở máy bạn, Gunicorn sẽ không dùng nó
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)