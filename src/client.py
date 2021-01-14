import socket
import signal
import pickle
import select
import sys
from rsa import RSA_model

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
    print ("Port number required")
    exit()

server.connect(('', int(sys.argv[1])))

def signal_handler(signal, frame):
    ''' Capturing client's signal to exit
    '''
    print ("Closing server")
    server.close()
    exit()

# Setting up signal handler
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":

    # Providing server name
    name = input("Please enter your name: ")
    while name == "server":
        name = input("Your name cannot be 'server' please enter another name: ")

    # Initializing private public key
    user_rsa = RSA_model()
    print("Your public key is: ", user_rsa.m,  user_rsa.e)
    print("Your private key is: ", user_rsa._p, user_rsa._q, user_rsa._d)

    # Messages come in the form sender, reciever, message
    message = (name, "server", (user_rsa.m, user_rsa.e))


    data_msg = pickle.dumps(message)
    server.send(data_msg)
    print("User name and public key sent to server!")

    contacts = []

    while True:
        
        # Set list of byte streams to check with select
        sockets = [sys.stdin, server]

        # Selecting I/O ready to be read
        # Either stdin, or a message from the server
        ready, _, _  = select.select(sockets, [], [])

        for s in ready:
            # Server socket is ready
            if s == server:
                message = s.recv(2048)
                # Socket is not closed and message was received
                if message:
                    sender, receiver, msg = pickle.loads(message)
                    # Message from server is a list of users and public keys
                    if sender == "server":
                        contacts.extend(message)
                    # Message was destined for client
                    elif receiver == name:
                        message = user_rsa.decrypt(msg)
                        print(sender + ": " + message)
                # Socket is closed
                else:
                    print("Server was closed")
                    exit()

            # Client is sending a message
            else:
                message = sys.stdin.readline()
                message_split = message.split(" ", 1)
                cipher = user_rsa.encrypt(message_split[1])
                msg = pickle.dumps((name, message_split[0], cipher))
                server.send(msg)