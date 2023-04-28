import socket
CARD_VALUES = {1: 'Ace', 2: '2', 3: '3', 4: '4', 5 : '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 13: 'King', 12: 'Queen', 11: 'Jack'}


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    HOST = '127.0.0.1'
    port = 5038 
     # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(('127.0.0.1', 5038))  # connect to the server

    message = "Hello"

    player_name = client_socket.recv(1024).decode()
    print('Player Card: ', player_name)

    while message.lower().strip() != 'bye':
        # send message
        data = client_socket.recv(1024).decode()  # receive response
        if "Error" not in data:
            print('Server Card: ' + CARD_VALUES[int(data)])  # show in terminal
            print('choose a card number')
            while True:
                message = input(" -> ")  # again take input
                if message in CARD_VALUES.values():
                    key = list(filter(lambda x: CARD_VALUES[x] == message, CARD_VALUES))[0]
                    message = player_name + "|" + str(key)
                    client_socket.send(message.encode())
                    break
                else:
                    print('Please select a valid card') 
        else:
            print(data)
            message = input(" -> ")  # again take input
            if message in CARD_VALUES.values():
                key = list(filter(lambda x: CARD_VALUES[x] == message, CARD_VALUES))[0]
                message = player_name + "|" + str(key)
                client_socket.send(message.encode())
                break
            else:
                    print('Please select a valid card') 

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()