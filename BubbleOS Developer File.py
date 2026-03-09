import webbrowser
import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog
import os
from tkinterweb import HtmlFrame
import certifi
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

os.environ['SSL_CERT_FILE'] = certifi.where()

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
            root.destroy() 
        else:
            log_event("DEBUG: No install marker found to delete.")
    except Exception as e:
        log_event(f"DEBUG Error: {e}")

OS_NAME = "BubbleOS"
OS_VERSION = "1.2.0"
BOOT_TIME = time.time()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("BubbleOS")
root.geometry("1000x700") 
root.configure(bg="black")

# Auto screen adjustment
try:
    root.attributes("-fullscreen", True)
    
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


# Web Browser
def open_browser():
    browser_win = tk.Toplevel(root)
    browser_win.title("BubbleOS Web Browser")
    browser_win.geometry("1000x800")

    def open_external():
        url = url_entry.get().strip()
        print(f"DEBUG: Attempting to open {url} in external browser...")
        
        if not url:
            print("DEBUG: URL bar is empty!")
            return

        if not url.startswith("http"):
            url = "https://" + url
            
        webbrowser.open(url)

    nav_frame = tk.Frame(browser_win, bg="#2b2b2b", pady=10)
    nav_frame.pack(fill="x")

    url_entry = tk.Entry(nav_frame, bg="white", fg="black")
    url_entry.pack(side="left", fill="x", expand=True, padx=10)
    url_entry.insert(0, "https://www.youtube.com")

    tk.Button(nav_frame, 
              text="Open in Player", 
              command=open_external, 
              fg="black", 
              highlightbackground="#2b2b2b").pack(side="right", padx=5)

    browser = HtmlFrame(browser_win, messages_enabled=False)
    browser.pack(fill="both", expand=True)
    browser.load_website("https://duckduckgo.com/html")

# Updated from old CLI version to new GUI version.
# Keeps old code running but prevents crashing.
# Still shows messages in shell terminal for debugging purposes.
def print_output(text):
    log_event(text)

def update_clock():
    time_part = time.strftime("%H:%M:%S")
    date_part = time.strftime("%m/%d/%Y")
    clock_label.config(text=f"{time_part}\n{date_part}")
    root.after(1000, update_clock)

def update():
    print_output("""BubbleOS v1.2.0 Update:
- Fixed semi-broken and the old hard-to-use filesystem back from v0.1
- Added a separate document app to type into that saves either to your computer or into the BubbleOS files app
- Made the BubbleOS boot screen text back to cyan
- Other user experience enhancements
- Minor bug fixes""")

def about():
    print_output("""BubbleOS is an OS simulator developed in Python.
Created by Ian W. and Patrick S.
Special thanks to Campbell D., Spencer M., and Adham I.""")

