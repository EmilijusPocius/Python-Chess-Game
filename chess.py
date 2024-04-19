import pygame
from abc import ABC, abstractmethod
from images import w_images, b_images, board_image
from itertools import chain
import time

class Pieces(ABC):
    def __init__(self, position, color, image):
        self.position = position
        self.__image = image
        self.color = color
        self.move_list = []
    
    def draw(self):
        screen.blit(self.__image, (self.position[0] * 60 + 20, self.position[1] * 60 + 20))

    @abstractmethod
    def available_moves(self, w_pieces, b_pieces):
        pass

    @abstractmethod
    def checking_moves(self, w_pieces, b_pieces):
        pass

class Pawn(Pieces):
    def __init__(self, position, color, image):
        super().__init__(position, color, image)
        self.can_get_en_passant = False
        self.upgrade_name_index = self.position[0] + 1

    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []
        (x, y) = self.position

        #White Pawns
        if self.color == "w":
            #Moving
            if y == 6 and (x, y-1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces] \
                and (x, y-2) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                self.position = (x, y-2)
                if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append(self.position)
                self.position = (x, y)
            if (x, y-1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                self.position = (x, y-1)
                if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append(self.position)
                self.position = (x, y)
            #Taking
            for piece in b_pieces:
                if (x-1, y-1) == (piece.position[0], piece.position[1]):
                    self.position = (x-1, y-1)
                    piece_original_position = piece.position
                    piece.position = (-10, -10)
                    if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                        available_moves_list.append(self.position)
                    self.position = (x, y)
                    piece.position = piece_original_position
                if (x+1, y-1) == (piece.position[0], piece.position[1]):
                    self.position = (x+1, y-1)
                    piece_original_position = piece.position
                    piece.position = (-10, -10)
                    if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                        available_moves_list.append(self.position)
                    self.position = (x, y)
                    piece.position = piece_original_position
                #En passant
                if isinstance(piece, Pawn) and piece.can_get_en_passant == True:
                    if (x-1, y) == (piece.position[0], piece.position[1]):
                        self.position = (x-1, y-1)
                        piece_original_position = piece.position
                        piece.position = (-10, -10)
                        if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                            available_moves_list.append(self.position)
                        self.position = (x, y)
                        piece.position = piece_original_position
                    if (x+1, y) == (piece.position[0], piece.position[1]):
                        self.position = (x+1, y-1)
                        piece_original_position = piece.position
                        piece.position = (-10, -10)
                        if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                            available_moves_list.append(self.position)
                        self.position = (x, y)
                        piece.position = piece_original_position
        #Black Pawns
        if self.color == "b":
            #Moving
            if y == 1 and (x, y+1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces] \
                and (x, y+2) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                self.position = (x, y+2)
                if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append(self.position)
                self.position = (x, y)
            if (x, y+1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                self.position = (x, y+1)
                if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append(self.position)
                self.position = (x, y)
            #Taking
            for piece in w_pieces:
                if (x-1, y+1) == (piece.position[0], piece.position[1]):
                    self.position = (x-1, y+1)
                    piece_original_position = piece.position
                    piece.position = (-10, -10)
                    if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                        available_moves_list.append(self.position)
                    self.position = (x, y)
                    piece.position = piece_original_position
                if (x+1, y+1) == (piece.position[0], piece.position[1]):
                    self.position = (x+1, y+1)
                    piece_original_position = piece.position
                    piece.position = (-10, -10)
                    if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                        available_moves_list.append(self.position)
                    self.position = (x, y)
                    piece.position = piece_original_position
                #En passant
                if isinstance(piece, Pawn) and piece.can_get_en_passant == True:
                    if (x-1, y) == (piece.position[0], piece.position[1]):
                        self.position = (x-1, y+1)
                        piece_original_position = piece.position
                        piece.position = (-10, -10)
                        if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                            available_moves_list.append(self.position)
                        self.position = (x, y)
                        piece.position = piece_original_position
                    if (x+1, y) == (piece.position[0], piece.position[1]):
                        self.position = (x+1, y+1)
                        piece_original_position = piece.position
                        piece.position = (-10, -10)
                        if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                            available_moves_list.append(self.position)
                        self.position = (x, y)
                        piece.position = piece_original_position
        
        return available_moves_list

    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        (x, y) = self.position
        if self.color == "w":
            checking_moves_list.append((x-1, y-1))
            checking_moves_list.append((x+1, y-1))
        elif self.color == "b":
            checking_moves_list.append((x-1, y+1))
            checking_moves_list.append((x+1, y+1))
        
        return checking_moves_list

class Rook(Pieces):
    def __init__(self, position, color, image):
        super().__init__(position, color, image)
        self.can_castle = False
        if self.color == "w" and self.position[1] == 7:
            self.can_castle = True
        elif self.color == "b" and self.position[1] == 0:
            self.can_castle = True

    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        original_position = self.position
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            to_break = False
            while 0 <= x <= 7 and 0 <= y <= 7:
                for piece in w_pieces + b_pieces:
                    if (x, y) == piece.position:
                        if piece.color == self.color:
                            to_break = True
                            break
                        else:
                            piece_original_position = piece.position
                            piece.position = (-10, -10)
                            self.position = (x, y)
                            if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            piece.position = piece_original_position
                            self.position = original_position
                            to_break = True
                            break

                if to_break:
                    break

                self.position = (x, y)
                if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append((x, y))
                self.position = original_position

                x += direction_x
                y += direction_y
                
        return available_moves_list
    
    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            while 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                    checking_moves_list.append((x, y))
                    break
                checking_moves_list.append((x, y))
                x += direction_x
                y += direction_y
        return checking_moves_list

class Knight(Pieces):
    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []

        directions = [(1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)]
        original_position = self.position
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            if 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                    self.position = (x, y)
                    if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                        available_moves_list.append((x, y))
                    self.position = original_position
                elif self.color == "w" and (x, y) in [(piece.position[0], piece.position[1]) for piece in b_pieces]:
                    for piece in b_pieces:
                        if piece.position == (x, y):
                            piece_original_position = piece.position
                            piece.position = (-10, -10)
                            self.position = (x, y)
                            if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            piece.position = piece_original_position
                            self.position = original_position
                elif self.color == "b" and (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces]:
                     for piece in w_pieces:
                        if piece.position == (x, y):
                            piece_original_position = piece.position
                            piece.position = (-10, -10)
                            self.position = (x, y)
                            if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            piece.position = piece_original_position
                            self.position = original_position

        return available_moves_list
    
    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        directions = [(1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            if 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                    checking_moves_list.append((x, y))
                elif self.color == "w" and (x, y) in [(piece.position[0], piece.position[1]) for piece in b_pieces]:
                    checking_moves_list.append((x, y))
                elif self.color == "b" and (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces]:
                    checking_moves_list.append((x, y))
        return checking_moves_list

class Bishop(Pieces):
    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []

        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        original_position = self.position
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            to_break = False
            while 0 <= x <= 7 and 0 <= y <= 7:
                for piece in w_pieces + b_pieces:
                    if (x, y) == piece.position:
                        if piece.color == self.color:
                            to_break = True
                            break
                        else:
                            piece_original_position = piece.position
                            piece.position = (-10, -10)
                            self.position = (x, y)
                            if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            piece.position = piece_original_position
                            self.position = original_position
                            to_break = True
                            break

                if to_break:
                    break

                self.position = (x, y)
                if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append((x, y))
                self.position = original_position

                x += direction_x
                y += direction_y
                
        return available_moves_list
    
    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            while 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                    checking_moves_list.append((x, y))
                    break
                checking_moves_list.append((x, y))
                x += direction_x
                y += direction_y
        return checking_moves_list

class Queen(Pieces):
    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        original_position = self.position
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            to_break = False
            while 0 <= x <= 7 and 0 <= y <= 7:
                for piece in w_pieces + b_pieces:
                    if (x, y) == piece.position:
                        if piece.color == self.color:
                            to_break = True
                            break
                        else:
                            piece_original_position = piece.position
                            piece.position = (-10, -10)
                            self.position = (x, y)
                            if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            piece.position = piece_original_position
                            self.position = original_position
                            to_break = True
                            break

                if to_break:
                    break

                self.position = (x, y)
                if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
                    available_moves_list.append((x, y))
                self.position = original_position

                x += direction_x
                y += direction_y
                
        return available_moves_list
    
    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            while 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                    checking_moves_list.append((x, y))
                    break
                checking_moves_list.append((x, y))
                x += direction_x
                y += direction_y
        return checking_moves_list

class King(Pieces):
    def __init__(self, position, color, image):
        super().__init__(position, color, image)
        self.can_castle = True

    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []

        if self.color == "w":
            all_black_checking_moves_list = []
            all_black_checking_moves_list = all_black_checking_moves(w_pieces, b_pieces)
            all_black_checking_moves_list = list(chain.from_iterable(all_black_checking_moves_list))
        elif self.color == "b":
            all_white_checking_moves_list = []
            all_white_checking_moves_list = all_white_checking_moves(w_pieces, b_pieces)
            all_white_checking_moves_list = list(chain.from_iterable(all_white_checking_moves_list))

        original_position = self.position
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            if 0 <= x <= 7 and 0 <= y <= 7:
                if self.color == "w":
                    if (x, y) not in all_black_checking_moves_list:
                        if (x, y) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                            self.position = (x, y)
                            if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            self.position = original_position
                        elif (x, y) in [(piece.position[0], piece.position[1]) for piece in b_pieces]:
                            for piece in b_pieces:
                                if (x, y) == piece.position:
                                    self.position = (x, y)
                                    if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                        available_moves_list.append((x, y))
                                    self.position = original_position
                elif self.color == "b":
                    if (x, y) not in all_white_checking_moves_list:
                        if (x, y) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                            self.position = (x, y)
                            if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            self.position = original_position
                        elif (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces]:
                            self.position = (x, y)
                            if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                available_moves_list.append((x, y))
                            self.position = original_position
        #Castling
        if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king) and self.can_castle:
            directions = [(-1, 0), (1, 0)]
            for direction_x, direction_y in directions:
                x, y = self.position[0] + direction_x, self.position[1] + direction_y
                to_break = False
                while 0 <= x <= 7 and 0 <= y <= 7:
                    for piece in w_pieces + b_pieces:
                        if (x, y) == piece.position:
                            if isinstance(piece, Rook):
                                if self.color == "w" and piece.color == "w" and piece.can_castle:
                                    if piece.position[0] < self.position[0]:
                                        self.position = (original_position[0] - 1, original_position[1])
                                        if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                            self.position = (original_position[0] - 2, original_position[1])
                                            if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                                available_moves_list.append((original_position[0] - 2, original_position[1]))
                                    if piece.position[0] > self.position[0]:
                                        self.position = (original_position[0] + 1, original_position[1])
                                        if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                            self.position = (original_position[0] + 2, original_position[1])
                                            if not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                                                available_moves_list.append((original_position[0] + 2, original_position[1]))
                                    self.position = original_position

                                elif self.color == "b" and piece.color == "b" and piece.can_castle:
                                    if piece.position[0] < self.position[0]:
                                        self.position = (original_position[0] - 1, original_position[1])
                                        if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                            self.position = (original_position[0] - 2, original_position[1])
                                            if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                                available_moves_list.append((original_position[0] - 2, original_position[1]))
                                    if piece.position[0] > self.position[0]:
                                        self.position = (original_position[0] + 1, original_position[1])
                                        if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                            self.position = (original_position[0] + 2, original_position[1])
                                            if not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                                                available_moves_list.append((original_position[0] + 2, original_position[1]))
                                    self.position = original_position
                            else:
                                to_break = True
                                break

                    if to_break:
                        break

                    x += direction_x
                    y += direction_y

        return available_moves_list
    
    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for direction_x, direction_y in directions:
            x, y = self.position[0] + direction_x, self.position[1] + direction_y
            if 0 <= x <= 7 and 0 <= y <= 7:
                checking_moves_list.append((x, y))
        return checking_moves_list

class PieceFactory:
    @staticmethod
    def create_piece(piece_type, position, color, image):
        if piece_type == 'Pawn':
            return Pawn(position, color, image)
        elif piece_type == 'Rook':
            return Rook(position, color, image)
        elif piece_type == 'Knight':
            return Knight(position, color, image)
        elif piece_type == 'Bishop':
            return Bishop(position, color, image)
        elif piece_type == 'Queen':
            return Queen(position, color, image)
        elif piece_type == 'King':
            return King(position, color, image)
        else:
            raise ValueError(f"Unknown piece type: {piece_type}")

w_pawn1   = PieceFactory.create_piece('Pawn', (0, 6), "w", w_images[0])
w_pawn2   = PieceFactory.create_piece('Pawn', (1, 6), "w", w_images[0])
w_pawn3   = PieceFactory.create_piece('Pawn', (2, 6), "w", w_images[0])
w_pawn4   = PieceFactory.create_piece('Pawn', (3, 6), "w", w_images[0])
w_pawn5   = PieceFactory.create_piece('Pawn', (4, 6), "w", w_images[0])
w_pawn6   = PieceFactory.create_piece('Pawn', (5, 6), "w", w_images[0])
w_pawn7   = PieceFactory.create_piece('Pawn', (6, 6), "w", w_images[0])
w_pawn8   = PieceFactory.create_piece('Pawn', (7, 6), "w", w_images[0])
w_rook1   = PieceFactory.create_piece('Rook', (0, 7), "w", w_images[1])
w_rook2   = PieceFactory.create_piece('Rook', (7, 7), "w", w_images[1])
w_knight1 = PieceFactory.create_piece('Knight', (1, 7), "w", w_images[2])
w_knight2 = PieceFactory.create_piece('Knight', (6, 7), "w", w_images[2])
w_bishop1 = PieceFactory.create_piece('Bishop', (2, 7), "w", w_images[3])
w_bishop2 = PieceFactory.create_piece('Bishop', (5, 7), "w", w_images[3])
w_queen   = PieceFactory.create_piece('Queen', (3, 7), "w", w_images[4])
w_king    = PieceFactory.create_piece('King', (4, 7), "w", w_images[5])
w_pieces = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8, w_rook1,
w_rook2, w_knight1, w_knight2, w_bishop1, w_bishop2, w_queen, w_king]

b_pawn1   = PieceFactory.create_piece('Pawn', (0, 1), "b", b_images[0])
b_pawn2   = PieceFactory.create_piece('Pawn', (1, 1), "b", b_images[0])
b_pawn3   = PieceFactory.create_piece('Pawn', (2, 1), "b", b_images[0])
b_pawn4   = PieceFactory.create_piece('Pawn', (3, 1), "b", b_images[0])
b_pawn5   = PieceFactory.create_piece('Pawn', (4, 1), "b", b_images[0])
b_pawn6   = PieceFactory.create_piece('Pawn', (5, 1), "b", b_images[0])
b_pawn7   = PieceFactory.create_piece('Pawn', (6, 1), "b", b_images[0])
b_pawn8   = PieceFactory.create_piece('Pawn', (7, 1), "b", b_images[0])
b_rook1   = PieceFactory.create_piece('Rook', (0, 0), "b", b_images[1])
b_rook2   = PieceFactory.create_piece('Rook', (7, 0), "b", b_images[1])
b_knight1 = PieceFactory.create_piece('Knight', (1, 0), "b", b_images[2])
b_knight2 = PieceFactory.create_piece('Knight', (6, 0), "b", b_images[2])
b_bishop1 = PieceFactory.create_piece('Bishop', (2, 0), "b", b_images[3])
b_bishop2 = PieceFactory.create_piece('Bishop', (5, 0), "b", b_images[3])
b_queen   = PieceFactory.create_piece('Queen', (3, 0), "b", b_images[4])
b_king    = PieceFactory.create_piece('King', (4, 0), "b", b_images[5])
b_pieces = [b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8, b_rook1,
b_rook2, b_knight1, b_knight2, b_bishop1, b_bishop2, b_queen, b_king]

def draw_game(selected_piece, available_moves, checked_king_position, draw_white_picks, draw_black_picks, white_win, black_win, stalemate):
    screen.blit(board_image, (0, 0)) 

    if available_moves is not None:
        if selected_piece.color == "w":
            color = (255, 255, 255, 128)
        elif selected_piece.color == "b":
            color = (0, 0, 0, 64)
        transparent_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        transparent_surface.fill(color)
        for move in available_moves:
            screen.blit(transparent_surface, (move[0] * 60 + 20, move[1] * 60 + 20))
            pygame.draw.rect(screen, color, (move[0] * 60 + 20 - 1, move[1] * 60 + 20 - 1, 60 + 2, 60 + 2), 2)
    if checked_king_position != (-10, -10):
        pygame.draw.rect(screen, (255, 0, 0), (checked_king_position[0] * 60 + 20 - 1, checked_king_position[1] * 60 + 20 - 1, 60 + 2, 60 + 2), 2)
    
    for piece in w_pieces + b_pieces:
        piece.draw()
    if selected_piece is not None:
        selected_piece.draw()

    if draw_white_picks:
        pygame.draw.rect(screen, (100, 60, 30), (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 30, 60*4, 60))
        for i in range(60, 181, 60):
            pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - 120 + i - 1, SCREEN_HEIGHT / 2 - 30), (SCREEN_WIDTH / 2 - 120 + i - 1, SCREEN_HEIGHT / 2 - 30 + 59), 2)
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 30, 60*4, 60), 3)
        image_index = 1
        for i in range(0, 181, 60):
            screen.blit(w_images[image_index], (SCREEN_WIDTH / 2 - 120 + i, SCREEN_HEIGHT / 2 - 30))
            image_index += 1

    if draw_black_picks:
        pygame.draw.rect(screen, (100, 60, 30), (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 30, 60*4, 60))
        for i in range(60, 181, 60):
            pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - 120 + i - 1, SCREEN_HEIGHT / 2 - 30), (SCREEN_WIDTH / 2 - 120 + i - 1, SCREEN_HEIGHT / 2 - 30 + 59), 2)
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 30, 60*4, 60), 3)
        image_index = 1
        for i in range(0, 181, 60):
            screen.blit(b_images[image_index], (SCREEN_WIDTH / 2 - 120 + i, SCREEN_HEIGHT / 2 - 30))
            image_index += 1

    if white_win or black_win or stalemate:
        if white_win:
            text = my_font.render("White Win", True, (0, 0, 0))
        elif black_win:
            text = my_font.render("Black Win", True, (0, 0, 0))
        elif stalemate:
            text = my_font.render("Stalemate", True, (0, 0, 0))

        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        text_background = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
        text_background.fill((250, 200, 125))
        text_background_rect = text_background.get_rect()
        text_background_rect.center = text_rect.center

        screen.blit(text_background, text_background_rect)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (0, 0, 0), text_background_rect, 4)


    pygame.display.flip()

