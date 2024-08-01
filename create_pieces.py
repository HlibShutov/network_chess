from pieces import *
import pygame
def create_pawns():
    white_pawns = [Pawn(i, 'white') for i in range(8)]
    black_pawns = [Pawn(i, 'black') for i in range(8)]
    pawns = white_pawns + black_pawns
    return pawns

def create_knights():
    white_knights = [Knight(1, 'white'), Knight(6, 'white')]
    black_knights = [Knight(1, 'black'), Knight(6, 'black')]
    knights = white_knights + black_knights
    return knights

def create_bishops():
    white_bishops = [Bishop(2, 'white'), Bishop(5, 'white')]
    black_bishops = [Bishop(2, 'black'), Bishop(5, 'black')]
    bishops = white_bishops + black_bishops
    return bishops

def create_rooks():
    white_rooks = [Rook(0, 'white'), Rook(7, 'white')]
    black_rooks = [Rook(0, 'black'), Rook(7, 'black')]
    rooks = white_rooks+ black_rooks
    return rooks 

def create_queens():
    queens = [Queen(3, 'white'), Queen(3, 'black')]
    return queens

def create_kings():
    kings = [King(4, 'white'), King(4, 'black')]
    return kings 
