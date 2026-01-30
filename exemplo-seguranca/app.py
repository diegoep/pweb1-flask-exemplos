"""
Aplicação Flask - Sistema de Cadastro e Login com Hash SHA-256

Demonstra conceitos de segurança:
- Hash de senhas com SHA-256 + Salt
- Sessões de usuário
- Validação de entrada
- Proteção contra acesso não autorizado
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import Usuario
import secrets

app = Flask(__name__)

# Chave secreta para sessões (em produção, use variável de ambiente)
app.secret_key = secrets.token_hex(32)


@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de novos usuários"""

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')

        # Validações
        if not username or not email or not senha:
            flash('Todos os campos são obrigatórios', 'error')
            return render_template('registro.html')

        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'error')
            return render_template('registro.html')

        # Tenta criar o usuário
        sucesso, mensagem = Usuario.criar_usuario(username, email, senha)

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('login'))
        else:
            flash(mensagem, 'error')

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        senha = request.form.get('senha', '')

        # Validações
        if not username or not senha:
            flash('Usuário e senha são obrigatórios', 'error')
            return render_template('login.html')

        # Tenta autenticar
        sucesso, mensagem = Usuario.autenticar(username, senha)

        if sucesso:
            # Cria sessão do usuário
            session['username'] = username
            flash(mensagem, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(mensagem, 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard do usuário (requer login)"""

    # Verifica se usuário está logado
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página', 'error')
        return redirect(url_for('login'))

    username = session['username']
    usuario = Usuario.obter_usuario(username)

    return render_template('dashboard.html', usuario=usuario)


@app.route('/usuarios')
def listar_usuarios():
    """Lista todos os usuários cadastrados"""

    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página', 'error')
        return redirect(url_for('login'))

    usuarios = Usuario.listar_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    session.pop('username', None)
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('index'))


@app.route('/info-seguranca')
def info_seguranca():
    """Página com informações sobre segurança"""
    return render_template('info_seguranca.html')


if __name__ == '__main__':
    app.run(debug=True)
