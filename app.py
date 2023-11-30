from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_USER"] = "sql10666446"
app.config["MYSQL_PASSWORD"] = "yDrdTE5e7c"
app.config["MYSQL_HOST"] = "sql10.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql10666446"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    #diccionario = []
    #nombreColumnas = [column[0] for column in cur.description]
    #for record in data:
        #diccionario.append(dict(zip(nombreColumnas, record)))
    cur.close()
    return render_template('index.html', books=data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    data = cur.fetchone()
    #nombreColumnas = [column[0] for column in cur.description]
    #res = dict(zip(nombreColumnas, data))
    cur.close()
    return render_template('edit.html', book=data)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE books SET title=%s, author=%s WHERE id=%s", (title, author, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
