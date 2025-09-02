file deleted import tkinter as tk
import random
import sys
import time

# ---------- THEME ----------
THEME = {
    "bg": "#0b1026",          # Deep navy background
    "grid_bg": "#141b3a",
    "line": "#223058",
    "x_color": "#00d1ff",     # Neon blue for X
    "o_color": "#ffd166",     # Warm gold for O
    "text": "#ffffff",
    "win_text": "#ffffff",
    "user_palette": ["#00d1ff", "#7afcff", "#52ffb8", "#ffffff"],
    "cpu_palette": ["#ffd166", "#ff9f1c", "#ff2e88", "#ffffff"],
    "draw_palette": ["#a9a9a9", "#d3d3d3", "#ffffff"],
}

# ---------- APP ----------
root = tk.Tk()
root.title("Tic Tac Toe - User vs Computer")
root.attributes("-fullscreen", True)
root.configure(bg=THEME["bg"])

# Escape to exit fullscreen quickly
def on_escape(event=None):
    root.destroy()
root.bind("<Escape>", on_escape)

# ---------- GAME STATE ----------
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
user_symbol = "X"
computer_symbol = "O"
game_locked = False  # prevent clicks during overlay

# ---------- AI / LOGIC ----------
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

def computer_move():
    if game_locked:  # ignore when overlay is up
        return
    move = find_winning_move(computer_symbol) or find_winning_move(user_symbol)
    if not move:
        # take center, then corners, else any
        empty = get_empty_cells()
        if (1,1) in empty:
            move = (1,1)
        else:
            corners = [(0,0),(0,2),(2,0),(2,2)]
            corner_choices = [c for c in corners if c in empty]
            if corner_choices:
                move = random.choice(corner_choices)
            elif empty:
                move = random.choice(empty)
            else:
                move = None

    if move:
        i, j = move
        place_symbol(i, j, computer_symbol)

        if check_winner(computer_symbol):
            show_fireworks_overlay(
                title="Computer wins!",
                subtitle="You’ve been outplayed 🤖",
                palette=THEME["cpu_palette"],
                duration_ms=4200
            )
        elif check_draw():
            show_fireworks_overlay(
                title="It's a draw!",
                subtitle="Balanced as all things should be.",
                palette=THEME["draw_palette"],
                duration_ms=3200
            )

# ---------- UI LAYOUT ----------
container = tk.Frame(root, bg=THEME["bg"])
container.pack(expand=True, fill="both")

title_lbl = tk.Label(
    container, text="Tic Tac Toe", fg=THEME["text"], bg=THEME["bg"],
    font=("Arial", 28, "bold")
)
title_lbl.pack(pady=(20, 10))

grid_frame = tk.Frame(container, bg=THEME["grid_bg"])
grid_frame.pack(expand=True)

btn_font = ("Arial", 72, "bold")

def place_symbol(i, j, symbol):
    board[i][j] = symbol
    btn = buttons[i][j]
    btn.config(
        text=symbol,
        state="disabled",
        disabledforeground=(THEME["x_color"] if symbol == "X" else THEME["o_color"])
    )

def on_click(i, j):
    if game_locked:
        return
    if board[i][j] == "":
        place_symbol(i, j, user_symbol)
        if check_winner(user_symbol):
            show_fireworks_overlay(
                title="Victory!",
                subtitle="You conquered the grid! 🏆",
                palette=THEME["user_palette"],
                duration_ms=4200
            )
        elif check_draw():
            show_fireworks_overlay(
                title="It's a draw!",
                subtitle="Try again for the glory.",
                palette=THEME["draw_palette"],
                duration_ms=3200
            )
        else:
            root.after(450, computer_move)

def reset_game():
    global board, game_locked
    game_locked = False
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

# Build 3x3 buttons
for i in range(3):
    for j in range(3):
        b = tk.Button(
            grid_frame, text="", font=btn_font, width=2, height=1,
            bg=THEME["grid_bg"], fg=THEME["text"],
            activebackground=THEME["grid_bg"], activeforeground=THEME["text"],
            highlightthickness=0,
            command=lambda r=i, c=j: on_click(r, c)
        )
        b.grid(row=i, column=j, padx=20, pady=20, ipadx=20, ipady=10, sticky="nsew")
        buttons[i][j] = b

for i in range(3):
    grid_frame.grid_columnconfigure(i, weight=1)
    grid_frame.grid_rowconfigure(i, weight=1)

controls = tk.Frame(container, bg=THEME["bg"])
controls.pack(pady=10)

reset_btn = tk.Button(controls, text="Reset", font=("Arial", 16, "bold"),
                      command=reset_game, bg="#2a355f", fg=THEME["text"],
                      activebackground="#2a355f", activeforeground=THEME["text"],
                      relief="flat", padx=16, pady=8)
reset_btn.pack(side="left", padx=8)

exit_btn = tk.Button(controls, text="Exit", font=("Arial", 16, "bold"),
                     command=root.destroy, bg="#652a2a", fg=THEME["text"],
                     activebackground="#652a2a", activeforeground=THEME["text"],
                     relief="flat", padx=16, pady=8)
exit_btn.pack(side="left", padx=8)

