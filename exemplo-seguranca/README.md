# Sistema de Cadastro e Login com Hash SHA-256

## 📋 Descrição

Este é um projeto didático em Flask que demonstra conceitos fundamentais de segurança em aplicações web, com foco em **autenticação de usuários** e **hash de senhas usando SHA-256**.

### ⚠️ IMPORTANTE

Este projeto usa SHA-256 para fins **educacionais** e de **demonstração**. Em ambientes de produção, use algoritmos projetados especificamente para hash de senhas como:
- **bcrypt** (recomendado)
- **Argon2** (estado da arte)
- **PBKDF2** (padrão NIST)

## 🎯 Objetivos de Aprendizado

Este projeto demonstra:

1. **Hash de Senhas**: Como usar SHA-256 para criar hashes de senhas
2. **Salt**: Implementação de salt único por usuário
3. **Autenticação**: Verificação de credenciais de forma segura
4. **Sessões**: Gerenciamento de sessões de usuário
5. **Proteção de Rotas**: Restrição de acesso a páginas protegidas
6. **Validação**: Validação básica de entrada de dados

## 🔐 Conceitos de Segurança

### Hash SHA-256

SHA-256 (Secure Hash Algorithm 256-bit) é uma função hash criptográfica que:
- Gera uma saída de 256 bits (64 caracteres hexadecimais)
- É determinística (mesma entrada = mesma saída)
- É unidirecional (não pode ser revertida)
- Qualquer mudança mínima na entrada muda completamente o hash

### Salt

O **salt** é um valor aleatório único adicionado à senha antes do hash:

```python
senha_original = "senha123"
salt = "a3f9d8c7b2e1..."  # 32 bytes aleatórios
senha_com_salt = senha_original + salt
hash_final = sha256(senha_com_salt)
```

**Benefícios:**
- Previne **rainbow table attacks**
- Garante que senhas iguais tenham hashes diferentes
- Aumenta significativamente a segurança

### Processo de Autenticação

**Registro:**
1. Usuário fornece senha
2. Sistema gera salt aleatório
3. Combina senha + salt
4. Aplica SHA-256
5. Armazena hash e salt (não a senha original)

**Login:**
1. Usuário fornece senha
2. Sistema recupera salt do banco de dados
3. Combina senha fornecida + salt
4. Aplica SHA-256
5. Compara com hash armazenado
6. Se idênticos, autenticação bem-sucedida

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone ou baixe este projeto

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: `http://127.0.0.1:5000`

## 📁 Estrutura do Projeto

```
exemplo-seguranca/
│
├── app.py                 # Aplicação Flask principal
├── models.py             # Modelo de usuário com hash SHA-256
├── requirements.txt      # Dependências do projeto
├── README.md            # Este arquivo
│
├── templates/           # Templates HTML
│   ├── base.html       # Template base
│   ├── index.html      # Página inicial
│   ├── registro.html   # Formulário de registro
│   ├── login.html      # Formulário de login
│   ├── dashboard.html  # Dashboard do usuário
│   ├── usuarios.html   # Lista de usuários
│   └── info_seguranca.html  # Informações sobre segurança
│
└── static/             # Arquivos estáticos
    └── css/
        └── style.css   # Estilos da aplicação
```

## 🎨 Funcionalidades

### 1. Registro de Usuário
- Formulário de cadastro com validação
- Senhas com mínimo de 6 caracteres
- Confirmação de senha
- Geração automática de salt
- Hash SHA-256 da senha

### 2. Login
- Autenticação de credenciais
- Criação de sessão
- Mensagens de erro informativas

### 3. Dashboard
- Área protegida (requer login)
- Exibe informações do usuário
- **Visualização educacional** do hash e salt (apenas para fins didáticos)

### 4. Lista de Usuários
- Exibe todos os usuários cadastrados
- Protegido por autenticação

### 5. Informações de Segurança
- Explicações detalhadas sobre hash
- Comparação de algoritmos
- Melhores práticas

## 💡 Código Importante

### Hash de Senha (models.py)

```python
import hashlib
import os

def gerar_salt():
    return os.urandom(32).hex()

def hash_senha(senha, salt):
    senha_com_salt = senha + salt
    return hashlib.sha256(senha_com_salt.encode('utf-8')).hexdigest()
```

### Criação de Usuário

```python
salt = gerar_salt()
senha_hash = hash_senha(senha_plana, salt)
# Armazena apenas senha_hash e salt, nunca a senha original
```

### Autenticação

```python
usuario = obter_usuario(username)
senha_hash_tentativa = hash_senha(senha_fornecida, usuario.salt)
if senha_hash_tentativa == usuario.senha_hash:
    # Login bem-sucedido
```

## ⚠️ Limitações do SHA-256 para Senhas

1. **Muito Rápido**: Facilita ataques de força bruta
   - Hardware moderno pode calcular bilhões de hashes SHA-256 por segundo
   - GPUs e ASICs tornam ataques de força bruta viáveis

2. **Sem Cost Factor**: Não pode ser ajustado para ficar mais lento
   - bcrypt/argon2 permitem aumentar o custo computacional
   - Protege contra melhorias de hardware

3. **Projetado para Integridade, não Senhas**:
   - SHA-256 foi criado para verificação de integridade
   - Algoritmos como bcrypt foram criados especificamente para senhas

## ✅ Melhores Práticas para Produção

### Use bcrypt

```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Hash
senha_hash = bcrypt.generate_password_hash('senha123')

# Verificar
if bcrypt.check_password_hash(senha_hash, 'senha123'):
    # Login bem-sucedido
```

### Outras Recomendações

1. **Nunca armazene senhas em texto plano**
2. **Use HTTPS** para todas as comunicações
3. **Implemente rate limiting** para prevenir força bruta
4. **Use autenticação de dois fatores (2FA)**
5. **Valide e sanitize** todas as entradas do usuário
6. **Implemente política de senhas fortes**
7. **Use bibliotecas testadas** (não reimplemente criptografia)

## 📚 Recursos Adicionais

### Documentação
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [SHA-2 (Wikipedia)](https://en.wikipedia.org/wiki/SHA-2)

### Bibliotecas Recomendadas
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- [Argon2-cffi](https://argon2-cffi.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)

## 🧪 Testando o Sistema

1. Acesse `http://127.0.0.1:5000`
2. Clique em "Registrar" e crie uma conta
3. Observe que a senha não é armazenada em texto plano
4. Faça login com as credenciais criadas
5. No dashboard, veja o hash SHA-256 da sua senha
6. Experimente criar múltiplos usuários com a mesma senha
7. Observe que cada um terá um hash diferente (graças ao salt)

## 📝 Exercícios Propostos

1. **Tente implementar bcrypt** no lugar do SHA-256
2. **Adicione requisitos de senha forte** (maiúsculas, números, caracteres especiais)
3. **Implemente "Esqueci minha senha"** com token de redefinição
4. **Adicione validação de email** com link de confirmação
5. **Implemente rate limiting** para prevenir ataques de força bruta
6. **Adicione logging** de tentativas de login
7. **Crie testes unitários** para as funções de hash

## 👨‍🏫 Para Educadores

Este projeto pode ser usado para ensinar:

- Fundamentos de autenticação web
- Diferença entre criptografia e hash
- Importância de algoritmos adequados
- Conceitos de salt e rainbow tables
- Sessões e cookies em aplicações web
- Proteção de rotas e autorização
- Validação de entrada

## 📄 Licença

Este projeto é de uso educacional e livre para modificação e distribuição.

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Este é um projeto didático e pode ser expandido de várias formas.

---

**Desenvolvido para fins educacionais - IFPB**
