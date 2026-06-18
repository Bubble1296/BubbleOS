import customtkinter as ctk
import calendar
import platform
import re
import webbrowser
import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from tkinterweb import HtmlFrame
import certifi
import ssl
import subprocess
import sys

def check_and_install():
    required_libs = {
        "tkinterweb": "tkinterweb",
        "customtkinter": "customtkinter",
        "certifi": "certifi"
    }
    missing = []
    for lib_name, pip_name in required_libs.items():
        try:
            __import__(lib_name)
        except ImportError:
            missing.append(pip_name)

    if not missing:
        return

    print(f"BubbleOS requires the following: {', '.join(missing)}")
    answer = input("Would you like to install them now? (type 'yes' or 'no' and hit 'Enter') ").lower()
    if answer == 'yes':
        for lib in missing:
            print(f"Installing {lib}...")
            subprocess.check_call([sys.executable, "-m" , "pip", "install" , lib])
        print("Installation complete. Please restart BubbleOS.")
        sys.exit()
    else:
        print("BubbleOS cannot run without these dependencies. Shutting down...")
        sys.exit()

check_and_install()

TIME_FORMAT = "24"
clock_label = None

ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

OS_NAME = "BubbleOS"
OS_VERSION = "1.4.0"
BOOT_TIME = time.time()
jokes = [
    "Why do programmers hate nature? Because there are too many bugs.",
    "What's brown and sticky? A stick.",
    "There are 10 types of people - those who know binary and those who don't."
]

def make_draggable(window, header):
    def start_move(event):
        window.lift()
        window.drag_data = {"x": event.x, "y": event.y}
    def stop_move(event):
        window.drag_data = None
    def on_motion(event):
        if window.drag_data:
            deltax = event.x - window.drag_data["x"]
            deltay = event.y - window.drag_data["y"]
            x = window.winfo_x() + deltax
            y = window.winfo_y() + deltay
            window.place(x=x, y=y)

    header.bind("<ButtonPress-1>", start_move)
    header.bind("<ButtonRelease-1>", stop_move)
    header.bind("<B1-Motion>", on_motion)

