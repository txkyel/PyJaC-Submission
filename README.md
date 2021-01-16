# PyJaC-Submission

## Dependencies
* ``Python 3.0`` or greater which you can download and install [here](https://www.python.org/downloads/)
* ``PyCryptoDome`` you read up on and learn how to to install [here](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)

## Description
A simple chat service used to model and demonstrate a network that utilizes 32 bit RSA encryption to encrypt client messages broadcasted over the network.

## How to run the Demo
1. Run ``server.py`` in terminal using the command ``python3 server.py``. Printed in terminal should be the port number that the service will be running on locally.
2. Using this port number, you can choose to run any number of instances of ``client.py`` using the command ``python3 client.py <port number>``.
3. In the client terminals, you can follow the prompts to message back and forth between clients seeing how the messages are being encrypted and decrypted. 
4. When finished, you can close the server and all the clients by sending ``SIGINT`` to the server process with the key combination ``Ctrl + D``

## Flaws
There are several flaws with the implementation of this program discouraging it from being used as a messaging system
* Clients and the server do not vet messages or client names allowing for invalid names and for messages to crash the server/clients
* The service does not follow any message protocol requiring messages to be within at most 2048 bytes in length
* Breaking of the used 32 bit RSA keys is feasible with methods such as the quadratic sieve due to how small these numbers are compared to real world applications using 1024 bit RSA or higher
* With the method used to encrypt messages, messages are easily decoded using frequency analysis
