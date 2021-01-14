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

    # Providing server username
    name = input("What is your name?")

    # Initializing private public key
    user_rsa = RSA_model()
    print("Your public key is: ", user_rsa.m,  user_rsa.e)
    print("Your private key is: ", user_rsa._p, user_rsa._q, user_rsa._d)

    data_name = pickle.dumps(name)
    server.send(data_name)
    print("User name and public key sent username to server!")

    while True:
        
        sockets = [sys.stdin, server]

        # Selecting I/O ready to be read
        # Either stdin, or a message from the server
        ready, _, _  = select.select(sockets, [], [])

        for s in ready:
            if s == server:
                message = s.recv(2048)
                if (message):
                    print(message)
                else:
                    print("Server was closed")
                    exit()
            else:
                message = sys.stdin.readline()
                cipher = user_rsa.encrypt(message)
                server.send(cipher)