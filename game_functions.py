import pygame
from pieces import *

#def check_mate(all_pieces, color, coordinates):
#    my_pieces = [i for i in all_pieces if i.color == color]
#    king = [i for i in my_pieces if isinstance(i, King)][0]
#    for piece in all_pieces:
#        for x in range(8):
#            for y in range(8):
#                captured_piece = None
#                if isinstance(piece, Pawn):
#                    for piece1 in all_pieces:
#                        if isinstance(piece1, Pawn):
#                            if (piece1.x == x and piece1.y == y and piece1.color != piece.color) or (piece1.get_enpassant() and piece1.x == x and ((piece1.y == y+1 and piece.color == 'black') or (piece.y == y-1 and piece.color == 'white'))):
#                                captured_piece = piece
#                        else:
#                            if (piece1.x == x and piece1.y == y and piece1.color != piece.color):
#                                captured_piece = piece
#                    if piece._validate_move(x, y, bool(captured_piece), coordinates): return 'continue'
#                    if not simulate_move_and_check_king(piece, x, y, all_pieces, coordinates, captured_piece): continue
#                elif isinstance(piece, King):
#                    for piece1 in all_pieces:
#                        if (piece1.x == x and piece1.y == y and piece1.color != piece.color):
#                            is_defended = is_piece_defended(piece1, all_pieces, coordinates)
#                            if not is_defended:
#                                captured_piece = piece
#                                coordinates = [i for i in figures_coordinates if i != (captured_piece.x, captured_piece.y)]
#                                all_pieces = [i for i in all_pieces if i != captured_piece]
#                    if piece._validate_move(x, y, bool(captured_piece), coordinates, all_pieces): return 'continue'
#                else:
#                    for piece1 in all_pieces:
#                        if (piece1.x == x and piece1.y == y and piece1.color != piece.color):
#                            captured_piece = piece
#                            coordinates.remove((captured_piece.x, captured_piece.y))
#                    if not simulate_move_and_check_king(piece, x, y, all_pieces, coordinates, captured_piece): continue
#                    if piece._validate_move(x, y, coordinates): return 'continue'
#    return 'mate'

def is_check(king, all_pieces, coordinates):
    threatened_squares = king.get_threatened_squares(all_pieces, coordinates)
    in_check = (king.x, king.y) in threatened_squares
    return in_check


def simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, coordinates, captured_piece):
    original_x, original_y = selected_piece.x, selected_piece.y
    selected_piece.x, selected_piece.y = new_x, new_y
    if captured_piece:
        all_pieces.remove(captured_piece)
    king = [piece for piece in all_pieces if isinstance(piece, King) and piece.color == selected_piece.color][0]
    new_coordinates = [(p.x, p.y) for p in all_pieces if p!=king]
    in_check = is_check(king, all_pieces, new_coordinates)
    selected_piece.x, selected_piece.y = original_x, original_y
    if captured_piece:
        all_pieces.append(captured_piece)
    return in_check

def is_piece_defended(piece, all_pieces, coordinates):
    for defender in all_pieces:
        if defender.color == piece.color and defender != piece:
            if isinstance(defender, Pawn):
                if defender._validate_move(piece.x, piece.y, True, [i for i in coordinates if i != (piece.x, piece.y)]):
                    return True
            elif isinstance(defender, King):
                if defender._validate_move(piece.x, piece.y, False, [i for i in coordinates if i != (piece.x, piece.y)], all_pieces):
                    return True
            else:
                if defender._validate_move(piece.x, piece.y, [i for i in coordinates if i != (piece.x, piece.y)]):
                    return True
    return False

def promote_pawn_dialog(sc):
    font = pygame.font.Font(None, 36)
    options = ['Queen', 'Rook', 'Bishop', 'Knight']
    option_rects = []

    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        rect = text.get_rect(center=(200, 100 + i * 50))
        sc.blit(text, rect)
        option_rects.append((rect, option))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, option in option_rects:
                    if rect.collidepoint(pos):
                        return option
