from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'tasks.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        conn.commit()

init_db()

# Rotas
@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template('tasks.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html')
    
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        title = request.form['title']
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
            conn.commit()
        return redirect(url_for('index'))
    
    with sqlite3.connect(DATABASE) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        return f"Tarefa com ID {task_id} não encontrada.", 404
    return render_template('edit_task.html', task=task)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)