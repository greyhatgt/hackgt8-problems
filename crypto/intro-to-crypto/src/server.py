import json
import socket
from _thread import *

flag = 'hackgt8{h0p3_tO_c4ES4r_yOU_1At3r_6169bb7d715857}'

with open('challenge.json') as file:
    challenge = json.load(file)

ServerSideSocket = socket.socket()
host = '0.0.0.0'
port = 2111
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def recv_until(connection, text):
    result = ""
    c = connection.recv(1).decode('utf-8')
    while c != text:
        result += c
        c = connection.recv(1).decode('utf-8')
    return result


def multi_threaded_client(connection):
    connection.send(str.encode(challenge['welcome_text']))
    for problem in challenge['problems']:
        connection.send(f'\n\n{problem["text"]}\n'.encode())
        connection.send(f'ciphertext: {problem["ciphertext"]}\n'.encode())
        connection.send(f'plaintext: '.encode())
        answer = recv_until(connection, '\n')
        if answer == problem['answer']:
            connection.send(f'{problem["correct"]}\n'.encode())
        else:
            connection.send(f'{problem["wrong"]}\n'.encode())
            break
    else:
        connection.send(f'\n\nGood job! Here\'s your flag.\nflag: {flag}'.encode())
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
