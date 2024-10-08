import os
from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
import pandas as pd
from google.cloud import bigquery

UPLOAD_FOLDER = os.path.join("files", "uploads")
ALLOWED_EXTENSIONS = {"csv"}
PROJECT_ID = "globant-apescara"
DATASET_ID = "data"

app = Flask(__name__)
app.secret_key = "session secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename) -> bool:
    return "." in filename and filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def uploadFile() -> Response:
    if request.method == "POST":
        # get file in flask
        file = request.files.get("file")
        data_filename = secure_filename(file.filename)

        # Read data in pandas
        try:
            columns = request.form.get("column_names").split(",")
        except:
            columns = None
        data = pd.read_csv(file, header=None, names=columns)
        data.columns = data.columns.astype(
            str
        )  # pyarrow wont work with numbers as column names

        # Upload to BigQuery
        client = bigquery.Client()

        # Set table name
        table_id = request.form.get("table_id")
        table_id = data_filename.split(".")[0] if not table_id else table_id

        # Set data write disposition
        job_config = bigquery.LoadJobConfig()
        write_disposition = request.form.get("write_disposition")
        job_config.write_disposition = (
            "WRITE_APPEND" if not write_disposition else write_disposition
        )

        client.load_table_from_dataframe(
            dataframe=data,
            destination=PROJECT_ID + "." + DATASET_ID + "." + table_id,
            job_config=job_config,
        )

        return jsonify({"message": f"data successfully uploaded to {table_id}"})
    return jsonify({"message": "invalid request"})


if __name__ == "__main__":
    app.run()
