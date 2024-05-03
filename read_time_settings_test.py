import unittest
from unittest.mock import mock_open, patch
from chess import read_time_settings

class TestReadTimeSettings(unittest.TestCase):
    # Arrange
    @patch('builtins.open', new_callable=mock_open, read_data="300\n400")
    def test_valid_file_contents(self, mock_file):
        # Act
        white_time, black_time = read_time_settings()
        # Assert
        self.assertEqual(white_time, 300)
        self.assertEqual(black_time, 400)

    # Arrange
    @patch('builtins.open', new_callable=mock_open, read_data="invalid\nvalues")
    def test_invalid_file_contents(self, mock_file):
        # Act
        white_time, black_time = read_time_settings()
        # Assert
        self.assertEqual(white_time, 600)
        self.assertEqual(black_time, 600)

    # Arrange
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        # Act
        white_time, black_time = read_time_settings()
        # Assert
        self.assertEqual(white_time, 600)
        self.assertEqual(black_time, 600)

if __name__ == '__main__':
    unittest.main()