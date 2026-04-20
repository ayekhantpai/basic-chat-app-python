import socket                   #for TCP socket
import threading                #for handling multiple clients
import sys                      #for command-line argument

# Validate command-line port number
if len(sys.argv) != 2:
    print("Usage: python client.py <port>") #telling user how to run the program 
    sys.exit(1)

try:
    PORT = int(sys.argv[1])             #convert to integer
    if PORT < 1025 or PORT > 65535:   #check if the port number is between 1025 and 65535 inclusive
        raise ValueError
except ValueError:
    print("Error: Port number must be an integer between 1025 and 65535") #print error message
    sys.exit(1)

SERVER_IP = "localhost"         #server IP to connect to localhost, same machine
ADDR = (SERVER_IP, PORT)
HEADER = 1024                   #max size of the message in bytes
FORMAT = "utf-8"                #text encoding
DISCONNECT_MESSAGE = "exit"     #keyword for client to exit

#create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)                        #connect to server
except Exception:
    print("Error: Could not connect to server.") #connection failed
    sys.exit(1)

#inform client to type 'exit', if want to disconnect
print("Successfully connected to server! Please type 'exit' to leave the chat.")

# Receive messages
def receive_messages():

    while True:
        try:
            data = client.recv(HEADER) #receive data from server

            if not data:
                print("\n[INFO] Server closed the connection.")
                break

            message = data.decode(FORMAT) #decode bytes to string
            print(f"\n{message}", end="") #print received message

        #catching other errors
        except Exception:
            break

    # Make sure program exits if server disconnects
    print("[DISCONNECTED]")
    client.close()  #close socket
    sys.exit(0)     #exit program

thread = threading.Thread(target=receive_messages)  # Start receiving message in separate thread
thread.daemon = True                                # Thread exist, if main program exist
thread.start()                                      # Start Thread


# Send messages
try:
    while True:
        msg = input() #read user input

        if msg.lower() == DISCONNECT_MESSAGE: #if user type 'exist'
            try:
                client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            except Exception:
                pass
            break #exit loop

        try:
            client.send(msg.encode(FORMAT))             #send message to server
        except Exception:
            print("[ERROR] Failed to send message.")    #failed
            break

except KeyboardInterrupt: #if Ctrl+C
    print("\n[EXIT] Closing client.")

# Cleanup
client.close()
print("Disconnected from server.")
