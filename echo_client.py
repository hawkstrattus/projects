import argparse
import socket
import sys
from typing import Tuple


def options() -> Tuple[str, int]: # function controls arguements passed to the script

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", type=str, help="Specify the server address")
    parser.add_argument("-p", "--port", type=int, help="Specify the server's port for connection")

    args = parser.parse_args()

    if args.server is None or args.port is None:
        print("Server and/or port not specified... exiting...")
        cleanup()


    return args.server, args.port


def cleanup(client_socket=None): # cleanup function to be called incase main() needs to exit
    if client_socket is not None:
        try:
            client_socket.close()
        except socket.error as error:
            print(f"Failed to close socket: {error}")
    sys.exit()


def main():

    server_address, server_port = options() # calling the options function to grab the server and port from the user

    # this block attempts to create a socket and handle errors
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("client socket made...\n")
    except socket.error as error:
        print(f"Failed to create client socket: {error}")
        cleanup()

    print("Socket created \n")

    # this block attempts to connect to the server socket
    try:
        client_socket.connect((server_address, server_port))
        print("client socket connected...\n")
    except socket.error as error:
        print(f"Failed to connect to server: {error}")
        cleanup(client_socket)
    
    print("Connected to server \n")

    # this block attempts to grab user input, send the input to the server, and recieve the message back
    while True:
        try:
            print("Enter your echo message:\n")
            message = input()
            client_socket.send(message.encode())
        except socket.error as error:
            print(f"Error with sending message: {error}")
            continue
        
        try:
            response = client_socket.recv(1024)
            print(f"Response: {response.decode()}")
        except socket.error as error:
            print(f"Error receiving message: {error}")

if __name__ == '__main__'
    main()