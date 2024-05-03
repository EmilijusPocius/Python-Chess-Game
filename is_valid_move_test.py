import unittest
from pieces import *

class TestIsValidMove(unittest.TestCase):

    def test_valid_move_no_enemy_piece(self):
        # Arrange
        your_class_instance = Bishop((0, 0), "w", w_images[3])
        new_position = (5, 5)  # New position to test
        original_position = (0, 0)  # Original position of the piece
        enemy_piece = None  # No enemy piece

        # Act
        result = your_class_instance._is_valid_move(w_pieces, b_pieces, new_position, original_position, enemy_piece)

        # Assert
        self.assertTrue(result)

    def test_valid_move_with_enemy_piece(self):
        # Arrange
        your_class_instance = Bishop((0, 0), "w", w_images[3])
        new_position = (5, 5)  # New position to test
        original_position = (0, 0)  # Original position of the piece
        enemy_piece = Knight((5, 5), "b", w_images[2])  # Instantiate an enemy piece

        # Act
        result = your_class_instance._is_valid_move(w_pieces, b_pieces, new_position, original_position, enemy_piece)

        # Assert
        self.assertTrue(result)

    def test_valid_move_out_of_bounds(self):
        # Arrange
        your_class_instance = Bishop((0, 0), "w", w_images[3])
        new_position = (-10, -10)  # New position to test
        original_position = (0, 0)  # Original position of the piece
        enemy_piece = None  # No enemy piece

        # Act
        result = your_class_instance._is_valid_move(w_pieces, b_pieces, new_position, original_position, enemy_piece)

        # Assert
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
