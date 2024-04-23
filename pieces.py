from abc import ABC, abstractmethod
from itertools import chain
from images import w_images, b_images

class Pieces(ABC):
    def __init__(self, position, color, image):
        self.position = position
        self.image = image
        self.color = color
        self.move_list = []

    @abstractmethod
    def available_moves(self, w_pieces, b_pieces):
        pass

    @abstractmethod
    def checking_moves(self, w_pieces, b_pieces):
        pass

    def _is_valid_move(self, w_pieces, b_pieces, new_position, original_position, enemy_piece):
        is_valid = False
        self.position = new_position
        if enemy_piece is not None:
            enemy_piece_original_position = enemy_piece.position
            enemy_piece.position = (-10, -10)
        if not king_in_check(True if self.color == "w" else False, w_pieces, b_pieces, w_king, b_king):
            is_valid = True
        self.position = original_position
        if enemy_piece is not None:
            enemy_piece.position = enemy_piece_original_position
    
        return is_valid

class Pawn(Pieces):
    def __init__(self, position, color, image):
        super().__init__(position, color, image)
        self.can_get_en_passant = False
        self.upgrade_name_index = self.position[0] + 1

    def available_moves(self, w_pieces, b_pieces):
        available_moves_list = []
        (x, y) = self.position

        # White Pawns
        if self.color == "w":
            # Moving
            if y == 6 and (x, y - 1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces] \
                and (x, y - 2) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                if self._is_valid_move(w_pieces, b_pieces, (x, y - 2), (x, y), None):
                    available_moves_list.append((x, y - 2))
            if (x, y - 1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                if self._is_valid_move(w_pieces, b_pieces, (x, y - 1), (x, y), None):
                    available_moves_list.append((x, y - 1))
            # Taking
            for piece in b_pieces:
                if (x - 1, y - 1) == (piece.position[0], piece.position[1]):
                    if self._is_valid_move(w_pieces, b_pieces, (x - 1, y - 1), (x, y), piece):
                        available_moves_list.append((x - 1, y - 1))
                if (x + 1, y - 1) == (piece.position[0], piece.position[1]):
                    if self._is_valid_move(w_pieces, b_pieces, (x + 1, y - 1), (x, y), piece):
                        available_moves_list.append((x + 1, y - 1))
                # En passant
                if isinstance(piece, Pawn) and piece.can_get_en_passant == True:
                    if (x - 1, y) == (piece.position[0], piece.position[1]):
                        if self._is_valid_move(w_pieces, b_pieces, (x - 1, y - 1), (x, y), piece):
                            available_moves_list.append((x - 1, y - 1))
                    if (x + 1, y) == (piece.position[0], piece.position[1]):
                        if self._is_valid_move(w_pieces, b_pieces, (x + 1, y - 1), (x, y), piece):
                            available_moves_list.append((x + 1, y - 1))
        # Black Pawns
        if self.color == "b":
            # Moving
            if y == 1 and (x, y + 1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces] \
                and (x, y + 2) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                if self._is_valid_move(w_pieces, b_pieces, (x, y + 2), (x, y), None):
                    available_moves_list.append((x, y + 2))
            if (x, y + 1) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                if self._is_valid_move(w_pieces, b_pieces, (x, y + 1), (x, y), None):
                    available_moves_list.append((x, y + 1))
            # Taking
            for piece in w_pieces:
                if (x - 1, y + 1) == (piece.position[0], piece.position[1]):
                    if self._is_valid_move(w_pieces, b_pieces, (x - 1, y + 1), (x, y), piece):
                        available_moves_list.append((x - 1, y + 1))
                if (x + 1, y + 1) == (piece.position[0], piece.position[1]):
                    if self._is_valid_move(w_pieces, b_pieces, (x + 1, y + 1), (x, y), piece):
                        available_moves_list.append((x + 1, y + 1))
                # En passant
                if isinstance(piece, Pawn) and piece.can_get_en_passant == True:
                    if (x - 1, y) == (piece.position[0], piece.position[1]):
                        if self._is_valid_move(w_pieces, b_pieces, (x - 1, y + 1), (x, y), piece):
                            available_moves_list.append((x - 1, y + 1))
                    if (x + 1, y) == (piece.position[0], piece.position[1]):
                        if self._is_valid_move(w_pieces, b_pieces, (x + 1, y + 1), (x, y), piece):
                            available_moves_list.append((x + 1, y + 1))

        return available_moves_list

    def checking_moves(self, w_pieces, b_pieces):
        checking_moves_list = []
        (x, y) = self.position
        if self.color == "w":
            checking_moves_list.append((x - 1, y - 1))
            checking_moves_list.append((x + 1, y - 1))
        elif self.color == "b":
            checking_moves_list.append((x - 1, y + 1))
            checking_moves_list.append((x + 1, y + 1))

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
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))
                            to_break = True
                            break
                if to_break:
                    break

                if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                    available_moves_list.append((x, y))

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
                    if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                        available_moves_list.append((x, y))
                elif self.color == "w" and (x, y) in [(piece.position[0], piece.position[1]) for piece in b_pieces]:
                    for piece in b_pieces:
                        if piece.position == (x, y):
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))
                elif self.color == "b" and (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces]:
                     for piece in w_pieces:
                        if piece.position == (x, y):
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))

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
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))
                            to_break = True
                            break
                if to_break:
                    break

                if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                    available_moves_list.append((x, y))

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
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))
                            to_break = True
                            break
                if to_break:
                    break

                if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                    available_moves_list.append((x, y))

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
            all_black_checking_moves_list = all_black_checking_moves(w_pieces, b_pieces)
            all_black_checking_moves_list = list(chain.from_iterable(all_black_checking_moves_list))
        elif self.color == "b":
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
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                                available_moves_list.append((x, y))
                        elif (x, y) in [(piece.position[0], piece.position[1]) for piece in b_pieces]:
                            for piece in b_pieces:
                                if (x, y) == piece.position:
                                    if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                        available_moves_list.append((x, y))
                elif self.color == "b":
                    if (x, y) not in all_white_checking_moves_list:
                        if (x, y) not in [(piece.position[0], piece.position[1]) for piece in w_pieces + b_pieces]:
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, None):
                                available_moves_list.append((x, y))
                        elif (x, y) in [(piece.position[0], piece.position[1]) for piece in w_pieces]:
                            if self._is_valid_move(w_pieces, b_pieces, (x, y), original_position, piece):
                                available_moves_list.append((x, y))
        # Castling
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
                                        if self._is_valid_move(w_pieces, b_pieces, (original_position[0] - 1, original_position[1]), original_position, None):
                                            if self._is_valid_move(w_pieces, b_pieces, (original_position[0] - 2, original_position[1]), original_position, None):
                                                available_moves_list.append((original_position[0] - 2, original_position[1]))
                                    if piece.position[0] > self.position[0]:
                                        if self._is_valid_move(w_pieces, b_pieces, (original_position[0] + 1, original_position[1]), original_position, None):
                                            if self._is_valid_move(w_pieces, b_pieces, (original_position[0] + 2, original_position[1]), original_position, None):
                                                available_moves_list.append((original_position[0] + 2, original_position[1]))

                                elif self.color == "b" and piece.color == "b" and piece.can_castle:
                                    if piece.position[0] < self.position[0]:
                                        if self._is_valid_move(w_pieces, b_pieces, (original_position[0] - 1, original_position[1]), original_position, None):
                                            if self._is_valid_move(w_pieces, b_pieces, (original_position[0] - 2, original_position[1]), original_position, None):
                                                available_moves_list.append((original_position[0] - 2, original_position[1]))
                                    if piece.position[0] > self.position[0]:
                                        if self._is_valid_move(w_pieces, b_pieces, (original_position[0] + 1, original_position[1]), original_position, None):
                                            if self._is_valid_move(w_pieces, b_pieces, (original_position[0] + 2, original_position[1]), original_position, None):
                                                available_moves_list.append((original_position[0] + 2, original_position[1]))
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

