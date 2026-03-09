import random
import time
import tkinter as tk
from tkinter import ttk
import os

def finish_setup(window):
    import os
    with open(".bubble_installed", "w") as f:
        f.write("installed")
    window.destroy()
    print("Setup Complete!")

def log_event(msg):
    """Standard logging function for BubbleOS"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def dev_reset():
    """Removes the install marker so the Welcome Screen shows again."""
    try:
        if os.path.exists(".bubble_installed"):
            os.remove(".bubble_installed")
            log_event("DEBUG: Install marker deleted. Restarting...")
            # This closes the app so you can relaunch it to see the welcome screen
            root.destroy() 
        else:
            log_event("DEBUG: No install marker found to delete.")
    except Exception as e:
        log_event(f"DEBUG Error: {e}")

OS_NAME = "BubbleOS"
OS_VERSION = "1.0"
BOOT_TIME = time.time()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("BubbleOS")
root.geometry("1000x700") 
root.configure(bg="black")

# Auto screen adjustment
try:
    root.attributes("-fullscreen", True)
    # Get the actual screen width/height for placement logic
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
except:
    root.attributes("-fullscreen", False)
    root.geometry("1000x700")
    screen_w = 1000
    screen_h = 700

# Basic functions code
virtual_files = {}
jokes = [
    "Why do programmers hate nature? Because there are too many bugs.",
    "What's brown and sticky? A stick.",
    "There are 10 types of people - those who know binary and those who don't."
]

def print_output(text):
    output.config(state="normal")
    output.insert(tk.END, f"> {text}\n")
    output.see(tk.END)
    output.config(state="disabled")

def update_clock():
    time_part = time.strftime("%H:%M:%S")
    date_part = time.strftime("%m/%d/%Y")
    clock_label.config(text=f"{time_part}\n{date_part}")
    root.after(1000, update_clock)

def update():
    print_output("""BubbleOS Update:
- Major GUI overhaul (CLI to mouse GUI)
- Commands have been turned into apps
- Added the 'Legacy CLI Terminal' app""")

def about():
    print_output("""BubbleOS is an OS simulator developed in Python.
