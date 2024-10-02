import argparse
import re
import sys
import socket
import threading

SERVER_IP = "0.0.0.0" # All network interfaces (INADDR_ANY)
PORT = 0
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024

# TODO Add client count for logging
# TODO Make sure all errors are handled
# TODO Clean up
# TODO Test with 10 clients concurrently, create a script?

def parse_arguments():
    global PORT
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True, help="Server\'s port")

    try:
        args = parser.parse_args()

    except SystemExit as e:
        parser.print_help()
        sys.exit()

    PORT = args.port

def create_socket():
    print("Creating socket")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server_socket
    
def bind_socket(server_socket, port):
    print("Binding socket")
    server_socket.bind((SERVER_IP, port))

def listen_socket(server_socket):
    print("Listening on {}:{}".format(SERVER_IP, PORT))
    server_socket.listen(MAX_CONNECTIONS)

def accept_connection(server_socket):
    print("Accept connection")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client_request, args=(client_socket,)).start()

def handle_client_request(client_socket):
    client_data = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    print("Client request:")
    if client_data:
        print(client_data)
        handle_response(client_socket, client_data)
    else:
        print("Client disconnected")

def process_data(client_data):
    return len(re.findall('[a-zA-Z]', client_data))

# TODO: Count the letters here
def handle_response(client_socket, client_data):
    print("Count: " + str(process_data(client_data)))
    count = str(process_data(client_data))
    print("Server response:\n{}".format(count))
    client_socket.send(bytes(count, "utf-8"))

if __name__ == '__main__':
    parse_arguments()
    main_socket = create_socket()
    bind_socket(main_socket, PORT)
    listen_socket(main_socket)
    accept_connection(main_socket)

    main_socket.close()