from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Файл для хранения задач
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Загрузка задач из файла"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'todo': [], 'in-progress': [], 'done': []}

def save_tasks(tasks):
    """Сохранение задач в файл"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    if title:
        tasks = load_tasks()
        new_task = {
            'id': len(tasks['todo']) + len(tasks['in-progress']) + len(tasks['done']) + 1,
            'title': title
        }
        tasks['todo'].append(new_task)
        save_tasks(tasks)
    return jsonify(success=True)

@app.route('/move_task', methods=['POST'])
def move_task():
    task_id = int(request.form.get('task_id'))
    from_status = request.form.get('from_status')
    to_status = request.form.get('to_status')

    tasks = load_tasks()

    # Находим задачу
    task = None
    for t in tasks[from_status]:
        if t['id'] == task_id:
            task = t
            break

    if task:
        # Удаляем из старой колонки
        tasks[from_status] = [t for t in tasks[from_status] if t['id'] != task_id]
        # Добавляем в новую колонку
        tasks[to_status].append(task)
        save_tasks(tasks)

    return jsonify(success=True)

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = int(request.form.get('task_id'))
    status = request.form.get('status')

    tasks = load_tasks()
    tasks[status] = [t for t in tasks[status] if t['id'] != task_id]
    save_tasks(tasks)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
