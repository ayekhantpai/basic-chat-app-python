# Basic Chat Application

A real-time text-based chat application built with Python using TCP sockets and multithreading. This project enables multiple users to connect to a central server and communicate instantly through a client-server architecture.

## Features
- Supports multiple clients simultaneously  
- Real-time message sending and receiving  
- Unique chat ID assigned to each client  
- Timestamp added to every message  
- Active connection count displayed on server  
- Graceful disconnect using `exit` command  
- Handles unexpected client disconnections  

## Technologies Used
- Python 3  
- Socket Library  
- Threading Library  
- Datetime Library  
- Visual Studio Code  

## Project Files
- `server.py` – Starts the chat server, accepts client connections, and broadcasts messages  
- `client.py` – Connects to the server and allows users to send and receive messages  

## How to Run

## Run Server
python server.py <port>

## Run Client
python client.py <port>

### Start Server Start Client
python client.py <port>

Port Requirement
Choose any available port number in the range:
1025 ≤ port ≤ 65535
Both server and client must use the same port number.