def all_black_checking_moves(w_pieces, b_pieces):
    all_black_checking_moves_list = []
    for piece in b_pieces:
        all_black_checking_moves_list.append(piece.checking_moves(w_pieces, b_pieces))
    return all_black_checking_moves_list

def all_white_checking_moves(w_pieces, b_pieces):
    all_white_checking_moves_list = []
    for piece in w_pieces:
        all_white_checking_moves_list.append(piece.checking_moves(w_pieces, b_pieces))
    return all_white_checking_moves_list

def king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
    if white_turn:
        all_black_checking_moves_list = all_black_checking_moves(w_pieces, b_pieces)
        all_black_checking_moves_list = list(chain.from_iterable(all_black_checking_moves_list))
        x, y = w_king.position[0], w_king.position[1]
        return True if (x, y) in all_black_checking_moves_list else False

    elif not white_turn:
        all_white_checking_moves_list = all_white_checking_moves(w_pieces, b_pieces)
        all_white_checking_moves_list = list(chain.from_iterable(all_white_checking_moves_list))
        x, y = b_king.position[0], b_king.position[1]
        return True if (x, y) in all_white_checking_moves_list else False

def reset_can_get_en_passant(white_turn, w_pecies, b_pecies):
    if white_turn:
        for piece in w_pieces:
            if isinstance(piece, Pawn):
                piece.can_get_en_passant = False
    elif not white_turn:
        for piece in b_pieces:
            if isinstance(piece, Pawn):
                piece.can_get_en_passant = False

