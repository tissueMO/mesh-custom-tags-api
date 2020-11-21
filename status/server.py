##########################################################################################
#    内蔵アプリケーションサーバーを起動します。
##########################################################################################
from flask import Flask, request
import api.main as main

app = Flask(__name__)

@app.route("/reset", methods=["GET", "POST"])
def reset():
    return main.reset()

@app.route("/on", methods=["GET", "POST"])
def on():
    return main.on(_get_request_json())

@app.route("/off", methods=["GET", "POST"])
def off():
    return main.off(_get_request_json())

@app.route("/set", methods=["GET", "POST"])
def set():
    return main.set(_get_request_json())

@app.route("/get_status", methods=["GET", "POST"])
def get_status():
    return main.get_status(_get_request_json())

@app.route("/get_latest", methods=["GET", "POST"])
def get_latest():
    return main.get_latest(_get_request_json())

@app.route("/get_latest_span", methods=["GET", "POST"])
def get_latest_span():
    return main.get_latest_span(_get_request_json())


def _get_request_json():
    """GET/POST両方に対応した形式でリクエストデータを変換します。

    Returns:
        list: リクエストデータ
    """
    if request.method == "POST":
        return request.json
    else:
        return request.args


if __name__ == "__main__":
    app.run(
        debug=False,
        host="0.0.0.0",
        port=8080
    )
