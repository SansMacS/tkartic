import socket
import threading
import json
import random
from typing import List, Dict, Tuple

HOST = '192.168.0.42'
PORT = 5000

# Estado global
clients_lock = threading.Lock()
clients = []  # List[Tuple[socket.socket, io.BufferedRWPair]]
client_names = {}  # Dict[socket.socket, str]

# Armazenamento por fase
initial_messages = {}  # Dict[socket.socket, str]
delivered_to = {}      # Dict[socket.socket, socket.socket] # Quem recebeu de quem na fase msg
images_by_client = {}  # Dict[socket.socket, Dict]          # {"name":..., "data":...}
replies_by_client = {} # Dict[socket.socket, str]

def sock_makefile(conn: socket.socket):
    return conn.makefile('rwb')

def send_json(fw, obj):
    line = (json.dumps(obj) + "\n").encode('utf-8')
    fw.write(line)
    fw.flush()

def recv_json(fr):
    line = fr.readline()
    if not line:
        return None
    return json.loads(line.decode('utf-8'))

def derangement(n: int) -> List[int]:
    """Retorna uma permutação sem pontos fixos (ninguém mapeado para si).
    Tenta até conseguir, falha se n < 2."""
    if n < 2:
        raise ValueError("Derangement requer pelo menos 2 elementos")
    while True:
        perm = list(range(n))
        random.shuffle(perm)
        if all(perm[i] != i for i in range(n)):
            return perm

def broadcast_phase(phase: str, prompt: str = None):
    with clients_lock:
        for conn, f in clients:
            send_json(f, {"type": "phase", "phase": phase, "prompt": prompt or ""})

def deliver_to_mapping(mapping: Dict[socket.socket, socket.socket], payloads: Dict[socket.socket, dict], kind: str):
    """Envia conteúdos conforme o mapeamento (sender -> receiver) com tipo kind."""
    with clients_lock:
        for sender, receiver in mapping.items():
            # Encontra o filewriter do receiver
            for r_conn, r_f in clients:
                if r_conn == receiver:
                    data = payloads.get(sender, {})
                    send_json(r_f, data | {"type": kind, "from": client_names[sender]})
                    break

def wait_collect_messages(kind_expected: str, target_store: dict):
    """Coleta de todos os clientes uma mensagem do tipo kind_expected e guarda em target_store."""
    pending = []
    with clients_lock:
        for conn, f in clients:
            pending.append((conn, f))

    received = set()
    while len(received) < len(pending):
        for conn, f in pending:
            if conn in received:
                continue
            obj = recv_json(f)
            if obj is None:
                continue
            if obj.get("type") == kind_expected:
                target_store[conn] = obj.get("text") or obj  # para imagem guardamos obj inteiro
                received.add(conn)
            elif obj.get("type") == "ping":
                send_json(f, {"type": "pong"})
            elif obj.get("type") == "bye":
                # Opcional: tratar saída
                pass

def wait_collect_images(kind_expected: str, target_store: dict):
    pending = []
    with clients_lock:
        for conn, f in clients:
            pending.append((conn, f))
    received = set()
    while len(received) < len(pending):
        for conn, f in pending:
            if conn in received:
                continue
            obj = recv_json(f)
            if obj is None:
                continue
            if obj.get("type") == kind_expected:
                # valida campos mínimos
                name = obj.get("name") or "imagem.png"
                data = obj.get("data") or ""
                target_store[conn] = {"name": name, "data": data}
                received.add(conn)

def compute_derangement_mapping() -> Dict[socket.socket, socket.socket]:
    """Cria um mapeamento sender->receiver garantindo receiver != sender."""
    with clients_lock:
        entries = [conn for conn, _ in clients]
        idx_map = {entries[i]: i for i in range(len(entries))}
        perm = derangement(len(entries))
        mapping = {}
        for i, conn in enumerate(entries):
            receiver = entries[perm[i]]
            mapping[conn] = receiver
        return mapping

def game_loop():
    # Fase 1: pedir mensagens iniciais
    broadcast_phase("initial_msg", "Escreva sua mensagem inicial para começar a partida.")
    wait_collect_messages("msg", initial_messages)

    # Redistribuição das mensagens iniciais (derangement)
    msg_payloads = {}
    with clients_lock:
        for conn, f in clients:
            msg_text = initial_messages.get(conn, "")
            msg_payloads[conn] = {"type": "deliver_msg", "text": msg_text}
    mapping = compute_derangement_mapping()
    # Guardamos quem recebeu de quem (para referência futura)
    global delivered_to
    delivered_to = mapping.copy()
    deliver_to_mapping(mapping, msg_payloads, "deliver_msg")

    # Fase 2: pedir imagens relacionadas à mensagem recebida
    broadcast_phase("send_image", "Envie uma imagem relacionada à mensagem recebida (arquivo local).")
    wait_collect_images("img", images_by_client)

    # Redistribuição das imagens (derangement)
    img_payloads = {}
    with clients_lock:
        for conn, f in clients:
            img = images_by_client.get(conn, {"name": "imagem.png", "data": ""})
            img_payloads[conn] = {"type": "deliver_img", "name": img["name"], "data": img["data"]}
    mapping2 = compute_derangement_mapping()
    deliver_to_mapping(mapping2, img_payloads, "deliver_img")

    # Fase 3: pedir resposta em texto relacionada à imagem recebida
    broadcast_phase("reply_msg", "Escreva uma mensagem relacionada à imagem que você recebeu.")
    wait_collect_messages("msg_reply", replies_by_client)

    # Redistribuição das respostas (derangement)
    reply_payloads = {}
    with clients_lock:
        for conn, f in clients:
            txt = replies_by_client.get(conn, "")
            reply_payloads[conn] = {"type": "deliver_reply", "text": txt}
    mapping3 = compute_derangement_mapping()
    deliver_to_mapping(mapping3, reply_payloads, "deliver_reply")

    # Critério de término simples: todos receberam pelo menos uma mensagem e uma imagem nesta rodada
    with clients_lock:
        for conn, f in clients:
            send_json(f, {"type": "end", "reason": "Rodada concluída. Todos receberam conteúdo."})

def client_thread(conn: socket.socket, addr):
    frw = sock_makefile(conn)
    # Espera hello com nome
    hello = recv_json(frw)
    if not hello or hello.get("type") != "hello" or not hello.get("name"):
        frw.close()
        conn.close()
        return
    name = hello["name"]
    with clients_lock:
        clients.append((conn, frw))
        client_names[conn] = name
    print(f"[+] {name} conectado de {addr}")

    # Mantém thread viva até o fim do jogo; o game_loop é disparado pelo main quando houver clientes suficientes
    # Aqui apenas aguarda eventos; as leituras são feitas nas funções de coleta.

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")
    print("Aguardando pelo menos 2 clientes...")

    # Aceitação de clientes em paralelo
    threading.Thread(target=accept_loop, args=(server,), daemon=True).start()

    # Espera pelo mínimo de clientes e inicia o jogo
    while True:
        with clients_lock:
            count = len(clients)
        if count >= 2:
            print(f"Iniciando partida com {count} clientes.")
            game_loop()
            break

    print("Encerrando servidor.")
    server.close()

def accept_loop(server):
    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=client_thread, args=(conn, addr), daemon=True)
            t.start()
        except Exception as e:
            break

if __name__ == "__main__":
    main()