def upgrade_pawn(w_pieces, b_pieces, upgrade_index):
    upgraded_pieces = {}
    for piece in w_pieces + b_pieces:
        if isinstance(piece, Pawn) and (piece.position[1] == 0 or piece.position[1] == 7):
            key = f"upgraded_{piece.color}_pawn_{piece.upgrade_name_index}"
            if upgrade_index == 1:
                upgraded_pieces[key] = Rook((piece.position), piece.color, (w_images[upgrade_index] if piece.color == "w" else b_images[upgrade_index]))
            elif upgrade_index == 2:
                upgraded_pieces[key] = Knight((piece.position), piece.color, (w_images[upgrade_index] if piece.color == "w" else b_images[upgrade_index]))
            elif upgrade_index == 3:
                upgraded_pieces[key] = Bishop((piece.position), piece.color, (w_images[upgrade_index] if piece.color == "w" else b_images[upgrade_index]))
            elif upgrade_index == 4:
                upgraded_pieces[key] = Queen((piece.position), piece.color, (w_images[upgrade_index] if piece.color == "w" else b_images[upgrade_index]))
            if piece.color == "w":
                w_pieces.append(upgraded_pieces[key])
                w_pieces.remove(piece)
            elif piece.color == "b":
                b_pieces.append(upgraded_pieces[key])
                b_pieces.remove(piece)

