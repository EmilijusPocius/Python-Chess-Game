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
    def __init__(self, x_position, y_position, image):
        self.x_position = x_position
        self.y_position = y_position
        self.image = image
    
    @abstractmethod
    def move(self, old_x, old_y, new_x, new_y, board, all_pieces):
        pass
    
    def draw(self):
        screen.blit(self.image, (self.x_position * 60 + 20, self.y_position * 60 + 20))
    
class WhitePiece(Pieces):
    def move(self, old_x, old_y, new_x, new_y, board, w_pieces, b_pieces):
        #move
        if (board[new_y][new_x] == "-"):
            board[old_y][old_x] = "-"
            board[new_y][new_x] = "w"
            self.x_position = new_x
            self.y_position = new_y
            
        #take
        elif (board[new_y][new_x] == "b"):
                board[old_y][old_x] = "-"
                board[new_y][new_x] = "w"
                self.x_position = new_x
                self.y_position = new_y
                for piece in b_pieces:
                    if piece.x_position == new_x and piece.y_position == new_y:
                        b_pieces.remove(piece)
        #return
        else:
            self.x_position = old_x
            self.y_position = old_y
        

class BlackPiece(Pieces):
    def move(self, old_x, old_y, new_x, new_y, board, w_pieces, b_pieces):
        #move
        if (board[new_y][new_x] == "-"):
            board[old_y][old_x] = "-"
            board[new_y][new_x] = "b"
            self.x_position = new_x
            self.y_position = new_y
            
        #take
        elif (board[new_y][new_x] == "w"):
                board[old_y][old_x] = "-"
                board[new_y][new_x] = "b"
                self.x_position = new_x
                self.y_position = new_y
                for piece in w_pieces:
                    if piece.x_position == new_x and piece.y_position == new_y:
                        w_pieces.remove(piece)
        #return
        else:
            self.x_position = old_x
            self.y_position = old_y

w_pawn1   = WhitePiece(0, 6, w_pawn_image)
w_pawn2   = WhitePiece(1, 6, w_pawn_image)
w_pawn3   = WhitePiece(2, 6, w_pawn_image)
w_pawn4   = WhitePiece(3, 6, w_pawn_image)
w_pawn5   = WhitePiece(4, 6, w_pawn_image)
w_pawn6   = WhitePiece(5, 6, w_pawn_image)
w_pawn7   = WhitePiece(6, 6, w_pawn_image)
w_pawn8   = WhitePiece(7, 6, w_pawn_image)
w_rook1   = WhitePiece(0, 7, w_rook_image)
w_rook2   = WhitePiece(7, 7, w_rook_image)
w_knight1 = WhitePiece(1, 7, w_knight_image)
w_knight2 = WhitePiece(6, 7, w_knight_image)
w_bishop1 = WhitePiece(2, 7, w_bishop_image)
w_bishop2 = WhitePiece(5, 7, w_bishop_image)
w_queen   = WhitePiece(3, 7, w_queen_image)
w_king    = WhitePiece(4, 7, w_king_image)
w_pieces = [w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7, w_pawn8, w_rook1,
w_rook2, w_knight1, w_knight2, w_bishop1, w_bishop2, w_queen, w_king]

b_pawn1   = BlackPiece(0, 1, b_pawn_image)
b_pawn2   = BlackPiece(1, 1, b_pawn_image)
b_pawn3   = BlackPiece(2, 1, b_pawn_image)
b_pawn4   = BlackPiece(3, 1, b_pawn_image)
b_pawn5   = BlackPiece(4, 1, b_pawn_image)
b_pawn6   = BlackPiece(5, 1, b_pawn_image)
b_pawn7   = BlackPiece(6, 1, b_pawn_image)
b_pawn8   = BlackPiece(7, 1, b_pawn_image)
b_rook1   = BlackPiece(0, 0, b_rook_image)
b_rook2   = BlackPiece(7, 0, b_rook_image)
b_knight1 = BlackPiece(1, 0, b_knight_image)
b_knight2 = BlackPiece(6, 0, b_knight_image)
b_bishop1 = BlackPiece(2, 0, b_bishop_image)
b_bishop2 = BlackPiece(5, 0, b_bishop_image)
b_queen   = BlackPiece(3, 0, b_queen_image)
b_king    = BlackPiece(4, 0, b_king_image)
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

def draw_game(selected_piece):
    screen.blit(board_image, (0, 0)) 
    for piece in w_pieces + b_pieces:
        piece.draw()
    if selected_piece is not None:
        selected_piece.draw()
    pygame.display.flip()

def main():
    running = True
    selected_piece = None
    original_x = None
    original_y = None
    while running:
        draw_game(selected_piece)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for piece in w_pieces + b_pieces:
                        if  piece.x_position * 60 + 20 <= event.pos[0] <= piece.x_position * 60 + 60 + 20 \
                        and piece.y_position * 60 + 20 <= event.pos[1] <= piece.y_position * 60 + 60 + 20:
                            selected_piece = piece
                            original_x = selected_piece.x_position
                            original_y = selected_piece.y_position
                            break
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_piece is not None:
                    new_x = ((event.pos[0] - 20) // 60)
                    new_y = ((event.pos[1] - 20) // 60)
                    selected_piece.move(original_x, original_y, new_x, new_y, board, w_pieces, b_pieces)
                    selected_piece = None
                    for i in range (8):
                        print(board[i])


        if selected_piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_piece.x_position = (mouse_x - 50) / 60
            selected_piece.y_position = (mouse_y - 50) / 60
            if (mouse_x < 20 or mouse_x > 480 or mouse_y < 20 or mouse_y > 480):
                selected_piece.x_position = original_x
                selected_piece.y_position = original_y
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