def create_window_frame(title, w, h):
    win = tk.Frame(desktop, bg="#1e1e1e", highlightbackground="#455", highlightthickness=2)
    win.place(x=120, y=100, width=w, height=h)
    
    header = tk.Frame(win, bg="#333", height=35, cursor="fleur")
    header.pack(fill="x", side="top")
    
    tk.Label(header, text=title, fg="white", bg="#333", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Button(header, text="✕", command=win.destroy, bg="#ff5f56", fg="black", bd=0, padx=10).pack(side="right")
    
    make_draggable(win, header) 
    return win

def log_event(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def open_custom_browser():
    win = create_window_frame("BubbleOS Web Browser", 1000, 700)
    toolbar = tk.Frame(win, bg="#222", pady=5)
    toolbar.pack(fill="x")
    url_bar = tk.Entry(toolbar, bg="#333", fg="white", insertbackground="white", borderwidth=0)
    url_bar.pack(side="left", fill="x", expand=True, padx=5)
    url_bar.insert(0, "https://duckduckgo.com/html")
    browser = HtmlFrame(win, messages_enabled=False)
    browser.pack(fill="both", expand=True)
    def smart_back():
        if hasattr(browser, "go_back"): browser.go_back()
        elif hasattr(browser, "back"): browser.back()
    tk.Button(toolbar, text="←", command=smart_back, bg="#455", fg="black").pack(side="left", padx=5)
    def load_url(event=None):
        url = url_bar.get().strip()
        if "." not in url: url = f"https://duckduckgo.com/html/?q={url}"
        elif not url.startswith("http"): url = "https://" + url
        browser.load_website(url)
    url_bar.bind("<Return>", load_url)
    browser.load_website("https://duckduckgo.com/html")

def open_calendar_app():
    win = create_window_frame("Calendar", 560, 450)
    bg_color = "#1e1e1e"
    
    now = datetime.now()
    view_state = [now.month, now.year]

    nav_frame = tk.Frame(win, bg=bg_color)
    nav_frame.pack(fill="x", pady=10)

    header_label = tk.Label(nav_frame, text="", fg="cyan", bg=bg_color, font=("Arial", 12, "bold"))

    days_frame = tk.Frame(win, bg=bg_color)
    days_frame.pack(expand=True, fill="both", padx=10)

    def draw_month():
        month, year = view_state[0], view_state[1]
        
        for widget in days_frame.winfo_children():
            widget.destroy()
            
        header_label.config(text=f"{calendar.month_name[month]} {year}")
        
        days_tags = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_tags):
            tk.Label(days_frame, text=day, fg="grey", bg=bg_color).grid(row=0, column=i, sticky="nsew")

        cal = calendar.monthcalendar(year, month)
        
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    is_today = (day == now.day and month == now.month and year == now.year)
                    btn_fg = "blue" if is_today else "black"
                    
                    tk.Button(days_frame, text=str(day), fg=btn_fg, width=4, 
                              command=lambda d=day: log_event(f"CALENDAR: {month}/{d}/{year}")
                              ).grid(row=r+1, column=c, padx=2, pady=2)

    def change_month(delta):
        view_state[0] += delta
        if view_state[0] > 12:
            view_state[0] = 1
            view_state[1] += 1
        elif view_state[0] < 1:
            view_state[0] = 12
            view_state[1] -= 1
        draw_month()

    tk.Button(nav_frame, text="<", command=lambda: change_month(-1), fg="black", width=3).pack(side="left", padx=20)
    header_label.pack(side="left", expand=True)
    tk.Button(nav_frame, text=">", command=lambda: change_month(1), fg="black", width=3).pack(side="right", padx=20)

    draw_month()

def open_word_processor():
    win = create_window_frame("Word Document Processor", 700, 500)
    toolbar = tk.Frame(win, bg="#333", pady=5)
    toolbar.pack(fill="x")
    
    text_area = tk.Text(win, font=("Arial", 12), bg="white", fg="black", insertbackground="black", undo=True)
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    def import_from_computer():
        file_path = filedialog.askopenfilename(
            title="Select a Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    text_area.delete("1.0", tk.END)
                    text_area.insert("1.0", content)
                log_event(f"DOCS: Imported file from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def save_to_computer():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save to Computer")
        if file_path:
            with open(file_path, "w") as f:
                f.write(text_area.get("1.0", tk.END))
            messagebox.showinfo("BubbleOS", "File Exported!")

    tk.Button(toolbar, text="📂 Import File", command=import_from_computer, bg="#455", fg="black").pack(side="left", padx=5)
    tk.Button(toolbar, text="💾 Save File", command=save_to_computer, bg="#455", fg="black").pack(side="left", padx=5)

def open_calculator():
    win = create_window_frame("Calculator", 350, 400)
    display = tk.Entry(win, font=("Arial", 20), bg="#222", fg="white", justify="right")
    display.pack(fill="x", padx=5, pady=5)
    btn_frame = tk.Frame(win, bg="#1e1e1e")
    btn_frame.pack(expand=True, fill="both", padx=5, pady=5)
    def click(b): 
        if b == "=":
            try: res = eval(display.get()); display.delete(0, tk.END); display.insert(0, str(res))
            except: display.delete(0, tk.END); display.insert(0, "Error")
        elif b == "C": display.delete(0, tk.END)
        else: display.insert(tk.END, b)
    buttons = ['7','8','9','/','4','5','6','*','1','2','3','-','C','0','=','+']
    r, c = 0, 0
    for b in buttons:
        btn = tk.Button(btn_frame, text=b, command=lambda x=b: click(x), fg="black")
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
        btn_frame.grid_columnconfigure(c, weight=1)
        btn_frame.grid_rowconfigure(r, weight=1)
        c += 1
        if c > 3: c=0; r+=1

def open_settings_app():
    win = create_window_frame("Settings", 400, 600)
    bg_color = "#1e1e1e"
    
    tk.Label(win, text="Personalization", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=10)
    
    presets = [
        ("Midnight (Default)", "#111111"),
        ("BubbleOS Blue", "#02b0fa"),
        ("Ocean Blue", "#003366"),
        ("Naval Blue", "#05024a"),
        ("Forest Green", "#1a3300"),
        ("Maple Red", "#99001f"),
        ("Deep Purple", "#4b0082"),
        ("Bright Pink", "#f502dd"),
    ]
    
    for name, hex_code in presets:
        tk.Button(win, text=name, bg="#455", fg="black", width=20, 
                  command=lambda c=hex_code: desktop.config(bg=c)).pack(pady=2)

    tk.Label(win, text="Time Configuration", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=10)

    def set_time_format(fmt):
        global TIME_FORMAT
        TIME_FORMAT = fmt
        log_event(f"SYSTEM: Time format changed to {fmt}-hour")

    tk.Button(win, text="12-Hour (AM/PM)", width=20, fg="black", 
              command=lambda: set_time_format("12")).pack(pady=2)
    
    tk.Button(win, text="24-Hour (Military)", width=20, fg="black", 
              command=lambda: set_time_format("24")).pack(pady=2)

    tk.Frame(win, height=2, bd=1, relief="sunken", bg="#455").pack(fill="x", pady=15)

    tk.Label(win, text="System Management", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=5)
    
    def show_about():
        real_os = platform.system()
        os_release = platform.release()
        machine_type = platform.machine()
        
        try: login_name = os.getlogin()
        except: login_name = "User"
        
        about_text = (
            f"OS: {OS_NAME} {OS_VERSION}\n"
            f"Kernel: {real_os} {os_release}\n"
            f"Architecture: {machine_type}\n"
            f"User: {login_name}"
        )
        messagebox.showinfo("About BubbleOS", about_text)

    def check_updates():
        log_event("SYSTEM: Checking for updates...")
        update_win = tk.Label(win, text="Searching servers...", fg="yellow", bg=bg_color)
        update_win.pack()
        win.after(2000, lambda: update_win.config(text=f"BubbleOS {OS_VERSION} is up to date.", fg="lime"))

    tk.Button(win, text="About BubbleOS", width=20, fg="black", command=show_about).pack(pady=5)
    tk.Button(win, text="Check for Updates", width=20, fg="black", command=check_updates).pack(pady=5)

bs_variables = {"autobubble": "on"}
bs_custom_functions = {}

def open_bubblescript_app():
    win = create_window_frame("BubbleScript IDE", 600, 500)

    console = ctk.CTkTextbox(
        win,
        width=580,
        height=340,
        corner_radius=15,
        fg_color="#1a1a1a",
        text_color="#00d2ff",
    )
    console.pack(padx=10, pady=10, fill="both", expand=True)
    console.configure(state="disabled")

    def bs_log(text):
        if not win.winfo_exists(): return
        console.configure(state="normal")
        console.insert("end", f"{text}\n")
        console.configure(state="disabled")
        console.see("end")

    def gui_auto_bubble(text):
        bs_log(f"[{'='*10} Bubble {'='*10}]")
        bs_log(f"  > {text}")
        bs_log(f"[{'='*28}]")

    def gui_cmd_print(arg):
        val = bs_variables.get(arg, arg)
        if bs_variables.get("autobubble") == "on":
            gui_auto_bubble(val)
        else:
            bs_log(val)

    def gui_cmd_bubble(arg):
        gui_auto_bubble(arg.strip('"'))

    def gui_cmd_wait(arg):
        try:
            ms = int(float(arg) * 1000)
            win.after(ms, lambda: bs_log(f"[Wait for {arg}s complete]"))
        except ValueError:
            bs_log(f"Error: '{arg}' is not a numeric delay parameter value.")

    GUI_COMMANDS = {
        "print": gui_cmd_print,
        "write": gui_cmd_print,
        "bubble": gui_cmd_bubble,
        "wait": gui_cmd_wait,
    }

    def execute_line(line):
        line = line.strip()
        if not line or line.startswith("#"): return

        if "=" in line:
            name, val = line.split("=", 1)
            bs_variables[name.strip()] = val.strip().strip('"')
            bs_log(f"Var set: {name.strip()}")
            return

        parts = line.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in GUI_COMMANDS:
            GUI_COMMANDS[cmd](arg)
        else:
            bs_log(f"Unknown command: {cmd}")

    entry_frame = ctk.CTkFrame(win, fg_color="transparent")
    entry_frame.pack(fill="x", padx=10, pady=10, side="bottom")

    input_field = ctk.CTkEntry(entry_frame, placeholder_text="Type BubbleScript command...", corner_radius=10)
    input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def on_enter(event=None):
        cmd = input_field.get()
        if cmd:
            bs_log(f"BS> {cmd}")
            execute_line(cmd)
            input_field.delete(0, 'end')

    input_field.bind("<Return>", on_enter)
    
    run_btn = ctk.CTkButton(entry_frame, text="Run", width=60, corner_radius=10, command=on_enter)
    run_btn.pack(side="right")

    bs_log("BubbleScript Desktop IDE v0.1 Loaded")

def open_games_app():
    win = create_window_frame("Games", 450, 500)
    container = tk.Frame(win, bg="#1e1e1e")
    container.pack(expand=True, fill="both")

    def show_main_menu():
        for widget in container.winfo_children(): widget.destroy()
        tk.Label(container, text="Arcade Menu", font=("Arial", 18, "bold"), fg="cyan", bg="#1e1e1e").pack(pady=20)
        tk.Button(container, text="Play Hangman", width=20, command=start_hangman, fg="black").pack(pady=10)
        tk.Button(container, text="Guess the Number", width=20, command=start_number_game, fg="black").pack(pady=10)

    def start_hangman():
        for widget in container.winfo_children(): widget.destroy()
        word = random.choice(["python", "cybernetic", "code", "vex"])
        guessed = []
        attempts = 6

        tk.Button(container, text="Back", command=show_main_menu).pack(anchor="nw", padx=5, pady=5)
        disp = tk.Label(container, text="_ " * len(word), font=("Arial", 16), bg="#1e1e1e", fg="white")
        disp.pack(pady=20)
        stat = tk.Label(container, text=f"Lives: {attempts}", bg="#1e1e1e", fg="orange")
        stat.pack()
        ent = tk.Entry(container, justify="center")
        ent.pack(pady=10)

        def guess(e=None):
            nonlocal attempts
            char = ent.get().lower()
            ent.delete(0, tk.END)
            if char and char not in guessed:
                guessed.append(char)
                if char not in word: attempts -= 1
                view = "".join([c + " " if c in guessed else "_ " for c in word])
                disp.config(text=view)
                stat.config(text=f"Lives: {attempts}")
                if "_" not in view: stat.config(text="YOU WIN!", fg="lime")
                elif attempts <= 0: stat.config(text=f"GAME OVER! Word: {word}", fg="red")
        
        ent.bind("<Return>", guess)
        tk.Button(container, text="Guess", command=guess).pack()

    def start_number_game():
        for widget in container.winfo_children(): widget.destroy()
        target = random.randint(1, 100)
        tk.Button(container, text="Back", command=show_main_menu).pack(anchor="nw", padx=5, pady=5)
        tk.Label(container, text="Guess (1-100)", font=("Arial", 16), bg="#1e1e1e", fg="white").pack(pady=10)
        hint = tk.Label(container, text="Start guessing!", bg="#1e1e1e", fg="yellow")
        hint.pack()
        ent = tk.Entry(container, justify="center")
        ent.pack(pady=10)

        def check(e=None):
            try:
                val = int(ent.get())
                if val < target: hint.config(text="Higher!")
                elif val > target: hint.config(text="Lower!")
                else: hint.config(text="CORRECT!", fg="lime")
            except: hint.config(text="Enter a number!")
            ent.delete(0, tk.END)

        ent.bind("<Return>", check)
        tk.Button(container, text="Check", command=check).pack()

    show_main_menu()

def open_cli_app():
    win = create_window_frame("Legacy CLI", 600, 400)
    out = tk.Text(win, bg="black", fg="#00ff00", font=("Courier", 11), state="disabled")
    out.pack(expand=True, fill="both")
    ent = tk.Entry(win, bg="black", fg="#00ff00", insertbackground="white", borderwidth=0)
    ent.pack(fill="x")
    ent.focus_set()
    def write(t):
        out.config(state="normal"); out.insert(tk.END, t + "\n"); out.see(tk.END); out.config(state="disabled")
    def run(e):
        cmd = ent.get().lower().strip(); ent.delete(0, tk.END)
        if cmd == "help": write("Commands: help, time, joke, exit")                
        elif cmd == "time": write(time.strftime("%I:%M:%S %p"))
        elif cmd == "joke": write(random.choice(jokes))
        elif cmd == "exit": win.destroy()
        else: write(f"Unknown: {cmd}")
    ent.bind("<Return>", run)
    write("Type 'help' and press 'Enter'.")

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

def open_uptime_app():
    win = create_window_frame("System Monitor", 300, 400)
    bg_color = "#1e1e1e"
    
    tk.Label(win, text="System Stats:", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=10)
    up_lbl = tk.Label(win, text="BubbleOS Uptime: --", fg="white", bg=bg_color, font=("Courier", 11))
    up_lbl.pack(pady=5)
    cpu_lbl = tk.Label(win, text="CPU: --", fg="#00FF00", bg=bg_color, font=("Courier", 11))
    cpu_lbl.pack(pady=5)
    ram_lbl = tk.Label(win, text="RAM: --", fg="#FFFF00", bg=bg_color, font=("Courier", 11))
    ram_lbl.pack(pady=5)
    gpu_lbl = tk.Label(win, text="GPU: --", fg="#FF00FF", bg=bg_color, font=("Courier", 11))
    gpu_lbl.pack(pady=5)

    def get_stats():
        if not win.winfo_exists(): return
        
        uptime_seconds = int(time.time() - BOOT_TIME)
        hrs, rem = divmod(uptime_seconds, 3600); mins, secs = divmod(rem, 60)
        up_lbl.config(text=f"UPTIME: {hrs:02d}:{mins:02d}:{secs:02d}")

        if platform.system() == "Darwin":
            try:
                cmd = "top -l 1 | grep -E '^CPU'"
                cpu_output = subprocess.check_output(cmd, shell=True).decode()
                idle = re.findall(r"(\d+\.\d+)% idle", cpu_output)[0]
                cpu_lbl.config(text=f"CPU LOAD: {100 - float(idle):.1f}%")
            except: cpu_lbl.config(text="CPU LOAD: Error")

            try:
                vm = subprocess.check_output(['vm_stat']).decode()
                pages_free = int(re.search(r"Pages free:\s+(\d+)", vm).group(1))
                pages_active = int(re.search(r"Pages active:\s+(\d+)", vm).group(1))
                cpu_lbl.config(text=f"RAM USED: {(pages_active / (pages_free + pages_active)) * 100:.1f}%")
            except: ram_lbl.config(text="RAM: Error")
        else:
            cpu_lbl.config(text="CPU LOAD: Supported on Mac")
            ram_lbl.config(text="RAM USED: Supported on Mac")
            
        gpu_lbl.config(text="GPU: Optimized")
        win.after(2000, get_stats)

    get_stats()

def update_clock():
    global clock_label, TIME_FORMAT
    if clock_label and clock_label.winfo_exists():
        now = datetime.now()
        base_date = now.strftime("%A, %b %d, %Y")
        
        if TIME_FORMAT == "12":
            h = now.strftime("%I").lstrip("0")
            if h == "": h = "12"
            time_str = f"{h}:{now.strftime('%M:%S %p')}"
        else:
            time_str = now.strftime("%H:%M:%S")

        clock_label.configure(text=f"🕒 {base_date} | {time_str}")
        root.after(1000, update_clock)

def setup_main_ui():
    global desktop, taskbar, clock_label

    taskbar = tk.Frame(root, bg="#2b2b2b", height=50)
    taskbar.pack(side="bottom", fill="x")

    desktop = tk.Frame(root, bg="#111")
    desktop.pack(expand=True, fill="both")

    tk.Label(desktop, text="BubbleOS", font=("Arial", 40), fg="#222", bg="black").place(relx=0.5, rely=0.5, anchor="center")

    apps = [
        ("🌐", open_custom_browser), 
        ("📄", open_word_processor), 
        ("🧮", open_calculator),
        ("📟", open_cli_app), 
        ("⚙️", open_settings_app), 
        ("🕹", open_games_app),
        ("📈", open_uptime_app),
        ("🗓", open_calendar_app),
        ("🛠", open_bubblescript_app)
    ]

    def create_app_button(parent, name, command):
        outer = tk.Frame(parent, bg="#777", padx=2, pady=2)
        outer.pack(side="left", padx=8, pady=5)

        inner = tk.Frame(outer, bg="#555", padx=10, pady=5)
        inner.pack()

        lbl = tk.Label(inner, text=name, font=("Arial", 22), bg="#555", fg="white", cursor="hand2")
        lbl.pack()

        def on_click(e): command()
        def on_enter(e): inner.config(bg="#666"); lbl.config(bg="#666")
        def on_leave(e): inner.config(bg="#555"); lbl.config(bg="#555")

        for widget in [lbl, inner]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            
    for name, cmd in apps:
        create_app_button(taskbar, name, cmd)

    tk.Button(taskbar, text="⏻", command=root.destroy, bg="#ff5f56", fg="black", font=("Arial", 12, "bold"), width=3).pack(side="right", padx=10)

    clock_label = tk.Label(taskbar, text="", bg="#2b2b2b", fg="white", font=("Arial", 10, "bold"))
    clock_label.pack(side="right", padx=15)
    update_clock()

def show_loading_screen():
    load = tk.Frame(root, bg="black")
    load.place(relx=0, rely=0, relwidth=1, relheight=1)
    tk.Label(load, text="BubbleOS", font=("Arial", 50, "bold"), fg="cyan", bg="black").pack(pady=150)
    bar = ttk.Progressbar(load, length=500, mode="determinate")
    bar.pack(pady=20)
    status = tk.Label(load, text="Starting up BubbleOS...", fg="white", bg="black")
    status.pack()

    try: subprocess.Popen(['afplay', '/System/Library/Sounds/Ping.aiff'])
    except: pass

    def run_progress(v):
        if v <= 1000:
            bar["value"] = v / 10
            if v == 200: status.config(text="Booting up exposition...")
            if v == 400: status.config(text="Initiating drivers...")
            if v == 750: status.config(text="Reading code...")
            if v == 850: status.config(text="Finalizing UI...")
            if v == 985: status.config(text="Finished!")
            root.after(5, lambda: run_progress(v + 1))
        else:
            load.destroy()
            setup_main_ui()
            log_event("SYSTEM: BubbleOS v1.4.0 is online!")

    run_progress(0)

show_loading_screen()
root.mainloop()
