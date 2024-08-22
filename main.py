import logging
import uuid

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

import datasets
import db
import issues
from files import *
import domain
import metrics
from entity.dataset import DatasetRecord
from nltk_utils import download_nltk
from server import app, request

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

download_nltk()


def dataframe(dataset_id):
    dataset_record = datasets.get_dataset(dataset_id)
    return files.read(dataset_record.path)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def upload_dataset():
    file = request.files['File']  # First grab the file
    filename = secure_filename(file.filename)
    size, path = files.save(file, filename)

    # Save the dataset record to the database
    record = DatasetRecord(dataset_id=str(uuid.uuid4()), filename=filename, path=path, file_type=file.mimetype,
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
    df = files.read(record.path)
    result['overall_score'] = metrics.calculate_overall_score(df)

    return result, 200


@app.route('/dataset/<string:dataset_id>/tags', methods=['GET'])
def get_dataset_tags(dataset_id):
    df = dataframe(dataset_id)
    tags = datasets.get_tags(df)

    return tags, 200


@app.route('/dataset/<string:dataset_id>/metrics', methods=['GET'])
def get_dataset_metrics(dataset_id):
    df = dataframe(dataset_id)
    dataset_metrics = metrics.get_dataset_metrics(df)

    if not domain:
        return {"error": "Dataset not found"}, 404

    return dataset_metrics, 200


@app.route('/dataset/<string:dataset_id>/estimate/metrics', methods=['GET'])
def get_dataset_metrics_estimation(dataset_id):
    df = dataframe(dataset_id)
    dataset_metrics = metrics.get_metrics_estimate(df)

    if not domain:
        return {"error": "Dataset not found"}, 404

    return dataset_metrics, 200


@app.route('/dataset/<string:dataset_id>/metrics/readability', methods=['GET'])
def get_dataset_readability(dataset_id):
    df = dataframe(dataset_id)
    dataset_metrics = metrics.get_readability(df)

    return dataset_metrics, 200


@app.route('/dataset/<string:dataset_id>/overall_rating', methods=['GET'])
def get_dataset_rating(dataset_id):
    df = dataframe(dataset_id)
    dataset_metrics = metrics.calculate_overall_score(df)

    if not dataset_metrics:
        return {"error": "Dataset not found"}, 404

    return {'rating': dataset_metrics}, 200


@app.route('/dataset/<string:dataset_id>/data', methods=['GET'])
def get_dataset_data(dataset_id):
    df = dataframe(dataset_id)

    return df.to_json(orient='records'), 200


@app.route('/dataset/<string:dataset_id>/issues', methods=['GET'])
def get_dataset_issues(dataset_id):
    # TODO: Implement data validation and quality checks
    pass


@app.route('/dataset/<string:dataset_id>/stats', methods=['GET'])
def get_statistics(dataset_id):
    df = dataframe(dataset_id)
    statistics = (datasets.statistics(df))  # Assuming definemetrics has a get_statistics function

    if not statistics:
        return {"error": "Statistics not found"}, 404

    return statistics, 200


@app.route('/dataset/<string:dataset_id>/types', methods=['GET'])
def get_datatypes(dataset_id):
    df = dataframe(dataset_id)
    datatype = datasets.get_datatypes(df)  # Assuming definemetrics has a get_datatypes function

    if datatype is None:
        return {"error": "Datatype not found"}, 404

    return datatype.to_dict(orient='records'), 200


@app.route('/issues', methods=['GET'])
def get_issues_list():
    return issues.get_issues_list()


@app.route('/dataset/<string:dataset_id>/issues/missing_values', methods=['GET'])
def get_missingvalue(dataset_id):
    df = dataframe(dataset_id)
    datatype = (metrics.get_missingvalue(df))  # Assuming definemetrics has a get_missing valuefunction

    if not datatype:
        return {"error": "Missing value not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/issues/inconsistency', methods=['GET'])
def get_inconsistent_datatype(dataset_id):
    df = dataframe(dataset_id)
    datatype = (metrics.get_inconsistent_datatype(df))

    if not datatype:
        return {"error": "Inconsistent datatype not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/issues/outliers', methods=['GET'])
def get_outlier(dataset_id):
    df = dataframe(dataset_id)
    datatype = (metrics.get_outlier(df))  # Assuming definemetrics has a get_outlier value function

    if not datatype:
        return {"error": "Missing value not found"}, 404

    return datatype, 200


@app.route('/dataset/<string:dataset_id>/issues/typo', methods=['GET'])
def get_typos(dataset_id):
    df = dataframe(dataset_id)
    typos = (metrics.get_typos(df))  # Assuming definemetrics has a get_typos value function

    if not typos:
        return {"error": "Typos not found"}, 404

    return typos, 200


@app.route('/dataset/<string:dataset_id>/issues/invalid_format', methods=['GET'])
def get_formats(dataset_id):
    df = dataframe(dataset_id)
    formats = (metrics.get_invalid_formats(df))
    if not formats:
        return {"error": "Formats not found"}, 404

    return formats, 200


issues


@app.route('/dataset/<string:dataset_id>/issues/duplicate', methods=['GET'])
def get_duplicate(dataset_id):
    df = dataframe(dataset_id)
    duplicate = (metrics.get_duplicate(df))

    if not duplicate:
        return {"error": "Duplicate rows not found"}, 404

    return duplicate, 200


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
