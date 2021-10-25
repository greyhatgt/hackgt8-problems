import json
import threading
import time
import paramiko
from paramiko.py3compat import b, b2s

SERVER_NAME = 'jeff'
SERVER_USERNAME, SERVER_PASSWORD = 'admin', '1234'

with open('challenge.json') as file:
    challenge = json.load(file)

with open('flag.txt') as file:
    flag = file.read()

class Server(paramiko.ServerInterface):

    def __init__(self, client_address):
        self.event = threading.Event()
        self.client_address = client_address

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == SERVER_USERNAME) and (password == SERVER_PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_exec_request(self, channel, command):
        print(command)
        self.event.set()
        return True


def receive_command(channel, current_directory):
    initial_text = f'{SERVER_USERNAME}@{SERVER_NAME}:{current_directory}$ '
    channel.send(b(initial_text))

    received = ''
    start = time.time()
    while start + 30 > time.time():
        last_received = b2s(channel.recv(1))

        if last_received == chr(13):
            received = received[:-1]
        elif last_received == '\n':
            break
        else:
            received += last_received

    return received


def serve_channel(channel):
    channel.send(b(challenge['entry_text'] + '\n\n'))
    for problem in challenge['problems']:
        channel.send(b('\n' + problem['text'] + '\n'))
        command = receive_command(channel, problem['directory'])
        if command not in problem['answers']:
            channel.send(b(challenge['fail_message'] + '\n\n'))
            break

        if problem['return']:
            channel.send(b(problem['return'] + '\n'))
    else:
        channel.send(b('\n\nCongrats again!!\nHere\'s your flag.\n'))
        channel.send(b(flag + '\n\n'))


    channel.close()
