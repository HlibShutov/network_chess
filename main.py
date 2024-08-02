import pygame 
import sys
import socket
from draw_chessboard import *
from pieces import *
from create_pieces import *
from game_functions import *
pygame.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sc = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
FPS = 30

WHITE = (250, 250, 250)
GREEN = (0, 128, 0)

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

def draw_figures(all_pieces):
    chessboard(sc, WHITE, GREEN)
    for i in all_pieces:
        sc.blit(i.image, i.rect)
        pygame.display.flip()
draw_figures(all_pieces)

if len(sys.argv) == 1:
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
    player_color = 'white'
    opponent_color = 'black'
elif len(sys.argv) == 3:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    try:
        client.connect((HOST, PORT))
        print('connected to server')
    except:
        print('error while connecting to server')
    player_color = 'black'
    opponent_color = 'white'
else:
    print('error')
    exit()


while True:
    for event in pygame.event.get():
        if move_color == opponent_color:
            data = client.recv(256).decode()
            if data:
                piece_x, piece_y, new_x, new_y, promote_piece = list(map(int, data.split(' ')[:4])) + data.split(' ')[4:]
                captured_piece = None
                for piece in all_pieces:
                    if (piece.x, piece.y) == (piece_x, piece_y):
                        moved_piece = piece
                    if (piece.x, piece.y) == (new_x, new_y):
                        captured_piece = piece
                
                if isinstance(moved_piece, Pawn):
                    for piece in all_pieces:
                        if isinstance(piece, Pawn):
                            if piece.get_enpassant() and piece.x == new_x and ((piece.y == new_y-1 and piece.color == player_color)):
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
                move_color = player_color
                draw_figures(all_pieces)
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            figures_coordinates = [(i.x, i.y) for i in all_pieces]
            #print(check_mate(all_pieces, move_color, figures_coordinates)) 
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
                    old_x, old_y = selected_piece.x, selected_piece.y
                    if not selected_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates):
                        selected_piece = None
                        continue
                    figure = ''
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
                    if captured_piece:
                        all_pieces.remove(captured_piece)
                        if isinstance(captured_piece, Pawn): all_pawns.remove(captured_piece)
                        #if isinstance(captured_piece, Knight): all_knights.remove(captured_piece)
                    move_color = opponent_color
                    selected_piece = None
                    draw_figures(all_pieces)
                    for pawn in all_pawns:
                        pawn.subbstract_enpassant()
                    client.send(bytes(f"{old_x} {old_y} {new_x} {new_y} {figure}", "utf-8"))
                    continue
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
                    old_x, old_y = selected_piece.x, selected_piece.x
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
                        move_color = opponent_color
                        selected_piece = None
                        draw_figures(all_pieces)
                        for pawn in all_pawns:
                            pawn.subbstract_enpassant()
                        continue

                    move_color = opponent_color
                    if captured_piece:
                        all_pieces.remove(captured_piece)
                    selected_piece = None
                    draw_figures(all_pieces)
                    for pawn in all_pawns:
                        pawn.subbstract_enpassant()
                    client.send(bytes(f"{old_x} {old_y} {new_x} {new_y} ", "utf-8"))
                    continue
                for piece in all_pieces:
                    if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                        captured_piece = piece
                        figures_coordinates.remove((captured_piece.x, captured_piece.y))

                
                if simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, figures_coordinates, captured_piece):
                    print('check')
                    selected_piece = None
                    continue                   
                old_x, old_y = selected_piece.x, selected_piece.y
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
                    #if isinstance(captured_piece, Knight): all_knights.remove(captured_piece)
                    #if isinstance(captured_piece, Bishop): all_bishops.remove(captured_piece)
                    #if isinstance(captured_piece, Rook): all_rooks.remove(captured_piece)
                move_color = opponent_color
                selected_piece = None
                for pawn in all_pawns:
                    pawn.subbstract_enpassant()
                client.send(bytes(f"{old_x} {old_y} {new_x} {new_y} ", "utf-8"))
                draw_figures(all_pieces)

    sc.fill((0, 0, 0))
    clock.tick(FPS)
