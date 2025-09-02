  delete file 
import tkinter as tk
from tkinter import messagebox, Toplevel, Label
import random

# Initialize full screen window
root = tk.Tk()
root.title("Tic Tac Toe - User vs Computer")
root.attributes('-fullscreen', True)  # Full screen mode

board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
user_symbol = "X"
computer_symbol = "O"

def check_winner(symbol):
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)): return True
        if all(board[j][i] == symbol for j in range(3)): return True
    if all(board[i][i] == symbol for i in range(3)): return True
    if all(board[i][2 - i] == symbol for i in range(3)): return True
    return False

def check_draw():
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def get_empty_cells():
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]

def find_winning_move(symbol):
    for i, j in get_empty_cells():
        board[i][j] = symbol
        if check_winner(symbol):
            board[i][j] = ""
            return (i, j)
        board[i][j] = ""
    return None

def show_fullscreen_message(title, message, color):
    popup = Toplevel(root)
    popup.attributes('-fullscreen', True)
    popup.configure(bg=color)

    label = Label(popup, text=message, font=("Arial", 60, "bold"), fg="white", bg=color)
    label.pack(expand=True)

    popup.after(3000, lambda: [popup.destroy(), reset_game()])  # Auto close after 3 sec

def computer_move():
    move = find_winning_move(computer_symbol) or find_winning_move(user_symbol)
    if not move:
        empty = get_empty_cells()
        move = random.choice(empty) if empty else None

    if move:
        i, j = move
        board[i][j] = computer_symbol
        buttons[i][j].config(text=computer_symbol, state=tk.DISABLED)
        if check_winner(computer_symbol):
            show_fullscreen_message("Computer Wins!", "💻 You’ve been outplayed!", "#ff4d4d")
        elif check_draw():
            show_fullscreen_message("Draw!", "😐 It's a tie!", "#808080")

def on_click(i, j):
    if board[i][j] == "":
        board[i][j] = user_symbol
        buttons[i][j].config(text=user_symbol, state=tk.DISABLED)
        if check_winner(user_symbol):
            show_fullscreen_message("Victory!", "🏆 You conquered the grid!", "#4CAF50")
        elif check_draw():
            show_fullscreen_message("Draw!", "😐 It's a tie!", "#808080")
        else:
            root.after(500, computer_move)

def reset_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=tk.NORMAL)

# Layout
frame = tk.Frame(root)
frame.pack(expand=True)

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(frame, text="", font=("Arial", 48), width=5, height=2,
                                  command=lambda r=i, c=j: on_click(r, c))
        buttons[i][j].grid(row=i, column=j, padx=20, pady=20)

# Exit button
exit_btn = tk.Button(root, text="Exit", font=("Arial", 20), command=root.destroy, bg="#333", fg="white")
exit_btn.pack(pady=20)

root.mainloop()