def game_information(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        white_move_count, black_move_count, white_win, black_win, stalemate = func(*args, **kwargs)
        end = time.time()
        seconds = end - start
        minutes = seconds // 60
        seconds %= 60
        seconds = round(seconds)
        with open("game_info.txt", "w") as file:
            file.write(f"The game was running for {minutes} minutes and {seconds} seconds.\n")
            file.write(f"White move count: {white_move_count}, Black move count: {black_move_count}\n")
            if white_win:
                file.write(f"Winner: White\n")
            elif black_win:
                file.write(f"Winner: Black\n")
            elif stalemate:
                file.write(f"Game was a stalemate\n")
            else:
                file.write(f"Game was not finished.\n")
    return wrapper

@game_information
def main():
    running = True
    white_turn = True
    selected_piece = None
    original_position = None
    available_moves = None
    draw_white_picks = False
    draw_black_picks = False
    white_win = False
    black_win = False
    stalemate = False
    checked_king_position = (-10, -10)
    white_move_count = 0
    black_move_count = 0
    while running:
        draw_game(selected_piece, available_moves, checked_king_position, draw_white_picks, draw_black_picks, white_win, black_win, stalemate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return white_move_count, black_move_count, white_win, black_win, stalemate
            if not (white_win or black_win or stalemate):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not (draw_white_picks or draw_black_picks):
                            if white_turn:
                                for piece in w_pieces:
                                    if  piece.position[0] * 60 + 20 <= event.pos[0] <= piece.position[0] * 60 + 60 + 20 \
                                    and piece.position[1] * 60 + 20 <= event.pos[1] <= piece.position[1] * 60 + 60 + 20:
                                        selected_piece = piece
                                        original_position = selected_piece.position
                                        available_moves = selected_piece.available_moves(w_pieces, b_pieces)

                            if not white_turn:
                                for piece in b_pieces:
                                    if  piece.position[0] * 60 + 20 <= event.pos[0] <= piece.position[0] * 60 + 60 + 20 \
                                    and piece.position[1] * 60 + 20 <= event.pos[1] <= piece.position[1] * 60 + 60 + 20:
                                        selected_piece = piece
                                        original_position = selected_piece.position
                                        available_moves = selected_piece.available_moves(w_pieces, b_pieces)
                                        break
                        else:
                            upgrade_index = 1
                            for i in range(0, 181, 60):
                                if (SCREEN_WIDTH / 2 - 120 + i) < event.pos[0] < (SCREEN_WIDTH / 2 - 120 + i + 60) \
                                and (SCREEN_HEIGHT / 2 - 30) < event.pos[1] < (SCREEN_HEIGHT / 2 - 30 + 60):
                                    upgrade_pawn(w_pieces, b_pieces, upgrade_index)
                                    draw_white_picks = False
                                    draw_black_picks = False
                                upgrade_index += 1

                            if white_turn:
                                if king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
                                    checked_king_position = w_king.position
                                else:
                                    checked_king_position = (-10, -10)
                            elif not white_turn:
                                if king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
                                    checked_king_position = b_king.position
                                else:
                                    checked_king_position = (-10, -10)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and selected_piece is not None:
                        move_to_position = ((event.pos[0] - 20) // 60), ((event.pos[1] - 20) // 60)
                        if move_to_position in available_moves:
                            if isinstance(selected_piece, Pawn):
                                if selected_piece.color == "w":
                                    if original_position[1] == 6 and move_to_position[1] == 4:
                                        selected_piece.can_get_en_passant = True 
                                    elif move_to_position[1] == 0:
                                        draw_white_picks = True
                                elif selected_piece.color == "b":
                                    if original_position[1] == 1 and move_to_position[1] == 3:
                                        selected_piece.can_get_en_passant = True 
                                    elif move_to_position[1] == 7:
                                        draw_black_picks = True
                            elif isinstance(selected_piece, Rook):
                                selected_piece.can_castle = False
                            elif isinstance(selected_piece, King):
                                if selected_piece.can_castle:
                                    if selected_piece.color == "w":
                                        if move_to_position[0] == 2:
                                            for piece in w_pieces:
                                                if isinstance(piece, Rook) and piece.position[0] < move_to_position[0]:
                                                    piece.position = ((move_to_position[0] + 1, move_to_position[1]))
                                                    piece.can_castle = False
                                                    break
                                        elif move_to_position[0] == 6:
                                            for piece in w_pieces:
                                                if isinstance(piece, Rook) and piece.position[0] > move_to_position[0]:
                                                    piece.position = ((move_to_position[0] - 1, move_to_position[1]))
                                                    piece.can_castle = False
                                                    break
                                    elif selected_piece.color == "b":
                                        if move_to_position[0] == 2:
                                            for piece in b_pieces:
                                                if isinstance(piece, Rook) and piece.position[0] < move_to_position[0]:
                                                    piece.position = ((move_to_position[0] + 1, move_to_position[1]))
                                                    piece.can_castle = False
                                                    break
                                        elif move_to_position[0] == 6:
                                            for piece in b_pieces:
                                                if isinstance(piece, Rook) and piece.position[0] > move_to_position[0]:
                                                    piece.position = ((move_to_position[0] - 1, move_to_position[1]))
                                                    piece.can_castle = False
                                                    break
                                selected_piece.can_castle = False

                            selected_piece.position = move_to_position
                            for piece in w_pieces + b_pieces:
                                if piece.position == move_to_position and piece is not selected_piece:
                                    w_pieces.remove(piece) if piece in w_pieces else b_pieces.remove(piece)
                                if isinstance(piece, Pawn) and isinstance(selected_piece, Pawn) and piece.can_get_en_passant:
                                    if piece.color == "w":
                                        if piece.position == (move_to_position[0], move_to_position[1] - 1):
                                            w_pieces.remove(piece)
                                    elif piece.color == "b":
                                        if piece.position == (move_to_position[0], move_to_position[1] + 1):
                                            b_pieces.remove(piece)
                            white_move_count += 1 if white_turn else 0
                            black_move_count += 1 if not white_turn else 0
                            white_turn = not white_turn
                            if white_turn:
                                if king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
                                    checked_king_position = w_king.position
                                else:
                                    checked_king_position = (-10, -10)
                            elif not white_turn:
                                if king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
                                    checked_king_position = b_king.position
                                else:
                                    checked_king_position = (-10, -10)
                            reset_can_get_en_passant(white_turn, w_pieces, b_pieces)
                        else:
                            selected_piece.position = original_position

                        available_moves = None
                        selected_piece = None

        if selected_piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_piece.position = (mouse_x - 50) / 60, (mouse_y - 50) / 60
            if (mouse_x < 20 or mouse_x > 480 + 20 or mouse_y < 20 or mouse_y > 480 + 20):
                selected_piece.position = original_position
                available_moves = None
                selected_piece = None
        
        if white_turn:
            all_available_moves = []
            for piece in w_pieces:
                all_available_moves.append(piece.available_moves(w_pieces, b_pieces))
            if not any(all_available_moves) and king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                black_win = True
            elif not any(all_available_moves) and not king_in_check(True, w_pieces, b_pieces, w_king, b_king):
                stalemate = True
        elif not white_turn:
            all_available_moves = []
            for piece in b_pieces:
                all_available_moves.append(piece.available_moves(w_pieces, b_pieces))
            if not any(all_available_moves) and king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                white_win = True
            elif not any(all_available_moves) and not king_in_check(False, w_pieces, b_pieces, w_king, b_king):
                stalemate = True

        clock.tick(60) 
    
pygame.init()
pygame.font.init() 
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
my_font = pygame.font.SysFont('Gill Sans', 100)
pygame.display.set_caption("Chess")
pygame.display.set_icon(b_images[2])
clock = pygame.time.Clock()
main()
pygame.quit()