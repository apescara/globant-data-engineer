import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = os.path.join('files', 'uploads')
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)
app.secret_key = "session secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def uploadFile():
    if request.method == "POST":
        # upload file flask
        f = request.files.get("file")
        data_filename = secure_filename(f.filename)

        # Read data in pandas
        data = pd.read_csv(os.path.join(app.config["UPLOAD_FOLDER"], data_filename))

        return jsonify(data.to_json())
    return jsonify({"message": "invalid request"})

if __name__ == "__main__":
    app.run()
