from flask import Flask, render_template, request, jsonify
from therapy import get_ai_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "I'm here to listen. Please tell me what's on your mind."
        })

    try:
        ai_reply = get_ai_response(user_message)

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        print(e)

        return jsonify({
            "reply": "I'm sorry, I couldn't respond right now. Please try again."
        })


if __name__ == "__main__":
    app.run(debug=True)