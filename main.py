# sistema de autenticação de usuário e senha.
import sqlite3
import smtplib
from dotenv import load_dotenv

load_dotenv()

db = sqlite3.connect('users.db')

def create_table():
    cursor = db.cursor()
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS users(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT NOT NULL UNIQUE,
    #         password TEXT NOT NULL
    #     )
    # ''')

    db.commit()
    print("Tabela 'users' criada com sucesso.")

create_table()

while True:

    print("\n=== Sistema de Autenticação ===")
    print("1. Registrar usuário")
    print("2. Login")
    print("3. Sair")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        def register_user():
            username = input("Digite o nome de usuário: ")
            password = input("Digite a senha: ")
            re_password = input("Digite a senha novamente: ")
            if password != re_password:
                print("As senhas não coincidem.")
                return
            cursor = db.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            print(f"Usuário '{username}' registrado com sucesso.")

        register_user()

    elif choice == '2':
        def notification_email():
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import os

            gmail_user = os.getenv('GMAIL_USER')
            gmail_password = os.getenv('GMAIL_PASSWORD')
            gmail_destino = os.getenv('GMAIL_DESTINO')

            subject = "Recuperação de Senha"
            body = "Instruções para recuperação de senha foram enviadas para o seu e-mail."

            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = gmail_destino
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                text = msg.as_string()
                server.sendmail(gmail_user, gmail_destino, text)
                server.quit()
                print("E-mail de recuperação de senha enviado com sucesso.")
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")

        def login_user():
            attempts = 0
            max_attempts = 3

            while attempts < max_attempts:
                username = input("Digite o nome de usuário: ")
                password = input("Digite a senha: ")

                if not username or not password:
                    print("Nome de usuário e senha não podem estar vazios.")
                    continue

                cursor = db.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user = cursor.fetchone()
                if user:
                    print(f"Bem-vindo, {username}!")
                    return True

                attempts += 1
                print("Nome de usuário ou senha incorretos.")
                if attempts >= max_attempts:
                    print("Você errou sua senha várias vezes. Aguarde e tente novamente mais tarde.")

                    recuperar = input("Deseja recuperar sua senha? (s/n): ")
                    if recuperar.lower() == 's':
                        notification_email()
                        break
                else:
                    print(f"Tentativa {attempts}/{max_attempts}. Tente novamente.")

            return False
        login_user()

    if choice == '3':
        print("Saindo do sistema...")
        break