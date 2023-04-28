import random
import socket

# Define constants
NUM_ROUNDS = 13
CARD_VALUES = {1: 'Ace', 2: '2', 3: '3', 4: '4', 5 : '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 13: 'King', 12: 'Queen', 11: 'Jack'}
CARD_NAMES = {'Client1': 'Spades', 'Client2':'Diamonds', 'Client3' : 'Clubs', 'Server' : 'Spades'}
# Define server host and port
HOST = '127.0.0.1'
PORT = 5038

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(3)
print('Waiting for players to connect...')
try:
    # Accept connections from three clients
    client_sockets = []
    for i in range(3):
        client_socket, client_address = server_socket.accept()
        client_sockets.append(client_socket)
        client_name = 'Client'+ str(i+1)
        print('Connected to', client_name)
        player_name = CARD_NAMES[client_name]
        client_socket.send(player_name.encode())

    # Initialize scores for each player
    scores = {"Spades": 0, "Diamonds": 0, "Clubs": 0}

    # Play 13 rounds of the game

    client_cards = {"Spades": [], "Diamonds": [], "Clubs": []}
    server_cards = CARD_VALUES.copy()
    for round_num in range(NUM_ROUNDS):
        print('Round', round_num+1)

        # Generate a random card from the server's suit
        server_card = random.choice(list(server_cards.keys()))
        print('Card', CARD_VALUES[server_card])
        del server_cards[server_card]

        # Send the server card to all clients
        for client_socket in client_sockets:
            client_socket.sendall(str(server_card).encode())

        # Receive one card from each client
        round_card = {}
        for i, client_socket in enumerate(client_sockets):

            # Receive client's card
            while True:
                message = client_socket.recv(1024).decode()
                card = message.split("|")
                
                # Check that the card is a new card that hasn't been sent by this client before
                if card[1] in client_cards[card[0]]:
                    # Send an error message to the client and close the connection
                    client_socket.send('Error: You cannot use the same card twice.'.encode())
                    continue
                
                print(card[0] + " : " + card[1])
                round_card[card[0]] = card[1]
                break
            # Add the card to the list of cards sent by clients
            client_cards[card[0]].append(card[1])

        max_pairs = []

        # Determine the winner of the round
        max_value = max(round_card.values())
        for key, value in round_card.items():
            if value == max_value:
                max_pairs.append((key,value))

        for pair in max_pairs:
            scores[pair[0]] = int(scores[pair[0]]) + server_card
        print(client_cards)
        print(scores)
    # Determine the winner
    max_score = max(scores.items(), key = lambda x: x[1])
    print('Winner' + max_score)

except KeyboardInterrupt:
        if server_socket:
            server_socket.close()