w_pawn1 = PieceFactory.create_piece('Pawn', (0, 6), "w", w_images[0])
w_pawn2 = PieceFactory.create_piece('Pawn', (1, 6), "w", w_images[0])
w_pawn3 = PieceFactory.create_piece('Pawn', (2, 6), "w", w_images[0])
w_pawn4 = PieceFactory.create_piece('Pawn', (3, 6), "w", w_images[0])
w_pawn5 = PieceFactory.create_piece('Pawn', (4, 6), "w", w_images[0])
w_pawn6 = PieceFactory.create_piece('Pawn', (5, 6), "w", w_images[0])
w_pawn7 = PieceFactory.create_piece('Pawn', (6, 6), "w", w_images[0])
w_pawn8 = PieceFactory.create_piece('Pawn', (7, 6), "w", w_images[0])
w_rook1 = PieceFactory.create_piece('Rook', (0, 7), "w", w_images[1])
w_rook2 = PieceFactory.create_piece('Rook', (7, 7), "w", w_images[1])
w_knight1 = PieceFactory.create_piece('Knight', (1, 7), "w", w_images[2])
w_knight2 = PieceFactory.create_piece('Knight', (6, 7), "w", w_images[2])
w_bishop1 = PieceFactory.create_piece('Bishop', (2, 7), "w", w_images[3])
w_bishop2 = PieceFactory.create_piece('Bishop', (5, 7), "w", w_images[3])
w_queen = PieceFactory.create_piece('Queen', (3, 7), "w", w_images[4])
w_king = PieceFactory.create_piece('King', (4, 7), "w", w_images[5])
w_pieces = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8, w_rook1,
            w_rook2, w_knight1, w_knight2, w_bishop1, w_bishop2, w_queen, w_king]

