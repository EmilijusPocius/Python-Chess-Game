import pygame
from abc import ABC, abstractmethod

board_image = pygame.image.load("chessboard.png")

w_pawn_image = pygame.image.load("w_pawn.png")
w_rook_image = pygame.image.load("w_rook.png")
w_knight_image = pygame.image.load("w_knight.png")
w_bishop_image = pygame.image.load("w_bishop.png")
w_queen_image = pygame.image.load("w_queen.png")
w_king_image = pygame.image.load("w_king.png")
w_images = [w_pawn_image, w_rook_image, w_knight_image, w_bishop_image, w_queen_image, w_king_image]

b_pawn_image = pygame.image.load("b_pawn.png")
b_rook_image = pygame.image.load("b_rook.png")
b_knight_image = pygame.image.load("b_knight.png")
b_bishop_image = pygame.image.load("b_bishop.png")
b_queen_image = pygame.image.load("b_queen.png")
b_king_image = pygame.image.load("b_king.png")
b_images = [b_pawn_image, b_rook_image, b_knight_image, b_bishop_image, b_queen_image, b_king_image]

class Pieces(ABC):
    def __init__(self, color, x_position, y_position, image):
        self.color = color
        self.x_position = x_position
        self.y_position = y_position
        self.image = image
        self.selected = False
    
    @abstractmethod
    def move(self, old_x, old_y, new_x, new_y, board, w_pieces, b_pieces):
        pass

    def isSelected(self):
        return self.selected
    
    def draw(self):
        screen.blit(self.image, (self.x_position * 60 + 20, self.y_position * 60 + 20))

class Pawn(Pieces):
    def __init__(self, color, x_position, y_position, image):
        super().__init__(color, x_position, y_position, image)
        self.__first_move = True
        self.en_pasant = False

    def move(self, old_x, old_y, new_x, new_y, board, w_pieces, b_pieces):
        if self.color == "white":
            if self.__first_move == True:
                    #first move
                    if (new_y == old_y - 1 and new_x == old_x and board[new_y][new_x] == "-") \
                    or (new_y == old_y - 2 and new_x == old_x and board[new_y + 1][new_x] == "-" and board[new_y][new_x] == "-"):
                        board[old_y][old_x] = "-"
                        board[new_y][new_x] = "w"
                        if new_y == old_y - 2:
                            self.en_pasant = True
                        self.__first_move = False
                        return True
                    #diagonal take as first move
                    elif (new_y == old_y - 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y][new_x] == "b"):
                        board[old_y][old_x] = "-"
                        board[new_y][new_x] = "w"
                        for piece in b_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y:
                                b_pieces.remove(piece)
                        self.__first_move = False
                        return True
                    else:
                        return False
            elif self.__first_move == False:
                #move
                if (new_y == old_y - 1 and new_x == old_x and board[new_y][new_x] == "-"):
                    board[old_y][old_x] = "-"
                    board[new_y][new_x] = "w"
                    return True
                #diagonal take
                elif (new_y == old_y - 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y][new_x] == "b"):
                        board[old_y][old_x] = "-"
                        board[new_y][new_x] = "w"
                        for piece in b_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y:
                                b_pieces.remove(piece)
                        return True
                #en pasant
                elif (new_y == old_y - 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y + 1][new_x] == "b"):
                        for piece in b_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y + 1:
                                if isinstance(piece, Pawn):
                                    if piece.en_pasant == True:
                                        board[old_y][new_x] = "-"
                                        board[old_y][old_x] = "-"
                                        board[new_y][new_x] = "w"
                                        b_pieces.remove(piece)
                                        return True
                else:
                    return False
                
        elif self.color == "black":
            if self.__first_move == True:
                #first move
                if (new_y == old_y + 1 and new_x == old_x and board[new_y][new_x] == "-") \
                or (new_y == old_y + 2 and new_x == old_x and board[new_y - 1][new_x] == "-" and board[new_y][new_x] == "-"):
                    board[old_y][old_x] = "-"
                    board[new_y][new_x] = "b"
                    if new_y == old_y + 2:
                            self.en_pasant = True
                    self.__first_move = False
                    return True
                #diagonal take as first move
                elif (new_y == old_y + 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y][new_x] == "w"):
                        board[old_y][old_x] = "-"
                        board[new_y][new_x] = "b"
                        for piece in w_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y:
                                w_pieces.remove(piece)
                        self.__first_move = False
                        return True
                else:
                    return False
            elif self.__first_move == False:
                #move
                if (new_y == old_y + 1 and new_x == old_x and board[new_y][new_x] == "-"):
                    board[old_y][old_x] = "-"
                    board[new_y][new_x] = "b"
                    return True
                #diagonal take
                elif (new_y == old_y + 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y][new_x] == "w"):
                        board[old_y][old_x] = "-"
                        board[new_y][new_x] = "b"
                        for piece in w_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y:
                                w_pieces.remove(piece)
                        return True
                #en pasant
                elif (new_y == old_y + 1 and (new_x == old_x + 1 or new_x == old_x - 1) and board[new_y - 1][new_x] == "w"):
                        for piece in w_pieces:
                            if piece.x_position == new_x and piece.y_position == new_y - 1:
                                if isinstance(piece, Pawn):
                                    if piece.en_pasant == True:
                                        board[old_y][new_x] = "-"
                                        board[old_y][old_x] = "-"
                                        board[new_y][new_x] = "b"
                                        w_pieces.remove(piece)
                                        return True
                else:
                    return False
    
