from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test_app():
    return jsonify({"message": "test"})

if __name__ == "__main__":
    app.run()