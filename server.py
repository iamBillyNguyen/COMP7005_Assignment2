import argparse
import re
import sys
import socket
import threading

IP = ""
PORT = 0
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024

def parse_arguments():
    global IP, PORT

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server\'s IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server\'s port")

    try:
        args = parser.parse_args()

    except SystemExit as e:
        parser.print_help()
        sys.exit()

    IP = args.ip
    PORT = args.port

def create_socket():
    print("Server - Creating socket")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as e:
        print("Server - Error creating socket: {}".format(e))
        sys.exit()

    return server_socket
    
def bind_socket(server_socket):
    print("Server - Binding socket")
    try:
        server_socket.bind((IP, PORT))

    except socket.error as e:
        print("Server - Error binding socket: {}".format(e))
        sys.exit()

def listen_socket(server_socket):
    print("Server - Listening on {}:{}".format(IP, PORT))
    try:
        server_socket.listen(MAX_CONNECTIONS)

    except socket.error as e:
        print("Server - Error listening socket: {}".format(e))
        sys.exit()

# Threading is fine since no shared preference
def accept_connection(server_socket):
    client_socket = None
    print("Server - Accepting connection")
    while True:
        try:
            client_socket, client_address = server_socket.accept()

        except socket.error as e:
            print("Server - Error accepting connection: {}".format(e))
            client_socket.close()

        threading.Thread(target=handle_client_request, args=(client_socket,)).start()

def handle_client_request(client_socket):
    client_data = ""

    try:
        client_data = client_socket.recv(BUFFER_SIZE).decode("utf-8")

    except socket.error as e:
        print("Server - Error receiving data: {}".format(e))
        client_socket.close()
    print("------------------------------------")
    print("Server - Handling client request:")
    if client_data:
        print(client_data)
        handle_response(client_socket, client_data)
    else:
        print("Server - Client disconnected")

def process_data(client_data):
    return len(re.findall('[a-zA-Z]', client_data))


def handle_response(client_socket, client_data):
    print("Server - Counting alphabets: {}".format(process_data(client_data)))
    count = str(process_data(client_data))
    print("Server - Response:\n{}\n".format(count))
    try:
        client_socket.send(bytes(count, "utf-8"))

    except socket.error as e:
        print("Server - Error sending response: {}".format(e))
        client_socket.close()

if __name__ == '__main__':
    parse_arguments()
    se_socket = create_socket()
    bind_socket(se_socket)
    listen_socket(se_socket)
    accept_connection(se_socket)

    se_socket.close()
