from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
# Configuração da chave secreta para a sessão
app.secret_key = '1234'

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost' # Ou o IP do seu servidor MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbloja'

mysql = MySQL(app)

# Rota para a página de login (página inicial)
@app.route('/')
def login_page():
    return render_template('form-adm.html')

# Rota para o processamento do formulário de login
@app.route('/login', methods=['POST'])
def login():
    # Pega os dados do formulário
    username = request.form['username']
    password = request.form['password']

    # Conecta ao banco de dados e busca o usuário
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    # Verifica se o usuário e a senha estão corretos
    if user:
        # Se as credenciais estiverem corretas, armazena o usuário na sessão
        session['logged_in'] = True
        session['username'] = user[1]  # Assumindo que o nome de usuário está na segunda coluna
        return redirect(url_for('admin_dashboard'))
    else:
        # Se as credenciais estiverem incorretas, redireciona para o login com uma mensagem de erro
        return "Usuário ou senha incorretos. <a href='/'>Tente novamente</a>"

# Rota para a página administrativa
@app.route('/admin')
def admin_dashboard():
    # Verifica se o usuário está logado
    if 'logged_in' in session and session['logged_in']:
        return render_template('adm.html', username=session['username'])
    else:
        # Se não estiver logado, redireciona para a página de login
        return redirect(url_for('login_page'))

# Rota para sair (logout)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)