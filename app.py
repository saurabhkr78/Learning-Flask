from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    timer = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'timer': self.timer
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify({'todos': [todo.to_dict() for todo in todos]})

@app.route('/add', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = Todo(task=data['task'], timer=data['timer'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'success': True, 'id': new_todo.id})

@app.route('/edit/<int:id>', methods=['PUT'])
def edit_todo(id):
    data = request.json
    todo = Todo.query.get(id)
    if todo:
        todo.task = data['task']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
