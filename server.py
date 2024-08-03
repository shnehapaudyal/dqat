import flask
from flask_cors import CORS

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/File'
app.config['UPLOAD_BUCKET'] = 'dqaat-858c4cdd-d3af-4844-99a1-3fb036cf77a6-upload'

CORS(app)


request = flask.request
