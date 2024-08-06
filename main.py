import pygame 
import sys
import socket
from hashlib import md5
from threading import Thread
import time
from draw_chessboard import *
from pieces import *
from create_pieces import *
from game_functions import *
from generate_keys import keys_generator
from decrypt import decrypt
from encrypt import encrypt
from sending_messages import send

pygame.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sc = pygame.display.set_mode((400,500))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 16)
FPS = 30

WHITE = (250, 250, 250)
GREEN = (0, 128, 0)

data = None

chessboard(sc, WHITE, GREEN)

selected_piece = None
move_color = 'white'

all_pawns = create_pawns()
all_knights = create_knights()
all_bishops = create_bishops()
all_rooks = create_rooks()
all_queens = create_queens()
all_kings = create_kings()
all_pieces = all_pawns + all_knights + all_bishops + all_rooks + all_queens + all_kings
figures_coordinates = [(i.x, i.y) for i in all_pieces]

spectators = []

def handle_spectator(role):
    global spectators
    global public_key
    global sock
    while True:
        if role == 'server':
            sock.listen()
            client, address = sock.accept()
            client.send(bytes(' '.join(list(map(str,public_key))), 'utf-8'))
            opponent_public_key = client.recv(124).decode()
            opponent_public_key = list(map(int, opponent_public_key.split(' ')))
            spectators.append([client, opponent_public_key])
            message = f"{game_time},{time_increment}"
            sign = encrypt(private_key, md5(message.encode()).hexdigest())
            client.send(bytes(f"{message},{sign}", "utf-8"))

def timer(all_pieces):
    global player_time
    global opponent_time
    global move_color
    global player_color
    while True:
        if move_color == player_color:
            player_time -= 1
        else: opponent_time -= 1
        draw_figures(all_pieces, player_time, opponent_time)
        time.sleep(1)

def recieve(key, client, role):
    global data
    while True:
        message = client.recv(256).decode()
        if message:
            if message[:8] != "message:": 
                data = message
            else:
                if role != 'spectator':
                    message = message[8:]
                    message = decrypt(key, message)
                    print(f'{client.getpeername()[0]}:{client.getpeername()[1]} -', message)
                data = None

def draw_figures(all_pieces, player_time, opponent_time):
    chessboard(sc, WHITE, GREEN)
    for i in all_pieces:
        sc.blit(i.image, i.rect)
    player_timer = font.render(f"Your time: {player_time//60}:{player_time%60}", True, (0, 255, 0))
    opponent_timer = font.render(f"Opponent time: {opponent_time//60}:{opponent_time%60}", True, (0, 255, 0))
    player_timer_rect = player_timer.get_rect(center=(100, 450))
    opponent_timer_rect = opponent_timer.get_rect(center=(300, 450))
    sc.blit(player_timer, player_timer_rect)
    sc.blit(opponent_timer, opponent_timer_rect)
    pygame.display.flip()

public_key, private_key = keys_generator()

if len(sys.argv) == 1:
    game_time = int(input("Time (minutes): "))
    player_time = game_time*60
    opponent_time = game_time*60
    time_increment = int(input("Increment (seconds): "))
    HOST = '127.0.0.1'
    for port in range(49152, 65535):
        if sock.connect_ex(('127.0.0.1', port)):
            PORT = port
            sock.close()
            break
        sock.close()
    else: 
        print('no available port')
        exit()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, PORT))
        print(f"server started on {HOST}:{PORT}")
    except:
        print(f"error while starting server on {HOST}:{PORT}")
        exit()

    sock.listen(5)
    client, address = sock.accept()
    print(f"user connected on address: {address[0]}:{address[1]}")

    client.send(bytes(' '.join(list(map(str,public_key))), 'utf-8'))
    opponent_public_key = client.recv(124).decode()
    opponent_public_key = list(map(int, opponent_public_key.split(' ')))

    message = f"{game_time},{time_increment}"
    sign = encrypt(private_key, md5(message.encode()).hexdigest())
    client.send(bytes(f"{message},{sign}", "utf-8"))

    player_color = 'white'
    opponent_color = 'black'

    role = 'server'
elif len(sys.argv) == 3:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    try:
        client.connect((HOST, PORT))
        print('connected to server')
    except:
        print('error while connecting to server')

    opponent_public_key = client.recv(124).decode()
    opponent_public_key = list(map(int, opponent_public_key.split(' ')))
    client.send(bytes(' '.join(list(map(str, public_key))), 'utf-8'))
    
    message = client.recv(256).decode()
    message, sign = ','.join(message.split(',')[:2]), message.split(',')[2:] 
    decrypted_sign = decrypt(opponent_public_key, sign[0])
    if md5(message.encode()).hexdigest() == decrypted_sign:
        player_time, time_increment = int(message.split(',')[0])*60, int(message.split(',')[1])
        opponent_time = player_time
    else: print('sign does not match')

    player_color = 'black'
    opponent_color = 'white'

    role = 'client'
