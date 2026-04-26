from flask import Flask, render_template, request

from .handle import handle_message

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        update = request.json
        try:
            handle_message(update)
        except Exception as e:
            print(f"Error while handling update: {repr(e)}")
        return "ok"
    return render_template("status.html")
