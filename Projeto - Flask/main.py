# Importação dos módulos e pacotes necessários.
from flask import Flask, render_template, redirect, request, flash
import json
import os

# Configuração do Flask.
app = Flask(__name__)
app.config['SECRET_KEY'] = "SENAI791@PYTHON"

# Rota padrão do website (index).
@app.route("/")
def inicio():

    # Abre a página inicial.
    return render_template("login.html")

# Rota para o login do website.
@app.route("/login")
def login():

    # Abre a página de login.
    return render_template("login.html")

# Rota que valida as informações de login do usuário.
@app.route("/validar-login", methods=['post'])
def validar_login():

    # Recupera as informações do formulário de login.
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    # Acessa o arquivo JSON com os usuários cadastrados.
    with open('data/usuarios.json', 'r', encoding='utf-8') as arquivo:

        # Carrega os usuários em uma variável.
        usuarios = json.load(arquivo)

        # Percorre todos os usuários do arquivo JSON.
        for usuario in usuarios:

            # Verificar se as informações estão corretas.
            if (usuario['cpf'] == cpf and usuario['senha'] == senha):
                return redirect('/listar-usuarios')
           
        # Informa que as informações não conferem.
        flash('As informações não conferem!!!')
        return redirect('/login')

    # Redireciona o usuário para a rota padrão.
    return redirect('/')

# Rota para o cadastro de usuário do website.
@app.route("/usuario")
def usuario():

    # Abre a página de cadastro de usuário.
    return render_template("cadastro-usuario.html")

# Rota que irá cadastrar o usuário no website.
@app.route("/cadastrar-usuario", methods=['post'])
def cadastrar_usuario():

    # Recupera as informações do formulário.
    nome = request.form.get('nome')
    nascimento = request.form.get('nascimento')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Verifica se existe um arquivo com os dados dos usuários.
    if os.path.exists("data/usuarios.json"):

        # Lê o arquivo JSON existente.
        with open("data/usuarios.json", "r", encoding="utf-8") as arquivo:

            # Carrega os dados do arquivo em uma variável.
            usuarios = json.load(arquivo)
    else:

        # Cria uma nova lista, para cadastrar os usuários.
        usuarios = []

    # Laço de repetição que percorre todos os usuários cadastrados.
    for usuario in usuarios:

        # Verifica se o CPF informado já está cadastrado.
        if (usuario['cpf'] == cpf):
            flash("O CPF informado já está cadastrado...")
            return redirect('/login')
    
    # Cria um dicionário com as informações preenchidas no formulário.
    dados = {
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "email": email,
        "senha": senha
    }

    # Adiciona o novo usuário com seus dados.
    usuarios.append(dados)

    # Grava os novos dados no arquivo JSON.
    with open("data/usuarios.json", "w", encoding="utf-8") as arquivo:

        # Salva o arquivo JSON com os novos dados e os formata.
        json.dump(usuarios, arquivo, indent=4)

    # Envia uma mensagem de sucesso na gravação dos dados.
    flash("O usuário foi cadastrado com sucesso!!!")

    # Redireciona para a tela de login, após cadastrar o usuário.
    return redirect('/login')

# Rota que lista os usuários cadastrados.
@app.route("/listar-usuarios")
def listar_usuarios():

    # Abre o arquivo JSON com os usuário cadastrados.
    with open('data/usuarios.json', 'r', encoding='utf-8') as arquivo:

        # Carrega os usuários em uma variável.
        usuarios = json.load(arquivo)

    # Apresenta a listagem de usuários cadastrados.
    return render_template('listagem-usuarios.html', usuarios=usuarios)

# Rota que exibe as informações do usuário para alteração.
@app.route("/exibir-usuario/<string:cpf>")
def exibir_usuario(cpf):

    # Abre o arquivo JSON com os usuários cadastrados.
    with open('data/usuarios.json', 'r', encoding='utf-8') as arquivo:

        # Carrega os usuários em uma variável.
        usuarios = json.load(arquivo)

    # Localiza os dados do usuário a partir do CPF.
    for usuario in usuarios:
        if(usuario['cpf'] == cpf):
            return render_template("edita-usuario.html", usuario=usuario)
        
    # Informa que o usuário não foi encontrado.
    flash('Usuário não encontrado...')
    return redirect("/listar-usuarios")

# Rota que edita os dados do usuário.
@app.route("/editar-usuario/<string:cpf>", methods=['post'])
def editar_usuario(cpf):

    # Recupera os dados do formulário.
    nome = request.form.get('nome')
    nascimento = request.form.get('nascimento')
    email = request.form.get('email')

    # Abre o arquivo JSON com os usuários cadastrados.
    with open('data/usuarios.json', 'r', encoding='utf-8') as arquivo:

        # Carrega os usuários em uma variável.
        usuarios = json.load(arquivo)

    # Identifica o usuário pelo CPF.
    for usuario in usuarios:

        # Altera as informações do usuário.
        if (usuario['cpf'] == cpf):
            usuario['nome'] = nome
            usuario['nascimento'] = nascimento
            usuario['email'] = email
            break

    # Abre o arquivo JSON com os usuários cadastrados.
    with open('data/usuarios.json', 'w', encoding='utf-8') as arquivo:
        
        # Grava as alterações.
        json.dump(usuarios, arquivo, indent=4)

    # Informa que a alteração foi feita com sucesso.
    flash("Usuário alterado com sucesso!!!")
    return redirect("/listar-usuarios")

# Rota que excluí o usuário.
@app.route("/excluir-usuario/<string:cpf>", methods=['get'])
def excluir_usuario(cpf):

    # Abre o arquivo JSON com os usuários cadastrados.
    with open('data/usuarios.json', 'r', encoding='utf-8') as arquivo:

        # Carrega os usuários em uma variável.
        usuarios = json.load(arquivo)

    # Cria um indíce do usuário a ser excluído.
    index_usuario = None

    # Localiza o indíce do usuário a ser excluído.
    for index, usuario in enumerate(usuarios):
        
        # Localiza o usuário pelo CPF.
        if (usuario['cpf'] == cpf):
            index_usuario = index
            break

    # Verifica se existe o indíce e o excluí.
    if (index_usuario is not None):

        # Excluí o conteúdo do índice informado.
        usuarios.pop(index_usuario)

        # Abre o arquivo JSON com os usuários cadastrados.
        with open('data/usuarios.json', 'w', encoding='utf-8') as arquivo:
            
            # Grava as alterações.
            json.dump(usuarios, arquivo, indent=4)

        flash("Usuário excluído com sucesso!!!")
    else:
        flash("Não foi possível excluir o usuário!!!")

    # Apresenta a mensagem na listagem de usuarios.
    return redirect("/listar-usuarios")

# Rota que saí do software.
@app.route("/logout")
def logout():

    # Redireciona o usuário para a rota principal.
    return redirect("/")

# Execução do software.
if __name__ == "__main__":
    app.run(debug=True)