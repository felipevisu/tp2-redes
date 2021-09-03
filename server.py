import socket
import pickle
import time

from _thread import *
from game import *

server = "127.0.0.1"
port = 54321

BUFFER_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)
print("Esperando uma conexão")

games = []

def threaded_client(conn, player):
    index = player % 2

    if index == 0:
        game = new_game()
        game.id = len(games) + 1
        games.append(game)

    i = len(games) - 1

    games[i].players[index] = player_types[index]
    games[i].players[index].id = index

    conn.send(pickle.dumps(games[i].players[index]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(BUFFER_SIZE))
            games[i].players[index] = data

            games[i].set_winner()

            if not data:
                print("Desconetado")
                break
            else:
                if index == 1:
                    reply = games[i].players[0]
                else:
                    reply = games[i].players[1]

            if index == 0:
                for street in games[i].streets:
                    street.move()

            conn.sendall(pickle.dumps((reply, games[i])))
        except:
            break
    
    print("Conexão perdida")
    games[i].players[index] = None
    conn.close()


current_player = 0

while True:
    conn, addr = sock.accept()
    print("Conetado a:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1