# ---------- FIREWORKS OVERLAY ----------
def blend_hex(c1, c2, t):
    # t in [0,1]; returns hex blended between c1->c2
    def to_rgb(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
    def to_hex(rgb): return "#%02x%02x%02x" % rgb
    a = to_rgb(c1); b = to_rgb(c2)
    mix = (int(a[0] + (b[0]-a[0])*t), int(a[1] + (b[1]-a[1])*t), int(a[2] + (b[2]-a[2])*t))
    return to_hex(mix)

class Particle:
    def __init__(self, canvas, x, y, color, bg, size=5, speed=7.0):
        self.canvas = canvas
        self.x = x
        self.y = y
        ang = random.uniform(0, 2*3.14159)
        spd = random.uniform(0.35, 1.0) * speed
        self.vx = spd * 1.0 * float(__import__('math').cos(ang))
        self.vy = spd * 1.0 * float(__import__('math').sin(ang)) * -1  # upward bias
        self.life = random.randint(36, 64)         # frames
        self.life0 = self.life
        self.size = random.uniform(2.5, size)
        self.color0 = color
        self.bg = bg
        self.item = canvas.create_oval(
            x-self.size, y-self.size, x+self.size, y+self.size,
            fill=color, outline=""
        )

    def update(self):
        # physics
        self.vy += 0.18   # gravity
        self.vx *= 0.992  # air resistance
        self.vy *= 0.992
        self.x += self.vx
        self.y += self.vy
        self.size *= 0.985
        self.life -= 1

        # fade color towards bg
        t = 1 - (self.life / self.life0)
        t = max(0.0, min(1.0, t))
        col = blend_hex(self.color0, self.bg, t)
        s = max(0.8, self.size)

        self.canvas.coords(self.item, self.x - s, self.y - s, self.x + s, self.y + s)
        self.canvas.itemconfig(self.item, fill=col)

        return self.life > 0 and self.size > 0.7

class FireworksOverlay:
    def __init__(self, root, palette, title, subtitle, duration_ms=4000):
        self.root = root
        self.palette = palette
        self.title = title
        self.subtitle = subtitle
        self.duration_ms = duration_ms
        self.start_time = None
        self.particles = []
        self.last_burst = 0

        self.top = tk.Toplevel(root, bg=THEME["bg"])
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-topmost", True)
        self.top.overrideredirect(True)
        self.top.focus_set()

        self.canvas = tk.Canvas(self.top, bg=THEME["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        w = self.top.winfo_screenwidth()
        h = self.top.winfo_screenheight()
        # Title text
        self.title_item = self.canvas.create_text(
            w/2, h*0.32, text=self.title, fill=THEME["win_text"],
            font=("Arial", int(h*0.08), "bold")
        )
        self.subtitle_item = self.canvas.create_text(
            w/2, h*0.42, text=self.subtitle, fill=blend_hex(THEME["win_text"], THEME["bg"], 0.3),
            font=("Arial", int(h*0.035), "bold")
        )

        # Start
        self.start_time = time.time()
        self.animate()
        self.schedule_bursts()

    def schedule_bursts(self):
        if self._expired():
            return
        w = self.top.winfo_screenwidth()
        h = self.top.winfo_screenheight()
        # spawn 1-3 bursts at random positions
        for _ in range(random.randint(1, 2)):
            cx = random.randint(int(w*0.18), int(w*0.82))
            cy = random.randint(int(h*0.18), int(h*0.55))
            self.spawn_burst(cx, cy)
        self.root.after(random.randint(350, 600), self.schedule_bursts)

    def spawn_burst(self, x, y):
        color = random.choice(self.palette)
        n = random.randint(50, 80)
        for _ in range(n):
            p = Particle(self.canvas, x, y, color, THEME["bg"], size=6.5, speed=8.5)
            self.particles.append(p)
        play_explosion_sound()

    def animate(self):
        if self._expired():
            self.close()
            return
        alive = []
        for p in self.particles:
            if p.update():
                alive.append(p)
            else:
                self.canvas.delete(p.item)
        self.particles = alive
        self.root.after(16, self.animate)  # ~60 FPS

    def _expired(self):
        return (time.time() - self.start_time) * 1000 >= self.duration_ms

    def close(self):
        # clear particles
        for p in self.particles:
            self.canvas.delete(p.item)
        self.particles.clear()
        try:
            self.top.destroy()
        except:
            pass
        reset_game()

# ---------- SOUND ----------
def play_explosion_sound():
    """
    Tries to play a short celebratory 'boom-sparkle' using winsound on Windows,
    otherwise falls back to bell beeps.
    """
    def _beep_pattern():
        try:
            import winsound
            # low boom
            winsound.Beep(180, 80)
            winsound.Beep(140, 80)
            # sparkle
            for f in (800, 1000, 1200, 1400):
                winsound.Beep(f, 30)
        except Exception:
            try:
                # cross-platform simple bell fallback
                for _ in range(3):
                    root.bell()
                    time.sleep(0.05)
            except:
                pass

    # Run in after() so UI doesn't freeze
    root.after(0, _beep_pattern)

# ---------- GAME FLOW HOOK ----------
def show_fireworks_overlay(title, subtitle, palette, duration_ms=4000):
    global game_locked
    game_locked = True
    FireworksOverlay(root, palette=palette, title=title, subtitle=subtitle, duration_ms=duration_ms)

# ---------- START ----------
root.mainloop()
