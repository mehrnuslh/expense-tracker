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

if __name__ == '__main__':
    app.run(debug=True)