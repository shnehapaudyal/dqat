import uuid
from flask import Flask, render_template, abort, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

import db
import metrics
from entity.dataset import DatasetRecord

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/File'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def upload_dataset():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Then save the file

        record = DatasetRecord(dataset_id=uuid.uuid4(), filename=filename, path=file_path, file_type=file.mimetype,
                               size=file.content_length)
        record.save()

        return record.json(), 200
    return abort(400)


@app.route('/datasets', methods=['GET'])
def get_all_dataset_records():
    page = int(request.args.get('page', 0))
    per_page = int(request.args.get('per_page', 10))

    records, total_records = db.get_all_datasets(page=page, per_page=per_page)

    record_list = [record.json() for record in records]

    return {
        'records': record_list,
        'page': page,
        'size': total_records
    }, 200


@app.route('/dataset/<uuid:dataset_id>', methods=['GET'])
def get_single_dataset_record(dataset_id):
    record = db.read_dataset(dataset_id)

    if not record:
        return {"error": "Dataset not found"}, 404

    return record.json(), 200


@app.route('/dataset/<uuid:dataset_id>/metrics', methods=['GET'])
def get_dataset_metrics(dataset_id):
    dataset_metrics = metrics.get_dataset_metrics(dataset_id)

    if not metrics:
        return {"error": "Dataset not found"}, 404

    return dataset_metrics.json(), 200


if __name__ == '__main__':
    app.run(debug=True)