elif len(sys.argv) == 4:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    try:
        client.connect((HOST, PORT))
        print('connected to server')
    except:
        print('error while connecting to server')

    opponent_public_key = client.recv(124).decode()
    opponent_public_key = list(map(int, opponent_public_key.split(' ')))
    client.send(bytes(' '.join(list(map(str, public_key))), 'utf-8'))
    
    message = client.recv(256).decode()
    message, sign = ','.join(message.split(',')[:2]), message.split(',')[2:] 
    decrypted_sign = decrypt(opponent_public_key, sign[0])
    if md5(message.encode()).hexdigest() == decrypted_sign:
        player_time, time_increment = int(message.split(',')[0])*60, int(message.split(',')[1])
        opponent_time = player_time
    else: print('sign does not match')

    player_color = 'black'
    opponent_color = 'white'
    role = 'spectator'
else:
    print('error')
    exit()

draw_figures(all_pieces, player_time, opponent_time)

send_thread = Thread(target=send, args=(opponent_public_key, client), daemon=True)
recieve_thread = Thread(target=recieve, args=(private_key, client, role), daemon=True)
timer_thread = Thread(target=timer, args=(all_pieces,), daemon=True)
handle_spectator_thread = Thread(target=handle_spectator, args=(role,), daemon=True) 
send_thread.start()
recieve_thread.start()
timer_thread.start()
handle_spectator_thread.start()

