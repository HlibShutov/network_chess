import pygame

class Piece():
    def move(self, new_x, new_y, capture, coordinates):
        if self._validate_move(new_x, new_y, coordinates) and ((new_x, new_y) not in coordinates or ((new_x, new_y) in coordinates and capture == True)):
            self.x = new_x
            self.y = new_y
            self.rect = self.image.get_rect(center=(self.x*50+25, self.y*50+25))
            return True
        else: return False
class Pawn(pygame.sprite.Sprite):
    def __init__(self, file, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = file
        self.y = 1 if color == 'black' else 6
        self.moved_two_squares = False
        self.__enpassant = 0
        if color == 'white':
            self.image = pygame.image.load('images/white_pawn.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, 325))
        elif color == 'black':
            self.image = pygame.image.load('images/black_pawn.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, 75))

    def move(self, new_x, new_y, capture, coordinates):
        if self._validate_move(new_x, new_y, capture, coordinates):
            #if (self.color == 'white' and (self.x, self.y-1) not in coordinates) or (self.color == 'black' and (self.x, self.y+1) not in coordinates):

                if self.y-2 == new_y or self.y+2 == new_y:
                    self.__enpassant = 2
                self.x = new_x
                self.y = new_y
                self.moved_two_squares = True
                self.rect = self.image.get_rect(center=(self.x*50+25, self.y*50+25))
                return True
        else:
            print('incrorrect;')
            return False

    def get_enpassant(self):
        return bool(self.__enpassant)

    def subbstract_enpassant(self):
        if self.__enpassant > 0: self.__enpassant -= 1

    def _validate_move(self, new_x, new_y, capture, coordinates):
        direction = -1 if self.color == 'white' else 1
        if not capture and (self.x, self.y+direction) in coordinates: 
            return False 
        elif not self.moved_two_squares and not capture and new_x == self.x and new_y == self.y + direction*2 and (self.x, self.y + direction*2) not in coordinates: 
            return True 
        elif not capture and new_x == self.x and new_y == self.y + direction: 
            return True 
        elif capture and new_y == self.y + direction and abs(new_x - self.x) == 1: 
            return True 
        return False 

class Knight(pygame.sprite.Sprite, Piece):
    def __init__(self, file, color, y = None):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = file
        if y == None:
            self.y = 0 if color == 'black' else 7
        else: self.y = y
        if color == 'white':
            self.image = pygame.image.load('images/white_knight.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, self.y*50+25))
        elif color == 'black':
            self.image = pygame.image.load('images/black_knight.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, self.y*50+25))

    def _validate_move(self, new_x, new_y, coordinates):
        if ((abs(new_x - self.x) == 2 and abs(new_y - self.y) == 1) or (abs(new_x - self.x) == 1 and abs(new_y - self.y) == 2)): 
            return True
        else:
            return False

class Bishop(pygame.sprite.Sprite, Piece):
    def __init__(self, file, color, y = None):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = file
        if y == None:
            self.y = 0 if color == 'black' else 7
        else: self.y = y
        if color == 'white':
            self.image = pygame.image.load('images/white_bishop.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, self.y*50+25))
        elif color == 'black':
            self.image = pygame.image.load('images/black_bishop.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, self.y*50+25))
    def _validate_move(self, new_x, new_y, coordinates):
        if self.is_path_clear(new_x, new_y, coordinates) and abs(new_x - self.x) == abs(new_y - self.y):
            return True
        else:
            return False
    def is_path_clear(self, new_x, new_y, coordinates):
        x, y = self.x, self.y
        x_step = 1 if new_x > self.x else -1
        y_step = 1 if new_y > self.y else -1 
        while x != new_x and y != new_y:
            x+=x_step
            y+=y_step
            if (x, y) in coordinates:
                return False
        return True

class Rook(pygame.sprite.Sprite, Piece):
    def __init__(self, file, color, y = None):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = file
        if y == None:
            self.y = 0 if color == 'black' else 7
        else: self.y = y
        if color == 'white':
            self.image = pygame.image.load('images/white_rook.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, self.y*50+25))
        elif color == 'black':
            self.image = pygame.image.load('images/black_rook.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, self.y*50+25))
    def _validate_move(self, new_x, new_y, coordinates):
        if self.is_path_clear(new_x, new_y, coordinates):
            return True
        else:
            return False
    def is_path_clear(self, new_x, new_y, coordinates):
        x, y = self.x, self.y
        x_step = 0
        y_step = 0
        if new_x != self.x and new_y == self.y: 
            x_step = 1 if new_x > self.x else -1
        elif new_x == self.x and new_y != self.y:
            y_step = 1 if new_y > self.y else -1 
        else: return False
        x+=x_step
        y+=y_step
        while (x, y) != (new_x, new_y): 
            if (x, y) in coordinates:
                return False
            x+=x_step
            y+=y_step
        return True

class Queen(pygame.sprite.Sprite, Piece):
    def __init__(self, file, color, y = None):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = file
        if y == None:
            self.y = 0 if color == 'black' else 7
        else: self.y = y
        if color == 'white':
            self.image = pygame.image.load('images/white_queen.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, self.y*50+25))
        elif color == 'black':
            self.image = pygame.image.load('images/black_queen.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, self.y*50+25))
    def _validate_move(self, new_x, new_y, coordinates):
        if Bishop._validate_move(self, new_x, new_y, coordinates) or Rook.is_path_clear(self, new_x, new_y, coordinates):
            return True
        else: return False
    def is_path_clear(self, new_x, new_y, coordinates):
        return Bishop.is_path_clear(self, new_x, new_y, coordinates)

class King(pygame.sprite.Sprite):
    def __init__(self, file, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.long_castle = True
        self.short_castle = True
        self.x = file
        self.y = 0 if color == 'black' else 7
        if color == 'white':
            self.image = pygame.image.load('images/white_king.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file*50+25, 375))
        elif color == 'black':
            self.image = pygame.image.load('images/black_king.png').convert_alpha()
            self.rect = self.image.get_rect(center=(file * 50 + 25, 25))
    def move(self, new_x, new_y, capture, coordinates, pieces):
        is_move_valide = self._validate_move(new_x, new_y, capture, coordinates, pieces)
        if is_move_valide:
            self.x = new_x
            self.y = new_y
            self.rect = self.image.get_rect(center=(self.x*50+25, self.y*50+25))
            self.short_castle = False
            self.long_castle = False
            return is_move_valide
        else: return False
    def _validate_move(self, new_x, new_y, capture, coordinates, pieces):
        if (new_x, new_y) not in self.get_threatened_squares(pieces, coordinates) and (abs(new_x - self.x) <= 1 and abs(new_y - self.y) <= 1 or self.castle_available(new_x, new_y, coordinates, pieces)) and ((new_x, new_y) not in coordinates or ((new_x, new_y) in coordinates and capture == True)):
            if self.castle_available(new_x, new_y, coordinates, pieces):
                return 'short' if new_x == 6 else 'long'
            return True
        else: return False
    def get_threatened_squares(self, pieces, coordinates):
        threatened_squares = []
        for piece in pieces:
            if piece.color != self.color:
                for x in range(8):
                    for y in range(8):
                        if isinstance(piece, Pawn): 
                            if piece._validate_move(x, y, True, coordinates):
                                threatened_squares.append((x, y))
                                continue
                        elif isinstance(piece, King): 
                            if abs(x - piece.x) <= 1 and abs(y - piece.y) <= 1 and (x, y) not in coordinates: 
                                threatened_squares.append((x, y))
                                continue
                        else:
                            if piece._validate_move(x, y, coordinates):
                                threatened_squares.append((x, y))
        return set(threatened_squares)
    def castle_available(self, new_x, new_y, coordinates, pieces):
        if (self.x, self.y) in coordinates: coordinates.remove((self.x, self.y))
        threatened_squares = self.get_threatened_squares(pieces, coordinates)
        if (new_x == 6 and self.short_castle) or (new_x == 2 and self.long_castle):
            if new_y == self.y and (self.x, self.y) not in threatened_squares:
                if new_x == 6 and (5, new_y) not in threatened_squares: return True
                elif new_x == 2 and (3, new_y) not in threatened_squares and (2, new_y) not in threatened_squares and (3, new_y) not in coordinates: return True
        return False

