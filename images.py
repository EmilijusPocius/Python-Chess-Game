import pygame
import os

board_image = pygame.image.load(os.path.join("images", "chessboard.png"))

w_pawn_image = pygame.image.load(os.path.join("images", "w_pawn.png"))
w_rook_image = pygame.image.load(os.path.join("images", "w_rook.png"))
w_knight_image = pygame.image.load(os.path.join("images", "w_knight.png"))
w_bishop_image = pygame.image.load(os.path.join("images", "w_bishop.png"))
w_queen_image = pygame.image.load(os.path.join("images", "w_queen.png"))
w_king_image = pygame.image.load(os.path.join("images", "w_king.png"))
w_images = [w_pawn_image, w_rook_image, w_knight_image, w_bishop_image, w_queen_image, w_king_image]

b_pawn_image = pygame.image.load(os.path.join("images", "b_pawn.png"))
b_rook_image = pygame.image.load(os.path.join("images", "b_rook.png"))
b_knight_image = pygame.image.load(os.path.join("images", "b_knight.png"))
b_bishop_image = pygame.image.load(os.path.join("images", "b_bishop.png"))
b_queen_image = pygame.image.load(os.path.join("images", "b_queen.png"))
b_king_image = pygame.image.load(os.path.join("images", "b_king.png"))
b_images = [b_pawn_image, b_rook_image, b_knight_image, b_bishop_image, b_queen_image, b_king_image]