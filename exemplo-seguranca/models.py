"""
Modelo de Usuário com Hash SHA-256

IMPORTANTE: Este exemplo usa SHA-256 para fins DIDÁTICOS.
Em produção, use bcrypt, argon2 ou PBKDF2 que são algoritmos
projetados especificamente para hash de senhas.

Problemas do SHA-256 para senhas:
1. Muito rápido - facilita ataques de força bruta
2. Sem "salt" automático - vulnerável a rainbow tables
3. Não tem "cost factor" ajustável
"""

import hashlib
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    """Classe para gerenciar usuários no sistema"""

    # Simulando um banco de dados em memória
    usuarios_db = {}

    def __init__(self, username, email, senha_hash, salt):
        self.username = username
        self.email = email
        self.senha_hash = senha_hash
        self.salt = salt
        self.criado_em = datetime.now()

    @staticmethod
    def gerar_salt():
        """
        Gera um salt aleatório de 32 bytes

        O salt é importante para:
        - Prevenir rainbow table attacks
        - Garantir que senhas iguais tenham hashes diferentes
        """
        return os.urandom(32).hex()

    @staticmethod
    def hash_senha(senha, salt):
        """
        Cria hash SHA-256 da senha com salt

        Args:
            senha (str): Senha em texto plano
            salt (str): Salt único para este usuário

        Returns:
            str: Hash hexadecimal da senha
        """
        # Combina senha + salt antes de fazer hash
        # senha_com_salt = senha + salt
        # return hashlib.sha256(senha_com_salt.encode('utf-8')).hexdigest()
        return generate_password_hash(senha, method='pbkdf2:sha256', salt_length=32)

    @classmethod
    def criar_usuario(cls, username, email, senha):
        """
        Cria um novo usuário no sistema

        Args:
            username (str): Nome de usuário
            email (str): Email do usuário
            senha (str): Senha em texto plano

        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        # Validações
        if username in cls.usuarios_db:
            return False, "Usuário já existe"

        if len(senha) < 6:
            return False, "Senha deve ter no mínimo 6 caracteres"

        # Gera salt único para este usuário
        salt = cls.gerar_salt()

        # Cria hash da senha
        senha_hash = cls.hash_senha(senha, salt)

        # Cria e armazena o usuário
        usuario = cls(username, email, senha_hash, salt)
        cls.usuarios_db[username] = usuario

        return True, "Usuário criado com sucesso"

    @classmethod
    def autenticar(cls, username, senha):
        """
        Autentica um usuário

        Args:
            username (str): Nome de usuário
            senha (str): Senha em texto plano

        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        # Verifica se usuário existe
        if username not in cls.usuarios_db:
            return False, "Usuário ou senha inválidos"

        usuario = cls.usuarios_db[username]

        # Calcula hash da senha fornecida com o salt do usuário
        # senha_hash_tentativa = cls.hash_senha(senha, usuario.salt)

        # Compara os hashes
        # if senha_hash_tentativa == usuario.senha_hash:
        if check_password_hash(usuario.senha_hash, senha):
            return True, "Login realizado com sucesso"
        else:
            return False, "Usuário ou senha inválidos"

    @classmethod
    def obter_usuario(cls, username):
        """Retorna um usuário pelo username"""
        return cls.usuarios_db.get(username)

    @classmethod
    def listar_usuarios(cls):
        """Lista todos os usuários (sem senhas)"""
        return [
            {
                'username': u.username,
                'email': u.email,
                'criado_em': u.criado_em.strftime('%d/%m/%Y %H:%M:%S')
            }
            for u in cls.usuarios_db.values()
        ]
