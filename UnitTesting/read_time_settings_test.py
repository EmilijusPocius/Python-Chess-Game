import unittest
from unittest.mock import mock_open, patch
from chess import read_time_settings

class TestReadTimeSettings(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data="300\n400")
    def test_valid_file_contents(self, mock_file):
        # Test when the file contains valid integer values
        white_time, black_time = read_time_settings()
        self.assertEqual(white_time, 300)
        self.assertEqual(black_time, 400)

    @patch('builtins.open', new_callable=mock_open, read_data="invalid\nvalues")
    def test_invalid_file_contents(self, mock_file):
        # Test when the file contains invalid integer values
        white_time, black_time = read_time_settings()
        self.assertEqual(white_time, 600)  # Default value
        self.assertEqual(black_time, 600)  # Default value

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        # Test when the file does not exist
        white_time, black_time = read_time_settings()
        self.assertEqual(white_time, 600)  # Default value
        self.assertEqual(black_time, 600)  # Default value

if __name__ == '__main__':
    unittest.main()