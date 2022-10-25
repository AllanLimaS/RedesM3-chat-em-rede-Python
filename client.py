from base64 import decode
import socket
import msvcrt
import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def criptografa(senha,mensagem):
    mensagem = list(mensagem)
    nova_mensagem = ""
    for i in range(len(mensagem)):
        nova_mensagem = nova_mensagem + str(ord(mensagem[i]) * senha) + "-"
        
    return nova_mensagem

def descriptografa(senha,mensagem):
    mensagem = mensagem.split("-")
    nova_mensagem = ""
    for i in range( len(mensagem) - 1):
        nova_mensagem = nova_mensagem + chr( int(int(mensagem[i]) / senha))
    
    return nova_mensagem


senha = 9
server_IP = "127.0.0.1"
server_PORT = 666
print("Entre com seu usuário: ")
my_username = input('> ')
server.connect((server_IP, server_PORT))
server.setblocking(False)
print("Pressione ENTER para digitar ou ESC para sair\n")

server.send(bytes(my_username, encoding="utf-8"))
while True:
    if msvcrt.kbhit():
        key_stroke = msvcrt.getch()
        if key_stroke==b'\x1b':
            server.send(bytes(str(datetime.datetime.now())+"/" +my_username + "/" + "quit", encoding="utf-8"))
            print("Você se desconectou")
            exit()

        if key_stroke==b'\r':
            time = str(datetime.datetime.now()).split(" ")[1].split(".")[0]
            message = input(f'({time}) {"EU"} > ')
            server.send(bytes(str(datetime.datetime.now())+ "/" +my_username + "/" + criptografa(senha,message), encoding="utf-8"))

    try:
        while True:
            data = server.recv(10000).decode("utf-8").split("/")
            print(f'({data[0].split(" ")[1].split(".")[0]}) { data[1]}: { descriptografa(senha,data[2]) }')
            
    except:
        continue

server.close()