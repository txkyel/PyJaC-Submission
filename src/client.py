import socket
import signal
import pickle
import select
import sys
from rsa import RSA_model

# Preparing socket for connection to server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
    print ("Port number required")
    exit()
server.connect(('', int(sys.argv[1])))

def signal_handler(signal, frame):
    ''' Capturing SIGINT to close server
    '''
    print ("Closing server")
    server.close()
    exit()

# Setting up signal handler
signal.signal(signal.SIGINT, signal_handler)


def handle_msg(name, message, contacts):
    ''' Parses the message recieved from the server and 
    either manages the client list, prints the message if 
    intended for client, or drops the message entirely
    '''
    # Socket is not closed and message was received
    if message:
        # Unpack message
        sender, receiver, msg = pickle.loads(message)

        # Message is from server directly
        if sender == "server":
            # New contact
            if receiver == "add":
                print("Adding to conacts list", msg)
                contacts.extend(msg)

            # Remove contact
            elif receiver == "remove":
                # Find contact and remove
                for i in range(len(contacts)):
                    name, _, _ = contacts[i]
                    if name == msg:
                        print("Removing ", contacts.pop(i), " from contacts")
                        break

        # Message was destined for client
        elif receiver == name:
            message = user_rsa.decrypt(msg)
            print(sender + ": " + message)

    # Socket is closed
    else:
        print("Server was closed")
        exit()


if __name__ == "__main__":

    # Providing server name
    name = input("Please enter your name: ")
    while name == "server" or ' ' in name:
        name = input("Your name cannot be 'server' or contain spaces.\nPlease enter your name: ")

    # Initializing private public key
    user_rsa = RSA_model()
    print("Your public key is: ", user_rsa.n,  user_rsa.e)
    print("Your private key is: ", user_rsa._p, user_rsa._q, user_rsa._d)

    # Messages come in the form sender, reciever, message
    message = (name, "server", (user_rsa.n, user_rsa.e))

    data_msg = pickle.dumps(message)
    server.send(data_msg)
    print("User name and public key sent to server!")

    # List of tuples containing target name and RSA private key
    contacts = []

    print("Please format your messages as '<target user> <message>'")

    while True:
        
        # Set list of byte streams to check with select
        sockets = [sys.stdin, server]

        # Selecting ready file descriptors
        # Either stdin, or a message from the server
        ready, _, _  = select.select(sockets, [], [])

        # For all ready file descriptors
        for s in ready:
            # Server socket is ready
            if s == server:
                handle_msg(name, s.recv(2048), contacts)

            # Client is sending a message
            else:
                # Messages are formatted as <name> + " " + <message>
                # Determine intended receiver and encrypt message
                message = sys.stdin.readline()
                message_split = message.split(" ", 1)
                receiver = message_split[0]
                e = -1
                for c in contacts:
                    if c[0] == receiver:
                        _, n, e = c
                if e < 1:
                    print("User does not exist in contacts, please try again.")
                    continue
                cipher = user_rsa.encrypt(message_split[1].strip('\n'), e, n)
                msg = pickle.dumps((name, receiver, cipher))
                server.send(msg)