import socket
import signal
import pickle
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('', 0))

server.listen(100)

clients = []
client_details = []

def signal_handler(signal, frame):
    ''' Capturing an admin's signal to exit
    '''
    print ("Closing server")
    close_network()
    exit()

# Setting up signal handler
signal.signal(signal.SIGINT, signal_handler)

def new_client(conn):
    ''' Receive new message details from client.
    Send client existing client details.
    '''
    print("A client has connected")
    try:
        print("Receiving client's info")
        # Receive and unpack first message
        message = conn.recv(2048)
        sender, _, (n, e) = pickle.loads(message)
        client = (sender, n, e)

        # Sending new client existing client details
        # Adding client to records
        clients.append(conn)
        conn.send(pickle.dumps(("server", "add", client_details)))
        client_details.append(client)

        # Sending all clients new client info
        broadcast(pickle.dumps(("server", "add", [client])), conn)
        print("Client " + sender + " added to network!")
        return sender
    except:
        # Connection broken on initial message
        # Remove client and kill thread

        return False


def manage_client(conn):
    ''' A function we call to manage a client's connection in thread.
    '''

    client = new_client(conn)
    if not client:
        print("Failed to prepare client for network communication")
        return

    while True:
        try:
            message = conn.recv(2048)
            if message:
                msg = pickle.loads(message)
                # Log message server and destination
                print("RECEIVED MESSAGE: ", msg)
                # Broadcast message to all clients on the network
                broadcast(message, conn)
            else:
                # Connection is broken, disconnect the client and return to kill thread
                remove_client(conn)
                return
        except:
            # Error when receiving message
            # Log error and take action
            # In our case we just continue
            continue

def broadcast(message, conn):
    ''' Broadcasts the message to all clients on the network.
    '''
    for c in clients:
        if c != conn:
            try:
                c.send(message)
            except:
                # Error sending message to client, we remove close connection and remove client
                c.close()
                remove_client(conn)

def remove_client(c):
    ''' Removes the provided client from the list of client connections.
    '''
    if c in clients:
        idx = clients.index(c)
        clients.pop(idx)
        name, _, _ = client_details.pop(idx)
        print("Removed client " + name + " from the network")
        message = ("server", "remove", name)
        broadcast(pickle.dumps(message), None)

def close_network():
    ''' Closes the demo server
    '''
    for c in clients:
        c.close()
    server.close()


if __name__ == "__main__":


    print("Server bound to port ", server.getsockname()[1])

    # Using global closed variable to handle loop

    while True:
        # Accepts connections and stores their information
        # We only store the user's connection since the demo is run on the same machine
        conn = server.accept()[0] 

        # Start a new thread to handle the client's connection
        start_new_thread(manage_client,(conn,))
        