import socket
import json

BROADCAST_PORT = 37020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", BROADCAST_PORT))

print("Aguardando anúncio do servidor...")

data, addr = sock.recvfrom(1024)
msg = data.decode()
name, ip, port = msg.split(";")

print(f"Servidor encontrado: {name} em {ip}:{port}")



HOST = '25.49.7.41'  # coloque aqui o IP da máquina do servidor
PORT = 5000             # Porta TCP do servidor



# Exemplo de consulta
query = "SELECT nome FROM Usuario where id = 4;"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def requestBD(pedido):
    client.sendall(pedido.encode())

    data = client.recv(4096).decode()
    print("Resposta do servidor:", data)
    return json.loads(data)

    client.close()





