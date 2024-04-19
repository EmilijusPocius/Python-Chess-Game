import pygame
from abc import ABC, abstractmethod
from images import w_images, b_images, board_image
from pieces import Pawn, Rook, King, w_pieces, b_pieces, w_king, b_king, upgrade_pawn, king_in_check, reset_can_get_en_passant
import time

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
        screen.blit(piece.image, (piece.position[0] * 60 + 20, piece.position[1] * 60 + 20))
    if selected_piece is not None:
        screen.blit(selected_piece.image, (selected_piece.position[0] * 60 + 20, selected_piece.position[1] * 60 + 20))

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