# Chess

 VGTU EDIf-23/2 Emilijus Pocius OOP Course Work

# Coursework Report

## Introduction

### What is your application?

My application is a chess game implemented in Python using the Pygame library. It enables users to play the classic game of chess against another player on the same computer. The game handles all move logic, displays possible moves when holding a piece, manages complex moves like en passant and castling, and detects checks, checkmates, and resignation.

### How to run the program?

1) Ensure you have Python installed on your system. If not, you can download and install it from the official Python website (https://www.python.org/). 

2) Install Pygame by following the installation guide provided on the Pygame website (https://www.pygame.org/wiki/GettingStarted). 

You can install it using pip, the Python package installer, by running the following command in your terminal or command prompt:

pip install pygame

3) Download the source code for the chess game from the repository. 

4) Navigate to the directory containing the 'chess.py' file using the terminal or command prompt.

5) Run the program by executing the following command:

python chess.py

For example:

C: \ChessGame> python chess.py

### How to use the program?

Launching the Program: After running the program as described in the previous section, the chessboard and pieces will be displayed on the screen.

Making Moves: Players can make moves by holding a piece with left click and then releasing it on the destination square. The game enforces the rules of chess, so only valid moves can be made.

Resigning: Players can choose to resign from the game by clicking the ‘Resign’ button in the top left if they wish to concede defeat.

Adjusting Time Settings: To change the time settings for the players, open the 'time.txt' file located in the same directory as the program. Inside the file, you'll find two numbers separated by a newline. The first number represents white's time in seconds, and the second number represents black's time in seconds. Update these numbers as desired to adjust the time settings.

Exiting the Program: To exit the program, simply close the window displaying the game.

## Body/Analysis

The program implements all 4 object-oriented programming pillars: 

### Polymorphism:

Polymorphism is achieved through the ‘available_moves’ and ‘checking_moves’ method in each subclass of Pieces. Each subclass provides its own implementation of this method to define the specific movement behavior of the corresponding chess piece.

	class Pawn(Pieces):
	    def available_moves(self, w_pieces, b_pieces):
		# Pawn move logic
	    def checking_moves(self, w_pieces, b_pieces):
		# Pawn checking moves logic
	class Rook(Pieces):
	    def available_moves(self, w_pieces, b_pieces):
		# Rook move logic
	    def checking_moves(self, w_pieces, b_pieces):
		# Rook checking moves logic

### Abstraction:

Abstraction is demonstrated through the Pieces abstract base class, which defines abstract methods such as available_moves and checking_moves. These methods are designed to be overridden by subclasses to provide concrete implementations based on the type of chess piece.

	from abc import ABC, abstractmethod

	class Pieces(ABC):
	    def __init__(self, position, color, image):
	        # Constructor implementation
	
	    @abstractmethod
	    def available_moves(self, w_pieces, b_pieces):
	        pass
	
	    @abstractmethod
	    def checking_moves(self, w_pieces, b_pieces):
	        pass

### Inheritance:

Inheritance is utilized to create a hierarchy of chess piece classes that inherit common attributes and methods from the Pieces base class. Each subclass inherits the properties and behaviors of the parent class while also providing specialized functionality unique to the specific type of chess piece.

	class Pieces(ABC):
		# Base class specific implementation
	class Pawn(Pieces):
		# Subclass specific implementation
	class Rook(Pieces):
		# Subclass specific implementation

### Encapsulation:

Encapsulation is demonstrated through the use of private methods and attributes within the Pieces class. The _is_valid_move method, prefixed with an underscore, is intended for internal use and is not intended to be accessed directly outside the class. This helps to encapsulate the implementation details and hide the complexity from external code. 

	class Pieces(ABC):
	    def __init__(self, position, color, image):
	        # Constructor implementation
	
	    def _is_valid_move(self, w_pieces, b_pieces, new_position, original_position, enemy_piece):
	        # Encapsulated method for move validation

## Design Patterns

The program also implements two design patterns:

### Factory Method Pattern:

The Factory Method pattern is employed in the PieceFactory class to encapsulate the creation of various types of chess pieces. This pattern provides a way to delegate the instantiation logic to subclasses while ensuring that the client code remains agnostic to the concrete classes being instantiated. The PieceFactory class contains a static method create_piece that takes a piece_type parameter and returns an instance of the corresponding chess piece subclass (Pawn, Rook, Knight, Bishop, Queen, or King). This abstraction allows for the easy addition of new piece types in the future without modifying existing client code.

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

