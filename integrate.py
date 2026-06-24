from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# ================= CONFIG =================

app = Flask(__name__)
CORS(app)

# Set your Gemini API key here OR use environment variable
GEMINI_API_KEY = os.getenv("AIzaSyAQHPlEhSPsFgkujYn2SQoFEw2G_wRquQE")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ================= ROUTES =================

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return jsonify({"message": "Gemini API Backend Running 🚀"})


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True, port=8000)