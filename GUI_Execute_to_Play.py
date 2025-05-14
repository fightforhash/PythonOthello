import tkinter as tk
from tkinter import messagebox
from constants import CELL_SIZE, BOARD_COLOR, HIGHLIGHT_COLOR, WHITE_COLOR, BLACK_COLOR,POSSIBLE_MOVE_COLOR, EMPTY, BLACK, WHITE
from backend import OthelloBoard, get_legal_moves, make_move, opponent
from AI import OthelloAI
import copy
from database import Database

class OthelloGUI:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Othello Game")
        self.hint_ai = OthelloAI('hard')
        self.game_active = True
        self.menu_frame = None
        self.board_frame = None  # Initialize board_frame
        self.db = db
        self.create_menu()

    def create_menu(self):
        # Destroy the current menu frame if it exists to ensure we start fresh.
        if self.menu_frame:
            self.menu_frame.destroy()
        
        # Create a new menu frame.
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        # Title or Logo
        title_label = tk.Label(self.menu_frame, text="OTHELLO", font=("Arial", 24))
        title_label.pack(pady=(20, 10))  # Adjust padding as needed



        # Menu Buttons
        button_frame = tk.Frame(self.menu_frame)  # Notice the parent is self.menu_frame
        button_frame.pack()

        btn_play = tk.Button(button_frame, text="Play New Game", command=self.new_game)
        btn_play_ai = tk.Button(button_frame, text="Play Against AI", command=self.select_difficulty)
        btn_stats = tk.Button(button_frame, text="User Statistics", command=self.show_user_stats)
        btn_help = tk.Button(button_frame, text="Help", command=self.show_help)
        btn_quit = tk.Button(button_frame, text="Quit", command=self.quit_game)

        # Adjust button width and height as desired
        btn_play.pack(fill=tk.X, padx=10, pady=5)
        btn_play_ai.pack(fill=tk.X, padx=10, pady=5)
        btn_stats.pack(fill=tk.X, padx=10, pady=5)
        btn_help.pack(fill=tk.X, padx=10, pady=5)
        btn_quit.pack(fill=tk.X, padx=10, pady=5)


    def create_board(self):
        if self.board_frame:  # Destroy the existing board frame if it exists
            self.board_frame.destroy()
            self.menu_frame = None  # Set it to None after destroying
        
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.board_canvas = tk.Canvas(self.board_frame, width=8*CELL_SIZE, height=8*CELL_SIZE, bg=BOARD_COLOR)
        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.board_click)
        self.status_label = tk.Label(self.board_frame, text="", font=('Arial', 16))
        self.status_label.pack(side=tk.BOTTOM)
        self.update_status_and_board()
        # Add Hint button
        self.hint_button = tk.Button(self.board_frame, text="Hint", command=self.show_hint)
        self.hint_button.pack(side=tk.TOP, anchor='ne')  # Place it at the top right corner
        # Add Surrender button on the board frame
        self.surrender_button = tk.Button(self.board_frame, text="Surrender", command=self.handle_surrender)
        self.surrender_button.pack(side=tk.TOP, anchor='ne')  # Place it at the bottom

        self.update_status_and_board()

    def handle_surrender(self):
        # Calculate the current score
        black_score = sum(row.count(BLACK) for row in self.game.board)
        white_score = sum(row.count(WHITE) for row in self.game.board)

        # Determine the winner based on the current score
        if black_score != white_score:
            winning_player = "Black" if black_score > white_score else "White"
            winning_score = abs(black_score - white_score)
            messagebox.showinfo("Game Over", f"{winning_player} wins by {winning_score} points!")
        else:
            # The game is a tie
            messagebox.showinfo("Game Over", "The game is a tie!")

        # Set the game as over and disable further interaction
        self.game_active = False

        # Optionally disable the hint and surrender buttons
        self.hint_button.config(state='disabled')
        self.surrender_button.config(state='disabled')

        # Display a surrender message
        surrendered_player = "White" if self.current_player == WHITE else "Black"
        if (self.current_player == WHITE and white_score > black_score) or \
           (self.current_player == BLACK and black_score > white_score):
            messagebox.showinfo("Surrender", f"Player {surrendered_player} has surrendered.")
        
        # After surrender, you might want to reset the board or return to the menu
        self.create_menu()


    def show_hint(self):
        # Show a hint for the current player
        legal_moves = get_legal_moves(self.game.board, self.current_player)
        if legal_moves:
            _, best_move = self.hint_ai.alpha_beta_search(copy.deepcopy(self.game.board), self.current_player, self.hint_ai.max_depth)
            if best_move:
                self.highlight_best_move(best_move)
        else:
            messagebox.showinfo("No Moves", f"No valid moves for {['Black', 'White'][self.current_player]}")

    def highlight_best_move(self, move):
        # Clear previous hints
        self.board_canvas.delete("hint")
        # Draw a hint on the board for the best move
        row, col = move
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.board_canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=HIGHLIGHT_COLOR, outline=HIGHLIGHT_COLOR, tags="hint")


    def draw_board(self):
        self.board_canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.board_canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                if self.game.board[i][j] == WHITE:
                    self.board_canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill=WHITE_COLOR, outline=WHITE_COLOR)
                elif self.game.board[i][j] == BLACK:
                    self.board_canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill=BLACK_COLOR, outline=BLACK_COLOR)
        # Highlight possible moves for human player
        if (self.current_player != self.ai):
            legal_moves = get_legal_moves(self.game.board, self.current_player)
            for move in legal_moves:
                row, col = move
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.board_canvas.create_oval(x1+10, y1+10, x2-10, y2-10, outline=POSSIBLE_MOVE_COLOR)
        
        # Highlight possible moves for human player
        if (self.current_player != self.ai):
            legal_moves = get_legal_moves(self.game.board, self.current_player)
            for move in legal_moves:
                row, col = move
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.board_canvas.create_oval(x1+10, y1+10, x2-10, y2-10, outline=POSSIBLE_MOVE_COLOR)

    def board_click(self, event):
        # Ignore clicks if the game is not active
        if not self.game_active:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.current_player == BLACK or (self.current_player == WHITE and not self.ai):
            legal_moves = get_legal_moves(self.game.board, self.current_player)
            if (row, col) in legal_moves:
                self.make_move(row, col)

    def make_move(self, row, col):
        self.game.board = make_move(self.game.board, (row, col), self.current_player)
        self.current_player = opponent(self.current_player)  # Switch sides
        self.update_status_and_board()

    def update_status_and_board(self):
        # Update the board and status
        self.draw_board()
        self.status_label.config(text=f"{['Black', 'White'][self.current_player]} to move")

        # If the current player can't move, check if the game is over or skip the turn
        if not get_legal_moves(self.game.board, self.current_player):
            if not get_legal_moves(self.game.board, opponent(self.current_player)):
                self.game_over()
                return
            messagebox.showinfo("No Moves", f"No valid moves for {'Black' if self.current_player == BLACK else 'White'}")
            self.current_player = opponent(self.current_player)  # Skip the turn
            self.draw_board()  # Redraw the board to show possible moves for the new current player

        # If the current player is AI, make a move
        if self.current_player == WHITE and self.ai:
            self.root.after(500, self.ai_move)


    def next_turn(self):
        if not get_legal_moves(self.game.board, opponent(self.current_player)):
            if not get_legal_moves(self.game.board, self.current_player):
                # Game over, no moves for either player
                self.game_over()
                return
            messagebox.showinfo("No Moves", f"No valid moves for {'Black' if opponent(self.current_player) == BLACK else 'White'}. Turn skipped.")
        
        self.current_player = opponent(self.current_player)
        self.status_label.config(text=f"{'Black' if self.current_player == BLACK else 'White'}'s turn")
        
        if self.current_player == WHITE and self.ai:
            self.root.after(500, self.ai_move)  # Wait half a second and then make the AI move

    def ai_move(self):
        # Update the status label to indicate that the AI is thinking
        self.status_label.config(text="AI is thinking...")

        # Introduce a delay to simulate thinking time and update the UI
        self.root.after(500, self.make_ai_move)  # Wait half a second before making the AI move
    
    def make_ai_move(self):
        move = self.ai.make_move(self.game.board, self.current_player)
        if move:
            self.make_move(*move)
        else:
            # If AI has no valid move, skip the turn
            self.current_player = opponent(self.current_player)
            self.update_status_and_board()

        # Update the status label to show whose turn it is after the AI move
        self.status_label.config(text=f"{['Black', 'White'][self.current_player]}'s turn")



    def setup_menu(self):
        play_button = tk.Button(self.menu_frame, text="Play New Game", command=self.new_game)
        play_ai_button = tk.Button(self.menu_frame, text="Play New Game against AI", command=self.new_game_ai)
        help_button = tk.Button(self.menu_frame, text="Show Help", command=self.show_help)
        quit_button = tk.Button(self.menu_frame, text="Quit Game", command=self.quit_game)
        play_button.pack(side=tk.LEFT)
        play_ai_button.pack(side=tk.LEFT)
        help_button.pack(side=tk.LEFT)
        quit_button.pack(side=tk.LEFT)
    
    def select_difficulty(self):
        self.menu_frame.destroy()  # Safely destroy the menu_frame if it exists
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=(100, 20))

        tk.Label(self.difficulty_frame, text="Select AI Difficulty:").pack()

        for level in ['easy', 'medium', 'hard', 'expert']:
            button = tk.Button(self.difficulty_frame, text=level.capitalize(),
                               command=lambda lvl=level: self.new_game_ai(lvl))
            button.pack(side=tk.TOP, fill=tk.X)

    def new_game(self):
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None
            self.root.update_idletasks()  # Update the GUI
        self.game = OthelloBoard()
        self.ai = None
        self.current_player = BLACK
        self.game_active = True  # Reset the game_active flag
        self.create_board()


    def new_game_ai(self, difficulty):
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None
            self.root.update_idletasks()  # Update the GUI
        if self.difficulty_frame:
            self.difficulty_frame.destroy()
            self.difficulty_frame = None
        self.game = OthelloBoard()
        self.ai = OthelloAI(difficulty)
        self.current_player = BLACK
        self.game_active = True  # Reset the game_active flag
        self.create_board()

    
    def check_game_over(self):
        if not get_legal_moves(self.game.board, self.current_player) and not get_legal_moves(self.game.board, opponent(self.current_player)):
            self.game_over()
        else:
            self.draw_board()  # This will draw possible moves

    def game_over(self):
        # Calculate the final score and display the results
        black_score = sum(row.count(BLACK) for row in self.game.board)
        white_score = sum(row.count(WHITE) for row in self.game.board)
        result_message = "The game is a tie!"
        if black_score > white_score:
            result_message = f"Black wins by {black_score - white_score} points!"
        elif white_score > black_score:
            result_message = f"White wins by {white_score - black_score} points!"
        
        # Update the status label to show the game result instead of the next turn
        self.status_label.config(text=result_message)

        messagebox.showinfo("Game Over", result_message)
        self.create_menu()  # Return to the main menu

    def show_user_stats(self):
        user_id = self.db.get_logged_in_user_id()
        if user_id is None:
            messagebox.showinfo("Error", "No logged-in user found.")
            return  

        stats = self.db.select_user_stats(user_id)
        if not stats:
            messagebox.showinfo("Error", "Unable to retrieve user statistics.")
            return  

        # Create a new window for displaying statistics
        stats_window = tk.Toplevel(self.root)
        stats_window.title("User Statistics")

        # Get the main window's position and dimensions
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()

        # Calculate the position 
        window_width = 235
        window_height = 225
        position_x = main_x + (main_width - window_width) // 2
        position_y = main_y + (main_height - window_height) // 2

        # Set the position of the stats_window
        stats_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Labels for displaying statistics
        tk.Label(stats_window, text=f"Player ID: {stats[0][0]}", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(stats_window, text=f"Total Wins: {stats[0][1]}", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(stats_window, text=f"Total Losses: {stats[0][2]}", font=("Arial", 14 ,"bold" )).pack(pady=5)
        tk.Label(stats_window, text=f"Total Games Played: {stats[0][3]}", font=("Arial", 14,"bold")).pack(pady=5)
        tk.Label(stats_window, text=f"Win Percentage: {int(stats[0][4] * 100)}%", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Close button
        tk.Button(stats_window, text="Close", command=stats_window.destroy).pack(pady=10)
        
    def show_help(self):
        messagebox.showinfo("Game Help", "In both games against AI or another player, the game begins with black's first move.")

    def quit_game(self):
        self.root.destroy()

class LoginPage:
    def __init__(self, master, on_login_success, db):
        self.master = master
        self.on_login_success = on_login_success
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady =(100,0))
        self.db = db

        tk.Label(self.frame, text="Username").pack(pady = (150, 0))
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.validate_login).pack()
    
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.validate_user(username, password):
            self.frame.destroy()  # Remove the login frame
            self.on_login_success()  # Proceed to the game
        else:
            # Show an error message if credentials are invalid
            messagebox.showinfo("Login Failed", "Invalid username or password")

def center_window(root, width=600, height=700):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window on the screen
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window with the format "widthxheight+x+y"
    root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    root.geometry("600x700")
    root.title("Othello Game")
    center_window(root)

    host = "localhost"
    user = "root"
    password = "selleryH@11"
    database = "othellogame"

    db = Database(host, user, password, database)

    def start_othello():
        othello_gui = OthelloGUI(root,db)
        othello_gui.create_menu()
        

    LoginPage(root, start_othello, db)
    root.mainloop()

    db.close

if __name__ == "__main__":
    main()