# Files App rework WIP
def open_files_app():
    files_window = tk.Toplevel(root)
    files_window.title("File Explorer")
    files_window.geometry("500x550")
    files_window.configure(bg="#1e1e1e")

    # Storage path
    storage_path = os.path.expanduser("~/Documents/BubbleOS_Files") # <-- Saves locally to the user's computer
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    tk.Label(files_window, text="File Manager", fg="cyan", bg="#1e1e1e", font=("Arial", 12, "bold")).pack(pady=5)
    
    listbox = tk.Listbox(files_window, bg="#2b2b2b", fg="white", selectbackground="cyan", font=("Arial", 10))
    listbox.pack(padx=20, pady=5, fill="both", expand=True)

    tk.Label(files_window, text="Filename:", fg="gray", bg="#1e1e1e").pack()
    name_ent = tk.Entry(files_window, bg="#2b2b2b", fg="cyan", insertbackground="white")
    name_ent.pack(padx=20, fill="x", pady=5)
    name_ent.insert(0, "note.txt")

    cont_txt = tk.Text(files_window, height=8, bg="#2b2b2b", fg="white", insertbackground="white")
    cont_txt.pack(padx=20, fill="x", pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        for f in os.listdir(storage_path):
            if not f.startswith('.'): # Hide hidden system files
                listbox.insert(tk.END, f)

    def save_file():
        name = name_ent.get().strip()
        content = cont_txt.get("1.0", tk.END)
        
        file_path = os.path.join(storage_path, name)
        with open(file_path, "w") as f:
            f.write(content)
            
        log_event(f"SYSTEM: Saved {name} to real disk.")
        
        refresh_list()
    def delete_file():
        selection = listbox.curselection()
        if not selection: return
        
        name = listbox.get(selection[0])
        try:
            os.remove(os.path.join(storage_path, name))
            log_event(f"FILES: Deleted {name}")
            cont_txt.delete("1.0", tk.END)
            
            refresh_list() 
        except Exception as e:
            log_event(f"FILES ERROR: {e}")

    def load_file(event=None):
        selection = listbox.curselection()
        if not selection: return
        
        name = listbox.get(selection[0])
        try:
            with open(os.path.join(storage_path, name), "r") as f:
                data = f.read()
                cont_txt.delete("1.0", tk.END)
                cont_txt.insert("1.0", data)
            name_ent.delete(0, tk.END)
            name_ent.insert(0, name)
        except Exception as e:
            log_event(f"FILES ERROR: {e}")

    btn_frame = tk.Frame(files_window, bg="#1e1e1e")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Save/Update", command=save_file, width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_file, width=12, fg="red").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_list, width=10).pack(side="left", padx=5)

    # User has to double-click the file to load it, similar to a real OS.
    listbox.bind("<Double-Button-1>", load_file)
    refresh_list()

def open_word_processor():
    word_win = tk.Toplevel(root)
    word_win.title("BubbleDocs - Word Processor")
    word_win.geometry("700x600")
    word_win.configure(bg="#f0f0f0")

    toolbar = tk.Frame(word_win, bg="#d1d1d1", pady=10)
    toolbar.pack(side="top", fill="x")

    tk.Label(toolbar, text="Filename:", bg="#d1d1d1").pack(side="left", padx=5)
    doc_name_ent = tk.Entry(toolbar, width=15)
    doc_name_ent.pack(side="left", padx=5)
    doc_name_ent.insert(0, "document.txt")

    text_area = tk.Text(word_win, font=("Times New Roman", 12), undo=True, padx=20, pady=20)
    text_area.pack(expand=True, fill="both", padx=15, pady=15)

    # Saves to BubbleOS
    def save_internal():
        name = doc_name_ent.get().strip()
        content = text_area.get("1.0", tk.END).strip()
        if name:
            virtual_files[name] = content
            log_event(f"DOCS: Saved '{name}' to BubbleOS Filesystem.")
        else:
            log_event("DOCS ERROR: Filename missing!")

    # Saves to computer
    def export_to_pc():
        content = text_area.get("1.0", tk.END).strip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=doc_name_ent.get(),
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(content)
            log_event(f"DOCS: Exported to {file_path}")

    
    tk.Button(toolbar, text="💽 Save to BubbleOS", command=save_internal, bg="#4CAF50").pack(side="left", padx=5)
    tk.Button(toolbar, text="💾 Save to PC", command=export_to_pc, bg="#2196F3").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Close", command=word_window.destroy).pack(side="left", padx=5)

def open_calculator():
    calc_win = tk.Toplevel(root)
    calc_win.title("Calculator")
    calc_win.geometry("300x500")
    calc_win.configure(bg="#1e1e1e")
    
    header = tk.Frame(calc_win, bg="#2b2b2b", pady=5)
    header.pack(fill="x")
    
    tk.Label(header, text="Calculator", fg="white", bg="#2b2b2b", font=("Arial", 10, "bold")).pack(side="left")
    
    exit_btn = tk.Button(header, text="✕", command=calc_win.destroy, 
                         bg="#ff5f56", fg="black", bd=0, padx=10, relief="flat")
    exit_btn.pack(side="right", padx=5)

    display = tk.Entry(calc_win, font=("Arial", 24), bg="#2b2b2b", fg="white", 
                       borderwidth=0, justify="right")
    display.pack(fill="x", padx=10, pady=20)

    def btn_click(char):
        display.insert(tk.END, char)

    def clear():
        display.delete(0, tk.END)

    def calculate():
        try:
            result = eval(display.get())
            clear()
            display.insert(0, str(result))
        except Exception:
            clear()
            display.insert(0, "Error")

    btns_frame = tk.Frame(calc_win, bg="#1e1e1e")
    btns_frame.pack(expand=True)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        'C', '0', '=', '+'
    ]

    row, col = 0, 0
    for btn_text in buttons:
        if btn_text == "=":
            cmd = calculate
        elif btn_text == "C":
            cmd = clear
        else:
            cmd = lambda x=btn_text: btn_click(x)

        tk.Button(btns_frame, text=btn_text, width=5, height=2, 
                  bg="#f0f0f0", fg="black", highlightbackground="#1e1e1e",
                  command=cmd, relief="flat").grid(row=row, column=col, padx=3, pady=3)
        
        col += 1
        if col > 3:
            col = 0
            row += 1

