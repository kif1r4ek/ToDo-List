from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "description": "Study Flask framework"},
    {"id": 2, "title": "Build a REST API", "description": "Create a simple REST API"}
]

def find_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    return task[0] if task else None

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):

    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"})

    return jsonify(task)
@app.route('/tasks', methods=['POST'])
def create_task():

    if "title" not in request.json and "description" not in request.json:
        abort(400)

    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json['title'],
        "description": request.json['description']
    }
    tasks.append(new_task)

    return jsonify(new_task)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not request.json:
        abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    tasks.remove(task)
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
