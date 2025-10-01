import socket

# Configuração do cliente
HOST = '127.0.0.1'  # IP do servidor (localhost para teste)
PORT = 5000         # Porta do servidor

# Cria o socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Pede o nome do usuário
nome = input("Digite seu nome de usuário: ")

# Envia o nome para o servidor
client_socket.sendall(nome.encode("utf-8"))

# Recebe resposta do servidor
mensagem = client_socket.recv(1024).decode("utf-8")
print("Servidor:", mensagem)

client_socket.close()