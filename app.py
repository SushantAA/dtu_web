from flask import Flask, render_template, url_for

from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo()
mongo.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/sus', methods=['POST', 'PUT'])
def index_post():
    return "post done"


if __name__ == "__main__":
    app.run(debug=True)