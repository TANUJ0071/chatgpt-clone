from flask import Flask, render_template, jsonify, request
import requests

OPENROUTER_API_KEY = ""  #your api here
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def qa():
    questioninput = request.json.get("question")
    
    if not questioninput:
        return jsonify({"error": "No question provided"}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "ChatGPT"
    }

    data = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": questioninput}
        ],
        "max_tokens": 3000,
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{OPENROUTER_BASE_URL}/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()

            print("API Response:", response_data)

            if "choices" in response_data and response_data["choices"]:
                content = response_data["choices"][0].get("message", {}).get("content", "")
                if content:
                    return jsonify({"result": content})
                else:
                    return jsonify({"error": "Response is missing content."}), 500
            else:
                return jsonify({"error": "No valid response from the model."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred during the API request: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
