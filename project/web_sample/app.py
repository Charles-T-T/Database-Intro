import openai
from flask import Flask, render_template, request, jsonify

# 设置 OpenAI API 密钥
# openai.api_key = 'your-api-key'

# 创建 Flask 应用
app = Flask(__name__)

# 创建函数与 OpenAI API 进行交互
def get_ai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 使用 gpt-3.5-turbo 模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# 首页
@app.route("/")
def index():
    # 加载页面时直接发送欢迎消息
    initial_message = {"role": "assistant", "content": "Welcome!"}
    return render_template("index.html", initial_message=initial_message)

# 处理用户消息
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    ai_message = get_ai_response(user_message)
    return jsonify({"ai_message": ai_message})

if __name__ == "__main__":
    app.run(debug=True)
    # http://127.0.0.1:5000/
