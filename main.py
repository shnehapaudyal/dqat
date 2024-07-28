import logging
import uuid

import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

import datasets
import db
import metrics
from entity.dataset import DatasetRecord

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/File'

CORS(app)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def upload_dataset():
    file = request.files['File']  # First grab the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Then save the file
    size = os.stat(file_path).st_size

    # Save the dataset record to the database
    record = DatasetRecord(dataset_id=str(uuid.uuid4()), filename=filename, path=file_path, file_type=file.mimetype,
                           size=size)
    print(record.json())
    record.save()
    print('saved')

    return record.json(), 200


@app.route('/datasets', methods=['GET'])
def get_all_dataset_records():
    page = int(request.args.get('page', 0))
    per_page = int(request.args.get('per_page', 10))

    records = db.get_all_datasets(page=page, per_page=per_page)

    record_list = [record.json() for record in records]

    return {
        'records': record_list,
        'page': page + 1,
        'size': len(record_list),
    }, 200


@app.route('/dataset/<string:dataset_id>', methods=['GET'])
def get_single_dataset_record(dataset_id):
    record = db.read_dataset(dataset_id)

    if not record:
        return {"error": "Dataset not found"}, 404

    result = record.json()
    result['overall_score'] = metrics.calculate_overall_score(dataset_id)

    return result, 200


@app.route('/dataset/<string:dataset_id>/metrics', methods=['GET'])
def get_dataset_metrics(dataset_id):
    dataset_metrics = metrics.get_dataset_metrics(dataset_id)

    if not metrics:
        return {"error": "Dataset not found"}, 404

    return dataset_metrics, 200


@app.route('/dataset/<string:dataset_id>/overall_rating', methods=['GET'])
def get_dataset_rating(dataset_id):
    dataset_metrics = metrics.calculate_overall_score(dataset_id)

    if not metrics:
        return {"error": "Dataset not found"}, 404

    return {'rating': dataset_metrics}, 200


@app.route('/dataset/<string:dataset_id>/data', methods=['GET'])
def get_dataset_data(dataset_id):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Calculate start and end indices for pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)

    return df.to_json(orient='records'), 200


@app.route('/dataset/<string:dataset_id>/issues', methods=['GET'])
def get_dataset_issues(dataset_id):
    # TODO: Implement data validation and quality checks
    pass


@app.route('/dataset/<string:dataset_id>/stats', methods=['GET'])
def get_statistics(dataset_id):
    statistics = (datasets.get_statistics(dataset_id))  # Assuming definemetrics has a get_statistics function

    if not statistics:
        return {"error": "Statistics not found"}, 404

    return statistics, 200


@app.route('/dataset/<string:dataset_id>/types', methods=['GET'])
def get_datatypes(dataset_id):
    datatype = (datasets.get_datatypes(dataset_id))  # Assuming definemetrics has a get_datatypes function

    if not datatype:
        return {"error": "Datatype not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/missing', methods=['GET'])
def get_missingvalue(dataset_id):
    datatype = (datasets.get_missingvalue(dataset_id))  # Assuming definemetrics has a get_missing valuefunction

    if not datatype:
        return {"error": "Missing value not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/datatypeproblem', methods=['GET'])
def get_inconsistent_datatype(dataset_id):
    datatype = (datasets.get_inconsistent_datatype(dataset_id))

    if not datatype:
        return {"error": "Inconsistent datatype not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/outlier', methods=['GET'])
def get_outlier(dataset_id):
    datatype = (datasets.get_outlier(dataset_id))  # Assuming definemetrics has a get_outlier value function

    if not datatype:
        return {"error": "Missing value not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/typos', methods=['GET'])
def get_typos(dataset_id):
    typos = (datasets.get_typos(dataset_id))  # Assuming definemetrics has a get_typos value function

    if not typos:
        return {"error": "Typos not found"}, 404

    return typos, 200


if __name__ == '__main__':
    app.run(debug=True)
