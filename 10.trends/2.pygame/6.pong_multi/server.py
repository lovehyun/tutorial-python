import socket
import threading

# 서버 설정
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(2)
print("Server started, waiting for players...")

clients = []

# 클라이언트 핸들러 함수
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            break

# 모든 클라이언트에 메시지 브로드캐스트
def broadcast(message, exclude_socket):
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

# 클라이언트 연결 수락
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Player connected from {client_address}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
