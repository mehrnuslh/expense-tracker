from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

@app.route('/')
def home():
    expenses = get_expenses()
    return render_template('index.html', expenses=expenses)

from flask import Flask, render_template, request, redirect

# ... keep your existing get_expenses() function ...

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form['name']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)',
        (name, amount, category, date)
    )
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE id = ?', (id,))
    expense = cursor.fetchone()
    conn.close()
    return render_template('edit.html', expense=expense)

@app.route('/update/<int:id>', methods=['POST'])
def update_expense(id):
    name = request.form['name']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE expenses SET name=?, amount=?, category=?, date=? WHERE id=?',
        (name, amount, category, date, id)
    )
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

