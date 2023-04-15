import socket
import threading

# Define deck of cards
cards = ['1','2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

# Define number of rounds to play
NUM_ROUNDS = 13

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        data = conn.recv(1024)
        if not data:
            break
        # Process the data received from the client
        # ...
        # Send welcome message to client
        conn.sendall(f'Welcome to the card game! You are client.'.encode())

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")


def start_server():
    # Define the host and port to listen on
    host = "127.0.0.1"
    port = 5555

    # Create a TCP socket and bind it to the host and port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    # Start listening for incoming connections
    server.listen()

    print(f"[LISTENING] Server is listening on {host}:{port}...")

    # Create a thread for each incoming connection
    while True:
        if threading.activeCount() - 1 > 3:
            conn.close()
            raise Exception('Fourth client connected so its connection was closed.')
        else:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == '__main__':
    start_server()