class Rook(Pieces):
    def move(self):
        pass

class Knight(Pieces):
    def move(self):
        pass

class Bishop(Pieces):
    def move(self):
        pass

class Queen(Pieces):
    def move(self):
        pass

class King(Pieces):
    def move(self):
        pass

w_pieces  = []
w_pawn1   = Pawn  ("white", 0, 6, w_pawn_image)
w_pawn2   = Pawn  ("white", 1, 6, w_pawn_image)
w_pawn3   = Pawn  ("white", 2, 6, w_pawn_image)
w_pawn4   = Pawn  ("white", 3, 6, w_pawn_image)
w_pawn5   = Pawn  ("white", 4, 6, w_pawn_image)
w_pawn6   = Pawn  ("white", 5, 6, w_pawn_image)
w_pawn7   = Pawn  ("white", 6, 6, w_pawn_image)
w_pawn8   = Pawn  ("white", 7, 6, w_pawn_image)
w_rook1   = Rook  ("white", 0, 7, w_rook_image)
w_rook2   = Rook  ("white", 7, 7, w_rook_image)
w_knight1 = Knight("white", 1, 7, w_knight_image)
w_knight2 = Knight("white", 6, 7, w_knight_image)
w_bishop1 = Bishop("white", 2, 7, w_bishop_image)
w_bishop2 = Bishop("white", 5, 7, w_bishop_image)
w_queen   = Queen ("white", 3, 7, w_queen_image)
w_king    = King  ("white", 4, 7, w_king_image)
w_pieces = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8, w_rook1,
w_rook2, w_knight1, w_knight2, w_bishop1, w_bishop2, w_queen, w_king]

b_pieces  = []
b_pawn1   = Pawn  ("black", 0, 1, b_pawn_image)
b_pawn2   = Pawn  ("black", 1, 1, b_pawn_image)
b_pawn3   = Pawn  ("black", 2, 1, b_pawn_image)
b_pawn4   = Pawn  ("black", 3, 1, b_pawn_image)
b_pawn5   = Pawn  ("black", 4, 1, b_pawn_image)
b_pawn6   = Pawn  ("black", 5, 1, b_pawn_image)
b_pawn7   = Pawn  ("black", 6, 1, b_pawn_image)
b_pawn8   = Pawn  ("black", 7, 1, b_pawn_image)
b_rook1   = Rook  ("black", 0, 0, b_rook_image)
b_rook2   = Rook  ("black", 7, 0, b_rook_image)
b_knight1 = Knight("black", 1, 0, b_knight_image)
b_knight2 = Knight("black", 6, 0, b_knight_image)
b_bishop1 = Bishop("black", 2, 0, b_bishop_image)
b_bishop2 = Bishop("black", 5, 0, b_bishop_image)
b_queen   = Queen ("black", 3, 0, b_queen_image)
b_king    = King  ("black", 4, 0, b_king_image)
b_pieces = [b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8, b_rook1,
b_rook2, b_knight1, b_knight2, b_bishop1, b_bishop2, b_queen, b_king]

