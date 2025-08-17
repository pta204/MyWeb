import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv  # <<< THÊM DÒNG NÀY

# Nạp các biến môi trường từ file .env
load_dotenv() # <<< THÊM DÒNG NÀY
# chatbot_all_in_one.py

# ... (các dòng import) ...
from dotenv import load_dotenv

# Nạp các biến môi trường từ file .env
load_dotenv()

# =========================================================
# THÊM DÒNG NÀY VÀO ĐỂ KIỂM TRA
print(f"Key đọc được từ .env là: '{os.getenv('GEMINI_API_KEY')}'")
# =========================================================

# Khởi tạo Flask app
app = Flask(__name__)

# ... (phần còn lại của code giữ nguyên) ...

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình Gemini API key
try:
    # Sử dụng os.getenv() để đọc biến môi trường một cách an toàn
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        # Nếu không tìm thấy key, raise lỗi để thông báo rõ ràng
        raise ValueError("Lỗi: Biến môi trường GEMINI_API_KEY chưa được thiết lập hoặc file .env không tồn tại.")

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini model configured successfully.")

except Exception as e:
    print(f"Error during Gemini configuration: {e}")
    model = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"response": "Lỗi: Gemini API chưa được cấu hình. Vui lòng kiểm tra API key trong file .env và khởi động lại server."}), 500

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Vui lòng nhập yêu cầu của bạn."}), 400

    try:
        prompt = f"""
        Bạn là một chuyên gia dinh dưỡng AI. Nhiệm vụ của bạn là tạo ra một thực đơn chi tiết dựa trên yêu cầu của người dùng.
        Yêu cầu của người dùng là: "{user_message}"

        Hãy tạo một thực đơn đầy đủ cho 7 ngày, bao gồm 3 bữa chính (Sáng, Trưa, Tối).
        Với mỗi món ăn, hãy cung cấp:
        1. Tên món ăn.
        2. Hướng dẫn chế biến đơn giản.
        3. Ước tính lượng calo.

        Lưu ý:
        - Sử dụng các nguyên liệu phổ biến, dễ tìm ở Việt Nam.
        - Trình bày rõ ràng, dễ đọc theo từng ngày, sử dụng markdown để định dạng.
        - Giữ giọng văn thân thiện, chuyên nghiệp.
        - Trả lời hoàn toàn bằng tiếng Việt.
        """
        response = model.generate_content(prompt)
        bot_response = response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        bot_response = "Xin lỗi, tôi đang gặp sự cố khi tạo thực đơn. Vui lòng thử lại sau."

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)