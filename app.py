from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

# Database configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Change this to your MySQL password
app.config['MYSQL_DB'] = 'notes_app'

mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM notes")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', notes=data)

@app.route('/add_note', methods=['POST'])
def add_note():
    content = request.form['content']
    cur = mysql.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s)", [content])
    mysql.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:id>', methods=['GET'])
def delete_note(id):
    cur = mysql.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", [id])
    mysql.commit()
    cur.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
