import socket                   #for TCP socket
import threading                #for handling multiple clients
import sys                      #for command-line argument
from datetime import datetime   #for date and time

# Validate command-line port number
if len(sys.argv) != 2:
    print("Usage: python server.py <port>") #telling user how to run the program 
    sys.exit(1)

try:
    PORT = int(sys.argv[1])             #convert to integer
    if PORT < 1025 or PORT > 65535:   #check if the port number is between 1025 and 65535 inclusive
        raise ValueError
except ValueError:
    print("Error: Port number must be an integer between 1025 and 65535") #print error message
    sys.exit(1)

ADDR = ("0.0.0.0", PORT)    #listen on all interfaces and, specified port
HEADER = 1024               #max size of the message in bytes
FORMAT = "utf-8"            #text encoding
DISCONNECT_MESSAGE = "exit" #keyword for client to exit

#Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) #bind to IP and port

clients = []            #list to keep track of clients
lock = threading.Lock() #lock to stop race conditions
client_count = 0        #to assign unique name to each client

#Send message to all clients except the sender client
def broadcast_message(message, sender_conn):

    with lock:
        for conn, name in clients[:]:   #looping through all clients
            if conn != sender_conn:     #not to sender
                try:
                    conn.send(message.encode(FORMAT))
                except:
                    conn.close() #if client is disconnected, remove from list
                    clients.remove((conn, name))

# To handle messages from one client
def handle_client(conn, name):

    print(f"[NEW CONNECTION] {name} connected.")     #show connection on server console
    conn.send(f"Welcome {name}! Type '{DISCONNECT_MESSAGE}' to exit.\n".encode(FORMAT))

    while True:
        try:
            data = conn.recv(HEADER) #receive message from client
            if not data:
                break

            message = data.decode(FORMAT).strip() #decode bytes to string

            # Check for exit message
            if message.lower() == DISCONNECT_MESSAGE:
                break

            # Add timestamp MM/DD/YYY format
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            message_with_time = f"[{timestamp}] {name}: {message}"

            print(message_with_time)                            # Print message on server console
            broadcast_message(message_with_time + "\n", conn)   # Broadcast to other clients

        #client disconnect unexceptedly
        except ConnectionResetError:
            print(f"[DISCONNECT] {name} disconnected unexpectedly.")
            break

        #catching other errors
        except Exception as e: 
            print(f"[ERROR] {name}: {e}")
            break

    # Cleanup after client disconnects
    with lock:
        clients[:] = [(c, n) for c, n in clients if c != conn]

    conn.close()
    print(f"[DISCONNECTED] {name}")

# Start server
def start():

    global client_count

    server.listen() #start listening for incoming connections
    print(f"[LISTENING] Server running on port {PORT}")

    try:
        while True:
            conn, _ = server.accept()

            with lock:
                client_count += 1
                name = f"Client {client_count}"                 #assign name to client
                clients.append((conn, name))
                print(f"[ACTIVE CONNECTIONS] {len(clients)}")   #show active connections

            #start a new thread
            thread = threading.Thread(target=handle_client, args=(conn, name))
            thread.start()

    except KeyboardInterrupt: #allow Ctrl+C to stop
        print("\n[SHUTDOWN] Server shutting down...")

    finally:
        with lock:
            for conn, _ in clients:
                try:
                    conn.close()
                except:
                    pass
            clients.clear()
        server.close() #close server socket

# Run
print("[STARTING] Server starting...")
start()

