from crypt import methods
import imp
from flask import Flask, render_template, url_for, request

from flask_pymongo import PyMongo

from pymongo import ReturnDocument

from bson.objectid import ObjectId

app = Flask(__name__)

mongo = PyMongo()

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/mydb")
todo_db = mongodb_client.db.todos

@app.route('/', methods=['POST', 'GET'])
def index():
    todos = todo_db.find()
    return render_template('index.html', todos = todos)

@app.route('/sus', methods=['POST'])
def index_post():
    todo_items = request.form.get('mm') # name
    print('todo_items = ',todo_items)
    todo_db.insert_one({'title': todo_items, 'body': "todo body"})
    
    todos_all = todo_db.find()
    return render_template('index.html', todos = todos_all)

@app.route('/delete')
def idx_delete():
    todo_db.todos.find_one_and_delete({'title': "todo title", 'body': "todo body"})

@app.route('/complete_todo/<oid>')
def complete_todo(oid):
    todo_item = todo_db.find_one({'_id': ObjectId(oid)})
    print('item = ', todo_item)
    return render_template('compete_item.html', todo = todo_item)

@app.route('/complete_todo_delete/<oid>')
def complete_todo_delete(oid):
    todo_item = todo_db.find_one({'_id': ObjectId(oid)})
    print('item = ', todo_item)
    todo_db.find_one_and_delete({'_id': ObjectId(oid)})
    todos = todo_db.find()
    return render_template('index.html', todos = todos)

@app.route('/complete_todo_update/<oid>')
def complete_todo_update(oid):    
    new_todo_item = request.form.get('umm') # name

    print('new_todo_item = ', new_todo_item)

    todo_db.find_one_and_update({'_id': ObjectId(oid)}, 
            { '$set' : {'title': new_todo_item}},
            return_document= ReturnDocument.AFTER)
    todos = todo_db.find()
    return render_template('index.html', todos = todos)


if __name__ == "__main__":
    app.run(debug=True)