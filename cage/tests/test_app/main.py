from flask import Flask
import os
app = Flask(__name__)


@app.route("/")
def hello_world():
        return os.environ["AVAR"]


@app.route("/main")
def main():
    return "This is a test app running in the Python cage"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))