# Spencer has suggested after BubbleOS Dev Test Beta v1.1.0 that the Setting's preset wallpapers should be cooler
def open_settings_app():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("400x400")
    settings_win.configure(bg="#2b2b2b")

    tk.Label(settings_win, text="Personalization", fg="white", bg="#2b2b2b", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(settings_win, text="Choose Wallpaper Color:", fg="gray", bg="#2b2b2b").pack()

    def change_wallpaper(color):
        desktop.configure(bg=color)
        log_event(f"SYSTEM: Wallpaper changed to {color}")

    color_frame = tk.Frame(settings_win, bg="#2b2b2b")
    color_frame.pack(pady=20)

    presets = [
        ("Midnight (Default)", "#111111"),
        ("Ocean", "#003366"),
        ("Deep Green", "#1a3300"),
        ("Slate", "#2f4f4f"),
        ("Purple", "#4b0082")
    ]

    for name, hex_code in presets:
        tk.Button(color_frame, text=name, bg=hex_code, fg="black", width=12,
                  command=lambda c=hex_code: change_wallpaper(c)).pack(pady=2)

    tk.Button(settings_win, text="Close", command=settings_win.destroy).pack(side="bottom", pady=10)

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
    write_to_cli("Legacy CLI Terminal Initialized. Type 'help' and press 'Enter' for commands.")

def setup_main_ui():
    global output, clock_label, desktop

    btn_params = {
        "bg": "#f0f0f0", 
        "fg": "black", 
        "relief": "flat", 
        "padx": 10, 
        "pady": 5,
        "font": ("Arial", 10)
    }
    
    taskbar = tk.Frame(root, bg="#2b2b2b", height=60)
    taskbar.pack(side="bottom", fill="x")

    desktop = tk.Frame(root, bg="#111")
    desktop.pack(expand=True, fill="both")

    tk.Label(desktop, text="BubbleOS", font=("Arial", 40), fg="#333", bg="black").place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Button(taskbar, text="🎮 Games", command=open_games_app, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="🌐 Browser", command=open_browser, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="📁 Files", command=open_files_app, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="📄 Docs", command=open_word_processor, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="🧮 Calculator", command=open_calculator, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="📟 Legacy CLI Terminal", command=open_cli_app, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="📈 Uptime Monitor", command=open_uptime_app, **btn_params).pack(side="left", padx=2, pady=5)
    tk.Button(taskbar, text="⚙️ Settings", command=open_settings_app, **btn_params).pack(side="left", padx=2, pady=5)

    clock_label = tk.Label(taskbar, bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"), justify="right")
    clock_label.pack(side="right", padx=20)
    
    tk.Button(taskbar, text="Quit", fg="black", bg="white", command=root.destroy).pack(side="right", padx=5)
    
    update_clock()

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
            
            if v == 100: status_label.config(text="Booting up BubbleOS...")
            if v == 300: status_label.config(text="Initializing drivers...")
            if v == 500: status_label.config(text="Booting up exposition...")
            if v == 700: status_label.config(text="Processing code...")
            if v == 800: status_label.config(text="Finalizing UI...")
            if v == 985: status_label.config(text="Finished!")

            root.after(6, lambda: run_progress(v + 1))
        else:
            load_frame.destroy()
            setup_main_ui()

    run_progress(0)

def open_uptime_app():
    uptime_win = tk.Toplevel(root)
    uptime_win.title("Uptime Monitor")
    uptime_win.geometry("350x250")
    uptime_win.configure(bg="#1e1e1e")

    tk.Label(uptime_win, text="Uptime Monitor", fg="#555555", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(pady=10)

    date_label = tk.Label(uptime_win, text="", fg="white", bg="#1e1e1e", font=("Arial", 12))
    date_label.pack(pady=5)
    
    time_label = tk.Label(uptime_win, text="", fg="#89CFF0", bg="#1e1e1e", font=("Arial", 20, "bold"))
    time_label.pack(pady=5)

    up_label = tk.Label(uptime_win, text="", fg="#00FF00", bg="#1e1e1e", font=("Courier", 12))
    up_label.pack(pady=20)

    def refresh_monitor():
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        seconds_alive = int(time.time() - BOOT_TIME)
        mins, secs = divmod(seconds_alive, 60)
        hrs, mins = divmod(mins, 60)
        uptime_str = f"UPTIME: {hrs:02d}:{mins:02d}:{secs:02d}"

        date_label.config(text=date_str)
        time_label.config(text=time_str)
        up_label.config(text=uptime_str)

        uptime_win.after(1000, refresh_monitor)

    refresh_monitor()

    tk.Button(uptime_win, text="CLOSE", command=uptime_win.destroy, bg="#333333", fg="black").pack(side="bottom", pady=10)

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


# FIRST-TIME BOOT NOT WORKING - WILL FIX IN LATER UPDATE
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
        log_event("BubbleOS V1.2.0 is online.")
    except:
        pass

root.after(1000, boot_sequence)

# Press 'Shift + R' to reset the system (PLEASE KNOW WHAT YOU ARE DOING!!)
root.bind("<Shift-R>", lambda e: dev_reset())

show_loading_screen()
root.mainloop()
