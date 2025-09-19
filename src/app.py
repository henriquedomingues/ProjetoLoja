from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '1234'

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbloja'

mysql = MySQL(app)

# ---------------------- LOGIN ---------------------- #

@app.route('/')
def login_page():
    return render_template('form-adm.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['logged_in'] = True
        session['username'] = user[1]
        return redirect(url_for('admin_dashboard'))
    else:
        return "Usuário ou senha incorretos. <a href='/'>Tente novamente</a>"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login_page'))

# ---------------------- CRUD EBOOKS ---------------------- #

@app.route('/admin')
def admin_dashboard():
    if 'logged_in' in session and session['logged_in']:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tblebooks WHERE status = 1")
        ebooks = cur.fetchall()
        cur.close()
        return render_template('adm.html', username=session['username'], ebooks=ebooks)
    else:
        return redirect(url_for('login_page'))

# Criar novo ebook
@app.route('/add', methods=['POST'])
def add_ebook():
    nome = request.form['nome']
    preco = request.form['preco']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tblebooks (nomeEbook, precoEbook, status) VALUES (%s, %s, 1)", (nome, preco,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin_dashboard'))

# Excluir ebook
@app.route('/delete/<int:id>')
def delete_ebook(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tblebooks SET status = 0 WHERE idEbook = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin_dashboard'))

# Editar (carrega dados no form)
@app.route('/edit/<int:id>')
def edit_ebook(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tblebooks WHERE idEbook = %s", (id,))
    ebook = cur.fetchone()
    cur.close()
    return render_template('edit.html', ebook=ebook)

# Atualizar após edição
@app.route('/update/<int:id>', methods=['POST'])
def update_ebook(id):
    nome = request.form['nome']
    preco = request.form['preco']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE tblebooks SET nomeEbook=%s, precoEbook=%s WHERE idEbook=%s", (nome, preco, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