Created by Ian W. and Patrick S.
Special thanks to Campbell D., Spencer M., and Adham I.""")

def open_files_app():
    files_window = tk.Toplevel(root)
    files_window.title("File Explorer")
    files_window.geometry("400x450")
    files_window.configure(bg="#1e1e1e")

    tk.Label(files_window, text="Filename:", fg="white", bg="#1e1e1e").pack(pady=5)
    name_ent = tk.Entry(files_window, bg="#2b2b2b", fg="cyan", insertbackground="white")
    name_ent.pack(padx=20, fill="x")

    tk.Label(files_window, text="Content:", fg="white", bg="#1e1e1e").pack(pady=5)
    cont_txt = tk.Text(files_window, height=8, bg="#2b2b2b", fg="white", insertbackground="white")
    cont_txt.pack(padx=20, fill="x")

    def save():
        name = name_ent.get().strip()
        body = cont_txt.get("1.0", tk.END).strip()
        if name:
            virtual_files[name] = body
            print_output(f"FILE SYSTEM: Saved '{name}'")
        
    def read():
        name = name_ent.get().strip()
        if name in virtual_files:
            cont_txt.delete("1.0", tk.END)
            cont_txt.insert("1.0", virtual_files[name])
            print_output(f"FILE SYSTEM: Opened '{name}'")

    tk.Button(files_window, text="Save", command=save, width=10).pack(pady=5)
    tk.Button(files_window, text="Read", command=read, width=10).pack(pady=5)

def open_uptime_app():
    app = tk.Toplevel(root)
    app.title("System Monitor")
    app.geometry("500x400")
    app.configure(bg="black")
    
    main_container = tk.Frame(app, bg="black")
    main_container.pack(expand=True)

    date_label = tk.Label(main_container, bg="black", fg="lime", font=("Times New Roman", 20,))
    date_label.pack(pady=5)
    
    live_time_label = tk.Label(main_container, bg="black", fg="lime", font=("Times New Roman", 20))
    live_time_label.pack(pady=5)
    
    up_label = tk.Label(main_container, bg="black", fg="lime", font=("Times New Roman", 20))
    up_label.pack(pady=20)

    def refresh_loop():
        if not app.winfo_exists():
            return
        
        current_date = time.strftime("%A, %B %d, %Y")
        
        current_time = time.strftime("%H:%M:%S")
        
        total_seconds = int(time.time() - BOOT_TIME)
        hrs, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)
        uptime_str = f"System Uptime: {hrs:02d}:{mins:02d}:{secs:02d}"
        
        date_label.config(text=current_date)
        live_time_label.config(text=current_time)
        up_label.config(text=uptime_str)
        
        app.after(1000, refresh_loop)
        
    refresh_loop()

def open_games_app():
    game_win = tk.Toplevel(root)
    game_win.title("BubbleOS Games")
    game_win.geometry("450x600")
    game_win.configure(bg="#1e1e1e")

    container = tk.Frame(game_win, bg="#1e1e1e")
    container.pack(expand=True, fill="both")

    def show_main_menu():
        for widget in container.winfo_children(): widget.destroy()
        tk.Label(container, text="Games", font=("Arial", 20, "bold"), fg="cyan", bg="#1e1e1e").pack(pady=30)
        tk.Button(container, text="Play Hangman", width=20, command=start_hangman).pack(pady=10)
        tk.Button(container, text="Guess the Number", width=20, command=start_number_game).pack(pady=10)
        tk.Button(container, text="Exit", width=20, command=game_win.destroy).pack(pady=10)

    def start_hangman():
        for widget in container.winfo_children(): widget.destroy()
        word = random.choice(["python", "cybernetic", "program", "pneumonoultramicroscopicsilicovolcanoconiosis", "Floccinaucinihilipilification"])
        guessed = []
        attempts = 8

        tk.Button(container, text="Menu", command=show_main_menu, bg="white", fg="black").pack(anchor="nw", padx=10, pady=10)
        disp = tk.Label(container, text="_ " * len(word), font=("Arial", 16), bg="#1e1e1e", fg="white", wraplength=400)
        disp.pack(pady=20)
        stat = tk.Label(container, text=f"Lives: {attempts}", bg="#1e1e1e", fg="orange", font=("Arial", 12))
        stat.pack()
        ent = tk.Entry(container, font=("Arial", 14), justify="center")
        ent.pack(pady=10)
        ent.focus_set()

        def guess_logic(event=None):
            nonlocal attempts
            char = ent.get().lower().strip()
            ent.delete(0, tk.END)
            if char and char not in guessed and len(char) == 1:
                guessed.append(char)
                if char not in word: attempts -= 1
                view = "".join([c + " " if c in guessed else "_ " for c in word])
                disp.config(text=view)
                stat.config(text=f"Lives: {attempts}")
                if "_" not in view: stat.config(text="WINNER!", fg="lime")
                elif attempts <= 0: stat.config(text=f"FAIL! Word: {word}", fg="red")
        
        tk.Button(container, text="Guess", command=guess_logic, width=10).pack(pady=5)
        ent.bind("<Return>", guess_logic)

    def start_number_game():
        for widget in container.winfo_children(): widget.destroy()
        target = random.randint(1, 100)
        tk.Button(container, text="Menu", command=show_main_menu, bg="white", fg="black").pack(anchor="nw", padx=10, pady=10)
        tk.Label(container, text="Guess (1-100)", font=("Arial", 18), bg="#1e1e1e", fg="white").pack(pady=20)
        hint = tk.Label(container, text="Good luck!", bg="#1e1e1e", fg="cyan", font=("Arial", 12))
        hint.pack()
        ent = tk.Entry(container, font=("Arial", 14), justify="center")
        ent.pack(pady=10)
        
        def check():
            try:
                val = int(ent.get())
                if val < target: hint.config(text="Higher!")
                elif val > target: hint.config(text="Lower!")
                else: hint.config(text="CORRECT!", fg="lime")
            except: hint.config(text="Enter a number!")
            ent.delete(0, tk.END)
            
        tk.Button(container, text="Check", command=check, width=10).pack(pady=5)
        ent.bind("<Return>", lambda e: check())

    show_main_menu()

def open_cli_app():
    cli_win = tk.Toplevel(root)
    cli_win.title("Legacy CLI Terminal")
    cli_win.geometry("600x450")
    cli_win.configure(bg="black")

    terminal_out = tk.Text(cli_win, bg="black", fg="#00ff00", font=("Courier", 10), state="disabled")
    terminal_out.pack(expand=True, fill="both", padx=5, pady=5)

    input_frame = tk.Frame(cli_win, bg="black")
    input_frame.pack(fill="x", side="bottom", padx=5, pady=5)
    tk.Label(input_frame, text=">", bg="black", fg="#00ff00", font=("Courier", 14, "bold")).pack(side="left")
    cmd_ent = tk.Entry(input_frame, bg="black", fg="#00ff00", font=("Courier", 12), insertbackground="white", borderwidth=0)
    cmd_ent.pack(fill="x", side="left", expand=True, padx=5)
    cmd_ent.focus_force()

    def write_to_cli(text):
        terminal_out.config(state="normal")
        terminal_out.insert(tk.END, text + "\n")
        terminal_out.see(tk.END)
        terminal_out.config(state="disabled")

    def process_command(event=None):
        cmd = cmd_ent.get().lower().strip()
        cmd_ent.delete(0, tk.END)
        if not cmd: return
        write_to_cli(f"> {cmd}")
        
        if cmd == "help":
            write_to_cli("Commands: help, about, time, version, files, uptime, games, update, joke, exit")
        elif cmd == "time":
            write_to_cli(f"Current System Time: {time.strftime('%H:%M:%S')}")
        elif cmd == "about":
            write_to_cli("=== BubbleOS Info ===")
            write_to_cli("Developers: Ian W. and Patrick S.")
            write_to_cli("Contributors: Campbell D., Spencer M., Adham I.")
            write_to_cli("BubbleOS is an operating system simulator and developed in Python.")
        elif cmd == "version": write_to_cli(f"BubbleOS Version: {OS_VERSION}")
        elif cmd == "files": open_files_app()
        elif cmd == "uptime": open_uptime_app()
        elif cmd == "games": open_games_app()
        elif cmd == "update": update()
        elif cmd == "joke": write_to_cli(random.choice(jokes))
        elif cmd == "exit": cli_win.destroy()
        else: write_to_cli(f"Error: Unknown command '{cmd}'")

    cmd_ent.bind("<Return>", process_command)
    write_to_cli("Legacy CLI Terminal Initialized. Type 'help' for commands.")

def setup_main_ui():
    global output, clock_label
    
    taskbar = tk.Frame(root, bg="#2b2b2b", height=60)
    taskbar.pack(side="bottom", fill="x")

    desktop = tk.Frame(root, bg="#111")
    desktop.pack(expand=True, fill="both")

    cli_frame = tk.Frame(desktop, bg="#000", bd=2, relief="ridge")
    cli_frame.place(relx=0.5, rely=0.35, anchor="center", width=750, height=400)
    
    title_bar = tk.Frame(cli_frame, bg="#333")
    title_bar.pack(fill="x")
    tk.Label(title_bar, text="BubbleOS System Terminal", bg="#333", fg="white", font=("Arial", 9)).pack(side="left", padx=10)

    output = tk.Text(cli_frame, bg="#000", fg="#00ff88", state="disabled", font=("Courier", 11))
    output.pack(expand=True, fill="both", padx=5, pady=5)

    btn_params = {"side": "left", "padx": 5, "pady": 10}
    tk.Button(taskbar, text="Files", command=open_files_app).pack(**btn_params)
    tk.Button(taskbar, text="Games", command=open_games_app).pack(**btn_params)
    tk.Button(taskbar, text="Legacy CLI Terminal", command=open_cli_app).pack(**btn_params)
    tk.Button(taskbar, text="Uptime Monitor", command=open_uptime_app).pack(**btn_params)
    tk.Button(taskbar, text="Update", command=update).pack(**btn_params)
    tk.Button(taskbar, text="About", command=about).pack(**btn_params)

    clock_label = tk.Label(taskbar, bg="#2b2b2b", fg="white", font=("Arial", 14, "bold"), justify="right")
    clock_label.pack(side="right", padx=20)
    
    tk.Button(taskbar, text="Quit", fg="black", bg="red", command=root.destroy).pack(side="right", padx=5)
    
    update_clock()
    print_output("Welcome to BubbleOS!")

def show_loading_screen():
    load_frame = tk.Frame(root, bg="black")
    load_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    tk.Label(load_frame, text="BubbleOS", font=("Arial", 50, "bold"), fg="cyan", bg="black").pack(pady=150)
    
    bar = ttk.Progressbar(load_frame, length=600, mode="determinate", maximum=1000)
    bar.pack(pady=20)

    status_label = tk.Label(load_frame, text="Initializing...", fg="white", bg="black", font=("Arial", 10))
    status_label.pack()

    def run_progress(v):
        if v <= 1000:
            bar["value"] = v
            
            if v == 200: status_label.config(text="Booting up BubbleOS...")
            if v == 500: status_label.config(text="Reading code...")
            if v == 800: status_label.config(text="Finalizing GUI...")
            if v == 985: status_label.config(text="Finished!")

            root.after(6, lambda: run_progress(v + 1))
        else:
            load_frame.destroy()
            setup_main_ui()

    run_progress(0)

# Developer's Reset (for testing)
def dev_reset():
    """Removes the install marker so the Welcome Screen shows again."""
    if os.path.exists(".bubble_installed"):
        os.remove(".bubble_installed")
        log_event("DEBUG: Install marker deleted. Restart to see Welcome Screen.")
        root.destroy() 
    else:
        log_event("DEBUG: No install marker found.")

root.bind("<Shift-R>", lambda e: dev_reset()) # Press 'Shift + R' as the keyboard shortcut to reset

def finish_setup(window):
    try:
        with open(".bubble_installed", "w") as f:
            f.write("installed")
        window.destroy()
        log_event("System Setup Complete. Welcome to BubbleOS!")
    except Exception as e:
        log_event(f"Setup Error: {e}")

# NOT WORKING - WILL FIX LATER
"""# First-time Welcome Boot!
def show_welcome():
    welcome = tk.Toplevel(root)
    welcome.title("BubbleOS Setup")
    welcome.geometry("400x350")
    welcome.configure(bg="#1a1a1a")
    welcome.attributes("-topmost", True)

    x = (root.winfo_screenwidth() // 2) - 200
    y = (root.winfo_screenheight() // 2) - 175
    welcome.geometry(f"400x350+{x}+{y}")

    tk.Label(welcome, text="Initializing BubbleOS", fg="white", 
             bg="#1a1a1a", font=("Arial", 14)).pack(pady=20)

    progress = ttk.Progressbar(welcome, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    status_label = tk.Label(welcome, text="Loading system drivers...", 
                            fg="#00ff00", bg="#1a1a1a", font=("Courier", 9))
    status_label.pack()

    def run_loading():
        for i in range(1, 101):
            if not welcome.winfo_exists(): return 
            
            progress['value'] = i
            
            if i < 25: status_label.config(text="Loading BubbleOS...")
            elif i < 50: status_label.config(text="Optimizing UI...")
            elif i < 75: status_label.config(text=" 'Installing Drivers'...")
            elif i < 100: status_label.config(text="Finalizing...")
            
            welcome.update()
            time.sleep(0.03)

        play_startup_sound()
        status_label.config(text="System Ready!")
        btn.pack(pady=20)
    def finish_setup(window):
        with open(".bubble_installed", "w") as f:
            f.write("installed")
        window.destroy()
        log_event("Setup Complete!")

    btn = ttk.Button(welcome, text="Begin Adventure", command=lambda: finish_setup(welcome))
    
    welcome.after(500, run_loading)"""

def play_startup_sound():
    import subprocess
    try:
        subprocess.Popen(['afplay', '/System/Library/Sounds/Ping.aiff'])
    except:
        pass

def boot_sequence():
    """Simple, no-fail boot sequence."""
    try:
        play_startup_sound()
        log_event("BubbleOS V1.0.0 is online.")
    except:
        pass

root.after(1000, boot_sequence)

# Press 'Shift + R' to reset the system (PLEASE KNOW WHAT YOU ARE DOING!!)
root.bind("<Shift-R>", lambda e: dev_reset())

show_loading_screen()
root.mainloop()