board = [["b", "b", "b", "b", "bk", "b", "b", "b"], 
         ["b", "b", "b", "b", "b", "b", "b", "b"], 
         ["-", "-", "-", "-", "-", "-", "-", "-"], 
         ["-", "-", "-", "-", "-", "-", "-", "-"], 
         ["-", "-", "-", "-", "-", "-", "-", "-"], 
         ["-", "-", "-", "-", "-", "-", "-", "-"], 
         ["w", "w", "w", "w", "w", "w", "w", "w"], 
         ["w", "w", "w", "w", "wk", "w", "w", "w"]]

def draw_game(white_turn):
    screen.blit(board_image, (0, 0)) 
    if white_turn:
        for piece in b_pieces + w_pieces:
            piece.draw()
    else:
        for piece in w_pieces + b_pieces:
                piece.draw()
    pygame.display.flip()

def reset_en_pasant(w_pieces, b_pieces, white_turn):
    if white_turn:
        for piece in b_pieces:
            if isinstance(piece, Pawn):
                piece.en_pasant = False
    elif not white_turn:
        for piece in w_pieces:
            if isinstance(piece, Pawn):
                piece.en_pasant = False

def main():
    white_turn = True
    running = True
    selected_piece = None
    original_x_pos = None
    original_y_pos = None
    while running:
        draw_game(white_turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if white_turn:
                        for piece in w_pieces:
                            if  piece.x_position * 60 <= event.pos[0] <= piece.x_position * 60 + 60 \
                            and piece.y_position * 60 <= event.pos[1] <= piece.y_position * 60 + 60:
                                selected_piece = piece
                                original_x_pos = selected_piece.x_position
                                original_y_pos = selected_piece.y_position
                                break
                    else:
                        for piece in b_pieces:
                            if  piece.x_position * 60 <= event.pos[0] <= piece.x_position * 60 + 60 \
                            and piece.y_position * 60 <= event.pos[1] <= piece.y_position * 60 + 60:
                                selected_piece = piece
                                original_x_pos = selected_piece.x_position
                                original_y_pos = selected_piece.y_position
                                break
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_piece is not None:
                    new_x = (event.pos[0] // 60)
                    new_y = (event.pos[1] // 60)
                    if selected_piece.move(original_x_pos, original_y_pos, new_x, new_y, board, w_pieces, b_pieces):
                        selected_piece.x_position = new_x
                        selected_piece.y_position = new_y
                        selected_piece.selected = False
                        selected_piece = None
                        reset_en_pasant(w_pieces, b_pieces, white_turn)
                        white_turn = not white_turn
                    else:
                        selected_piece.x_position = original_x_pos
                        selected_piece.y_position = original_y_pos
                        selected_piece.selected = False
                        selected_piece = None
                    for i in range (8):
                        print(board[i])


        if selected_piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_piece.x_position = (mouse_x - 50) / 60
            selected_piece.y_position = (mouse_y - 50) / 60
            if (mouse_x < 20 or mouse_x > 480 or mouse_y < 20 or mouse_y > 480):
                selected_piece.x_position = original_x_pos
                selected_piece.y_position = original_y_pos
                selected_piece = None
        
        clock.tick(60) 
    
    pygame.quit()

pygame.init()
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
main()