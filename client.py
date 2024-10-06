import argparse
import sys
import socket

IP = ""
PORT = 0
FILE = ""
BUFFER_SIZE = 1024

def parse_arguments():
    global IP, PORT, FILE
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server\'s IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server\'s port")
    parser.add_argument("-f", "--file", type=str, required=True, help="Client\'s input file")

    try:
        args = parser.parse_args()

    except SystemExit as e:
        parser.print_help()
        sys.exit()

    IP = args.ip
    PORT = args.port
    FILE = args.file

def create_socket():
    print("Client - Creating socket...")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as e:
        print("Client - Error creating socket: {}".format(e))
        sys.exit()

    return client_socket

def connect_socket(client_socket):
    print("Client - Connecting to server socket at {}:{}...".format(IP, PORT))
    try:
        client_socket.connect((IP, PORT))

    except socket.error as e:
        print("Client - Error connecting to server: {}".format(e))
        client_socket.close()
        sys.exit()

def handle_request(client_socket):
    print("------------------------------------")
    print("Client - Request:")
    while True:
        try:
            file = open(FILE, "r")
            data = file.read()
            print(data)

            if not data:
                print("Client - Empty file")
                data = "\0"

            if len(data) > BUFFER_SIZE:
                print("Client - Error file is longer than 1024 characters")
                client_socket.close()
                sys.exit()

            while data:
                try:
                    client_socket.send(bytes(data, encoding="utf-8"))

                except socket.error as e:
                    print("Client - Error sending data: {}".format(e))
                    client_socket.close()
                    sys.exit()

                data = file.read()

            file.close()

        except IOError as e:
            print("Client - Error reading file: {}".format(e))
            client_socket.close()
            sys.exit()

        handle_server_response(client_socket)
        break

def handle_server_response(client_socket):
    try:
        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")

    except socket.error as e:
        print("Client - Error reading file: {}".format(e))
        client_socket.close()
        sys.exit()

    print("Client - Receiving server response:\n{}".format(response))

if __name__ == "__main__":
    parse_arguments()
    cl_socket = create_socket()
    connect_socket(cl_socket)
    handle_request(cl_socket)

    print("Client - Closing socket")
    cl_socket.close()
