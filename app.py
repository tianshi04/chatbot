import os
import google.generativeai as genai
import dotenv
import json
from flask import Flask, jsonify, request, render_template
import copy

# Load .env file
dotenv.load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Bạn là một người bạn hỗ trợ tui học về ngôn ngữ python. Bạn đôi khi hài hước, lấy những ví dụ trực quan dễ hiều, gần gủi",
)
 
chat_session = model.start_chat(
  history=[
    
  ]
) 

chat_session_dict = {}


# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Trang chính hiển thị giao diện người dùng
@app.route('/')
def index():
    return render_template('index.html')

# Tạo route để nhận yêu cầu GET
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

# Route để nhận tin nhắn và trả lời
@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message', '')
    
    # Tạo câu trả lời cho tin nhắn
    if message:
        if request.headers.getlist("X-Forwarded-For"):
          user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
          user_ip = request.remote_addr

        if user_ip not in chat_session_dict:
          chat_session_dict[user_ip] = copy.deepcopy(chat_session)

        print(user_ip + " : ", message)
        response = chat_session_dict[user_ip].send_message(message)
        response_message = response.text
        print(response_message)

    else:
        response_message = "No message received"
    
    # Trả lời lại client
    return jsonify(response=response_message)

# Khởi chạy server
if __name__ == '__main__':
    app.run(debug=True)