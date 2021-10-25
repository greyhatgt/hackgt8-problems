import paramiko

import socket
from .connection import create_server, run_server, build_connection_handler
from .sshserver import Server, serve_channel, SERVER_NAME


def main():
    host_key = paramiko.RSAKey.from_private_key_file('rsa_key')
    socket_server = create_server(port=2022)
    connection_handler = build_connection_handler(host_key, Server, SERVER_NAME, serve_channel)
    run_server(socket_server, connection_handler)


if __name__ == '__main__':
    main()
