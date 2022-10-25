from logging import exception
import socket
import select

IP = ""
PORT = 666

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(100)
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):

    try:
        message_length = int(100000)
        return {'data': client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:

        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Conexao de {}:{}, usuario: {}'.format(*client_address, user['data'].decode('utf-8')))
        else:
            message = receive_message(notified_socket)
            user = clients[notified_socket]
            try:
                componentes = message["data"].decode("utf-8").split("/")
                print(componentes)
                if(componentes[2] == "quit"):
                    print('O usuário [{}] se desconectou'.format(clients[notified_socket]['data'].decode('utf-8')))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                else:
                    print(f'({componentes[0].split(" ")[1].split(".")[0]}) {componentes[1]}: {componentes[2]}')
            except Exception as e:
                print("Houve algum problema no servidor: " + str(e))

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(message['data'])

    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)
        del clients[notified_socket]