while True:
    for event in pygame.event.get():
        if move_color == opponent_color or role == 'spectator':
            # data = client.recv(256).decode()
            if data:
                message, sign = data[:8], data[9:]
                decrypted_sign = decrypt(opponent_public_key, sign)
                if md5(message.encode()).hexdigest() == decrypted_sign:
                    piece_x, piece_y, new_x, new_y, promote_piece = list(map(int, message.split(',')[:4])) + message.split(',')[4:]
                    
                    if role == 'server':
                        message = f"{piece_x},{piece_y},{new_x},{new_y},{promote_piece}"
                        sign = encrypt(private_key, md5(message.encode()).hexdigest())
                        client.send(bytes(f"{message},{sign}", "utf-8"))

                        for spectator in spectators:
                            spectator[0].send(bytes(f"{message},{sign}", "utf-8"))

                    captured_piece = None

                    for piece in all_pieces:
                        if (piece.x, piece.y) == (piece_x, piece_y):
                            moved_piece = piece
                        if (piece.x, piece.y) == (new_x, new_y):
                            captured_piece = piece
                
                    if isinstance(moved_piece, Pawn):
                        for piece in all_pieces:
                            if isinstance(piece, Pawn):
                                if piece.get_enpassant() and piece.x == new_x and piece.color == player_color:
                                    if (piece.y == new_y-1 and piece.color == 'white') or (piece.y == new_y+1 and piece.color == 'black'):
                                        captured_piece = piece
                        moved_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates)
                        if promote_piece:
                            match promote_piece:
                                case 'Queen':
                                    all_pieces.append(Queen(new_x, opponent_color, y = new_y))
                                case 'Rook':
                                    all_pieces.append(Rook(new_x, opponent_color, y = new_y))
                                case 'Bishop':
                                    all_pieces.append(Bishop(new_x, opponent_color, y = new_y))
                                case 'Knight':
                                    all_pieces.append(Knight(new_x, opponent_color, y = new_y))
                            all_pieces.remove(moved_piece)
                            all_pawns.remove(moved_piece)
                    elif isinstance(moved_piece, King):
                        coordinates = figures_coordinates
                        pieces = all_pieces
                        if captured_piece:
                            coordinates = [i for i in figures_coordinates if i != (captured_piece.x, captured_piece.y)]
                            pieces = [i for i in all_pieces if i != captured_piece]
                        move_result = moved_piece.move(new_x, new_y, bool(captured_piece), coordinates, pieces)
                        if isinstance(move_result, str):
                            if move_result == 'short':
                                rook = [i for i in all_pieces if i.x == 7 and isinstance(i, Rook) and i.color == opponent_color][0]
                                rook.x = 5
                                rook.rect.topleft = (5 * 50, new_y * 50)
                            elif move_result == 'long':
                                rook = [i for i in all_pieces if i.x == 0 and isinstance(i, Rook) and i.color == opponent_color][0]
                                rook.x = 3
                                rook.rect.topleft = (3 * 50, new_y * 50)
                    else:
                        if captured_piece: figures_coordinates.remove((captured_piece.x, captured_piece.y))
                        moved_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates)
                        if isinstance(moved_piece, Rook):
                            king = [i for i in all_pieces if isinstance(i, King) and i.color == opponent_color][0]
                            if moved_piece.x == 0: king.long_castle = False
                            if moved_piece.x == 7: king.short_castle = False
                    if captured_piece:
                        all_pieces.remove(captured_piece)
                        if isinstance(captured_piece, Pawn): all_pawns.remove(captured_piece)
                    for pawn in all_pawns:
                        pawn.subbstract_enpassant()
                    draw_figures(all_pieces, player_time, opponent_time)
                    move_color = player_color
                    opponent_time+=time_increment
                else: print('sign does not match')
                data = None
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and role != 'spectator':
            pos = pygame.mouse.get_pos()
            figures_coordinates = [(i.x, i.y) for i in all_pieces]
            if move_color != player_color: 
                continue

            if selected_piece == None:
                for piece in all_pieces:
                    if piece.rect.collidepoint(pos):
                        selected_piece = piece if move_color == piece.color else None

            else:
                captured_piece = None
                new_x = pos[0] // 50
                new_y = pos[1] // 50
                old_x, old_y = selected_piece.x, selected_piece.y
                figure = ''
                if isinstance(selected_piece, Pawn):
                    for piece in all_pieces:
                        if isinstance(piece, Pawn):
                            if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color) or (piece.get_enpassant() and piece.x == new_x and ((piece.y == new_y+1 and piece.color == 'black') or (piece.y == new_y-1 and piece.color == 'white'))):
                                captured_piece = piece
                        else:
                            if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                                captured_piece = piece
                    if simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, figures_coordinates, captured_piece):
                        print('check')
                        selected_piece = None
                        continue                   
                    if not selected_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates):
                        selected_piece = None
                        continue
                    if (selected_piece.color == 'black' and new_y == 7) or (selected_piece.color == 'white' and new_y == 0):
                        figure = promote_pawn_dialog(sc)
                        match figure:
                            case 'Queen':
                                all_pieces.append(Queen(new_x, selected_piece.color, y = new_y))
                            case 'Rook':
                                all_pieces.append(Rook(new_x, selected_piece.color, y = new_y))
                            case 'Bishop':
                                all_pieces.append(Bishop(new_x, selected_piece.color, y = new_y))
                            case 'Knight':
                                all_pieces.append(Knight(new_x, selected_piece.color, y = new_y))
                        all_pieces.remove(selected_piece)
                        all_pawns.remove(selected_piece)
                elif isinstance(selected_piece, King):
                    coordinates = figures_coordinates
                    pieces = all_pieces
                    for piece in all_pieces:
                        if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                            is_defended = is_piece_defended(piece, all_pieces, figures_coordinates)
                            if not is_defended:
                                captured_piece = piece
                                coordinates = [i for i in figures_coordinates if i != (captured_piece.x, captured_piece.y)]
                                pieces = [i for i in all_pieces if i != captured_piece]
                    move_result = selected_piece.move(new_x, new_y, bool(captured_piece), coordinates, pieces)
                    if not move_result:
                        selected_piece = None
                        continue
                    if isinstance(move_result, str):
                        if move_result == 'short':
                            rook = [i for i in all_pieces if i.x == 7 and isinstance(i, Rook) and i.color == selected_piece.color][0]
                            rook.x = 5
                            rook.rect.topleft = (5 * 50, new_y * 50)
                        elif move_result == 'long':
                            rook = [i for i in all_pieces if i.x == 0 and isinstance(i, Rook) and i.color == selected_piece.color][0]
                            rook.x = 3
                            rook.rect.topleft = (3 * 50, new_y * 50)
                else:
                    for piece in all_pieces:
                        if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                            captured_piece = piece
                            figures_coordinates.remove((captured_piece.x, captured_piece.y))
                    if simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, figures_coordinates, captured_piece):
                        print('check')
                        selected_piece = None
                        continue                   
                    if not selected_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates):
                        selected_piece = None
                        continue
                    if isinstance(selected_piece, Rook):
                        king = [i for i in all_pieces if isinstance(i, King) and i.color == selected_piece.color][0]
                        if selected_piece.x == 0: king.long_castle = False
                        if selected_piece.x == 7: king.short_castle = False
                if captured_piece:
                    all_pieces.remove(captured_piece)
                    if isinstance(captured_piece, Pawn): all_pawns.remove(captured_piece)
                move_color = opponent_color
                player_time += time_increment
                selected_piece = None
                for pawn in all_pawns:
                    pawn.subbstract_enpassant()
                message = f"{old_x},{old_y},{new_x},{new_y},{figure}"
                sign = encrypt(private_key, md5(message.encode()).hexdigest())
                client.send(bytes(f"{message},{sign}", "utf-8"))

                if role == 'server':
                    for spectator in spectators:
                        spectator[0].send(bytes(f"{message},{sign}", "utf-8"))
                        print('kys')

                draw_figures(all_pieces, player_time, opponent_time)
    # sc.fill((0, 0, 0))
    clock.tick(FPS)