b_pawn1 = PieceFactory.create_piece('Pawn', (0, 1), "b", b_images[0])
b_pawn2 = PieceFactory.create_piece('Pawn', (1, 1), "b", b_images[0])
b_pawn3 = PieceFactory.create_piece('Pawn', (2, 1), "b", b_images[0])
b_pawn4 = PieceFactory.create_piece('Pawn', (3, 1), "b", b_images[0])
b_pawn5 = PieceFactory.create_piece('Pawn', (4, 1), "b", b_images[0])
b_pawn6 = PieceFactory.create_piece('Pawn', (5, 1), "b", b_images[0])
b_pawn7 = PieceFactory.create_piece('Pawn', (6, 1), "b", b_images[0])
b_pawn8 = PieceFactory.create_piece('Pawn', (7, 1), "b", b_images[0])
b_rook1 = PieceFactory.create_piece('Rook', (0, 0), "b", b_images[1])
b_rook2 = PieceFactory.create_piece('Rook', (7, 0), "b", b_images[1])
b_knight1 = PieceFactory.create_piece('Knight', (1, 0), "b", b_images[2])
b_knight2 = PieceFactory.create_piece('Knight', (6, 0), "b", b_images[2])
b_bishop1 = PieceFactory.create_piece('Bishop', (2, 0), "b", b_images[3])
b_bishop2 = PieceFactory.create_piece('Bishop', (5, 0), "b", b_images[3])
b_queen = PieceFactory.create_piece('Queen', (3, 0), "b", b_images[4])
b_king = PieceFactory.create_piece('King', (4, 0), "b", b_images[5])
b_pieces = [b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8, b_rook1,
            b_rook2, b_knight1, b_knight2, b_bishop1, b_bishop2, b_queen, b_king]

def upgrade_pawn(w_pieces, b_pieces, upgrade_index):
    upgraded_pieces = {}
    upgrade_mapping = {
        1: 'Rook',
        2: 'Knight',
        3: 'Bishop',
        4: 'Queen'
    }
    for piece in w_pieces + b_pieces:
        if isinstance(piece, Pawn) and (piece.position[1] == 0 or piece.position[1] == 7):
            upgrade_piece_type = upgrade_mapping.get(upgrade_index)
            key = f"upgraded_{piece.color}_pawn_{piece.upgrade_name_index}"
            upgraded_pieces[key] = PieceFactory.create_piece(upgrade_piece_type, piece.position, piece.color, (w_images[upgrade_index] if piece.color == "w" else b_images[upgrade_index]))
            if piece.color == "w":
                w_pieces.append(upgraded_pieces[key])
            elif piece.color == "b":
                b_pieces.append(upgraded_pieces[key])
            w_pieces.remove(piece) if piece in w_pieces else b_pieces.remove(piece)

def all_black_checking_moves(w_pieces, b_pieces):
    return [piece.checking_moves(w_pieces, b_pieces) for piece in b_pieces]

def all_white_checking_moves(w_pieces, b_pieces):
    return [piece.checking_moves(w_pieces, b_pieces) for piece in w_pieces]

def king_in_check(white_turn, w_pieces, b_pieces, w_king, b_king):
    if white_turn:
        all_black_checking_moves_list = all_black_checking_moves(w_pieces, b_pieces)
        all_black_checking_moves_list = list(chain.from_iterable(all_black_checking_moves_list))
        x, y = w_king.position[0], w_king.position[1]
        return (x, y) in all_black_checking_moves_list
    else:
        all_white_checking_moves_list = all_white_checking_moves(w_pieces, b_pieces)
        all_white_checking_moves_list = list(chain.from_iterable(all_white_checking_moves_list))
        x, y = b_king.position[0], b_king.position[1]
        return (x, y) in all_white_checking_moves_list

def reset_can_get_en_passant(white_turn, w_pieces, b_pieces):
    if white_turn:
        for piece in w_pieces:
            if isinstance(piece, Pawn):
                piece.can_get_en_passant = False
    elif not white_turn:
        for piece in b_pieces:
            if isinstance(piece, Pawn):
                piece.can_get_en_passant = False