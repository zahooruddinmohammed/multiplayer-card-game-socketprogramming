import socket

# Define the host and port to connect to
host = "127.0.0.1"
port = 5555

# Create a TCP socket and connect to the host and port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Send data to the server
client.send("Hello, server!".encode())

# Receive data from the server
response = client.recv(1024)
print(response.decode())
print("hello")

# Close the connection
client.close()