### Decorator Pattern:

The Decorator pattern is utilized in the game_information function to extend the behavior of the main function without modifying its core functionality. This pattern involves wrapping an existing function with additional functionality in a way that allows the original function to remain unchanged. The game_information function serves as a decorator that enhances the main function by calculating and logging game information such as the duration of the game, the number of moves made by each player, and the outcome of the game (winner or stalemate) to a text file (game_info.txt). By applying the Decorator pattern, the main function remains focused on orchestrating the chess game logic, while the game_information function handles the supplementary task of recording game statistics.

	def game_information(func):
	    def wrapper(*args, **kwargs):
	        start = time.time()
	        white_move_count, black_move_count, white_win, black_win, stalemate, w_pieces, b_pieces = func(*args, **kwargs)
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
	    # Main function implementation

## Reading from File & Writing to File

### Writing to File:

The program writes game information to a text file named "game_info.txt". It records various details such as the duration of the game, move counts for both players, and the outcome of the game. The information is formatted and written to the file using the write method of the file object.

	def game_information(func):
	    def wrapper(*args, **kwargs):
	        start = time.time()
	        white_move_count, black_move_count, white_win, black_win, stalemate, w_pieces, b_pieces = func(*args, **kwargs)
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

### Reading from File:

The program reads time settings from a text file named "time.txt". It retrieves the time settings for both white and black players, ensuring they are integers. If the file is not found or if there's a value error, default time settings of 600 seconds are used for both players.

	def read_time_settings():
	    try:
	        with open("time.txt", 'r') as file:
	            lines = file.readlines()
	            white_time = int(lines[0].strip())
	            black_time = int(lines[1].strip())
	            if len(str(white_time)) and len(str(black_time)) > 10:
	                white_time = 600
	                black_time = 600
	    except (ValueError, FileNotFoundError, IndexError):
	        white_time = 600
	        black_time = 600
	
	    return white_time, black_time

## Unit Testing

Since in the program there are many methods and classes, two test scripts were made that verify the behavior of specific components within the program.

### is_valid_move_test.py:

test_valid_move_no_enemy_piece: Tests the _is_valid_move method of a chess piece class when there is no enemy piece in the target position. Verifies that the move is valid.

test_valid_move_with_enemy_piece: Tests the _is_valid_move method when there is an enemy piece in the target position. Verifies that the move is valid.

test_valid_move_out_of_bounds: Tests the _is_valid_move method when the target position is out of bounds. Verifies that the move is valid.

### read_time_settings_test.py:

test_valid_file_contents: Tests the read_time_settings function when the file contains valid integer values for white and black times. Verifies that the function correctly reads and returns the time settings.

test_invalid_file_contents: Tests the function when the file contains invalid integer values. Verifies that the function returns default time values.

test_file_not_found: Tests the function when the file does not exist. Verifies that the function returns default time values.

## Results and Summary:

### Results:

The chess game operates smoothly without any apparent bugs, ensuring a seamless experience for users.

Visual appeal and user interface elements have been successfully incorporated into the game, enhancing its overall presentation and usability.

Despite facing initial challenges in implementing piece movement logic, thorough testing and debugging efforts have resulted in a robust and reliable game.

Continuous improvement opportunities exist, including refactoring certain code sections for better readability and incorporating additional features like AI opponents to enhance gameplay diversity.

The completion of this coursework has not only reinforced fundamental programming concepts but also provided valuable experience in game development and testing methodologies.

### Conclusion:

Through this coursework, I have gained a solid understanding of Object-Oriented Programming principles and the fundamentals of Python syntax. Working with the Pygame library has provided valuable insights into game development, including UI design and event handling. The resulting chess game showcases my ability to implement complex game logic and create an engaging user experience. Looking ahead, future prospects for the program include integrating AI opponents with varying difficulty levels to enable single-player gameplay, enhancing the overall experience and expanding the game's appeal.

## Resources:
https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent 
https://en.wikipedia.org/wiki/File:Chessboard480.svg 
https://www.pygame.org/docs/ 
https://chat.openai.com/ 
