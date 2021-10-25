import _thread as thread
import socket

import paramiko


def create_server(address=None, port=8080):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind((address if address else '', port))
    socket_server.listen(100)
    return socket_server


def build_connection_handler(host_key, server_class, server_name, channel_server):
    def handle_connection(client, address):
        transport = paramiko.Transport(client)

        transport.set_gss_host(server_name)
        transport.load_server_moduli()

        transport.add_server_key(host_key)
        server = server_class(address)
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            print(f'ssh negotiation failed with {address}')
            raise

        channel = transport.accept(20)
        channel.settimeout(30)
        if channel is None:
            print(f'no channel for {address}')
            raise
        print(f'authenticated {address}')

        server.event.wait(10)
        if not server.event.is_set():
            print(f'{address} never asked for shell')
            raise

        channel_server(channel)

    return handle_connection


def run_server(socket_server, connection_handler):
    while True:
        try:
            client_socket, client_address = socket_server.accept()
            thread.start_new_thread(connection_handler, (client_socket, client_address))
        except Exception as e:
            print(f'Error: {str(e)}')
