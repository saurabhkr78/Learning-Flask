from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

todos = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.json.get('task')
    if task:
        todo = {'id': next_id, 'task': task}
        todos.append(todo)
        next_id += 1
        return jsonify({'success': True, 'id': todo['id']})
    return jsonify({'success': False})

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({'todos': todos})

@app.route('/edit/<int:todo_id>', methods=['PUT'])
def edit_todo(todo_id):
    task = request.json.get('task')
    for todo in todos:
        if todo['id'] == todo_id:
            todo['task'] = task
            return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
