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

ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

OS_NAME = "BubbleOS"
OS_VERSION = "1.3.0"
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
    win = create_window_frame("Calculator", 300, 400)
    display = tk.Entry(win, font=("Arial", 20), bg="#222", fg="white", justify="right")
    display.pack(fill="x", padx=5, pady=5)
    btn_frame = tk.Frame(win, bg="#1e1e1e")
    btn_frame.pack()
    def click(b): 
        if b == "=":
            try: res = eval(display.get()); display.delete(0, tk.END); display.insert(0, str(res))
            except: display.delete(0, tk.END); display.insert(0, "Error")
        elif b == "C": display.delete(0, tk.END)
        else: display.insert(tk.END, b)
    buttons = ['7','8','9','/','4','5','6','*','1','2','3','-','C','0','=','+']
    r, c = 0, 0
    for b in buttons:
        tk.Button(btn_frame, text=b, width=5, height=2, command=lambda x=b: click(x), fg="black").grid(row=r, column=c)
        c+=1
        if c > 3: c=0; r+=1

def open_settings_app():
    win = create_window_frame("Settings", 400, 450)
    bg_color = "#1e1e1e"
    
    tk.Label(win, text="Personalization", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=10)
    
    presets = [
        ("Midnight", "#111111"),
        ("Ocean Blue", "#003366"),
        ("Forest Green", "#1a3300"),
        ("Deep Purple", "#4b0082")
    ]
    
    for name, hex_code in presets:
        tk.Button(win, text=name, bg="#455", fg="black", width=20, 
                  command=lambda c=hex_code: desktop.config(bg=c)).pack(pady=2)

    tk.Frame(win, height=2, bd=1, relief="sunken", bg="#455").pack(fill="x", pady=15)

    tk.Label(win, text="System Management", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=5)
    
    def show_about():
        real_os = platform.system()
        os_release = platform.release()
        machine_type = platform.machine()
        
        about_text = (
            f"OS: {OS_NAME} {OS_VERSION}\n"
            f"Kernel: {real_os} {os_release}\n"
            f"Architecture: {machine_type}\n"
            f"User: {os.getlogin()}"
        )
        messagebox.showinfo("About BubbleOS", about_text)

    def check_updates():
        log_event("SYSTEM: Checking for updates...")
        update_win = tk.Label(win, text="Searching servers...", fg="yellow", bg=bg_color)
        update_win.pack()
        win.after(2000, lambda: update_win.config(text=f"BubbleOS {OS_VERSION} is up to date.", fg="lime"))

    tk.Button(win, text="About BubbleOS", width=20, fg="black", command=show_about).pack(pady=5)
    tk.Button(win, text="Check for Updates", width=20, fg="black", command=check_updates).pack(pady=5)

def open_games_app():
    win = create_window_frame("BubbleOS Games", 450, 500)
    
    container = tk.Frame(win, bg="#1e1e1e")
    container.pack(expand=True, fill="both")

    def show_main_menu():
        for widget in container.winfo_children(): widget.destroy()
        tk.Label(container, text="Arcade Menu", font=("Arial", 18, "bold"), fg="cyan", bg="#1e1e1e").pack(pady=20)
        tk.Button(container, text="Play Hangman", width=20, command=start_hangman, fg="black").pack(pady=10)
        tk.Button(container, text="Guess the Number", width=20, command=start_number_game, fg="black").pack(pady=10)

    def start_hangman():
        for widget in container.winfo_children(): widget.destroy()
        word = random.choice(["python", "cybernetic", "code", "vex", "Pneumono­ultra­micro­scopic­silico­volcano­coniosis"])
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
        elif cmd == "time": write(time.strftime("%H:%M:%S"))
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
    
    tk.Label(win, text="HARDWARE Vitals", fg="cyan", bg=bg_color, font=("Arial", 12, "bold")).pack(pady=10)
    
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

        try:
            cmd = "top -l 1 | grep -E '^CPU'"
            cpu_output = subprocess.check_output(cmd, shell=True).decode()
            idle = re.findall(r"(\d+\.\d+)% idle", cpu_output)[0]
            usage = 100 - float(idle)
            cpu_lbl.config(text=f"CPU LOAD: {usage:.1f}%")
        except: cpu_lbl.config(text="CPU LOAD: Error")

        try:
            vm = subprocess.check_output(['vm_stat']).decode()
            pages_free = int(re.search(r"Pages free:\s+(\d+)", vm).group(1))
            pages_active = int(re.search(r"Pages active:\s+(\d+)", vm).group(1))
            total = pages_free + pages_active
            usage_pct = (pages_active / total) * 100
            ram_lbl.config(text=f"RAM USED: {usage_pct:.1f}%")
        except: ram_lbl.config(text="RAM: Error")

        try:
            gpu_cmd = "ioreg -l | grep -i 'GPU' | grep -i 'utilization' | head -n 1"
            gpu_output = subprocess.check_output(gpu_cmd, shell=True).decode()
            # If no direct utilization is found, we show 'Active' status
            if "utilization" in gpu_output.lower():
                gpu_lbl.config(text="GPU LOAD: Active")
            else:
                gpu_lbl.config(text="GPU: Optimized")
        except:
            gpu_lbl.config(text="GPU: Idle")

        win.after(2000, get_stats)

    get_stats()

def setup_main_ui():
    global desktop, clock_label
    taskbar = tk.Frame(root, bg="#2b2b2b", height=50)
    taskbar.pack(side="bottom", fill="x")
    desktop = tk.Frame(root, bg="#111")
    desktop.pack(expand=True, fill="both")
    
    tk.Label(desktop, text="BubbleOS", font=("Arial", 40), fg="#222", bg="black").place(relx=0.5, rely=0.5, anchor="center")
    
    apps = [
        ("🌐 Browser", open_custom_browser), 
        ("📄 Docs", open_word_processor), 
        ("🧮 Calculator", open_calculator),
        ("📟 CLI", open_cli_app), 
        ("⚙️ Settings", open_settings_app), 
        ("🕹 Games", open_games_app),
        ("📈 Uptime", open_uptime_app)
    ]
    
    for name, cmd in apps:
        tk.Button(taskbar, text=name, command=cmd, padx=8, fg="black").pack(side="left", padx=2, pady=5)

    clock_label = tk.Label(taskbar, bg="#2b2b2b", fg="white", font=("Arial", 10, "bold"))
    clock_label.pack(side="right", padx=15)
    
    def update_clock():
        clock_label.config(text=time.strftime("%H:%M:%S\n%m/%d/%Y"))
        root.after(1000, update_clock)
    update_clock()
    
    tk.Button(taskbar, text="Quit", command=root.destroy, bg="#ff5f56", fg="black").pack(side="right", padx=5)

def show_loading_screen():
    load = tk.Frame(root, bg="black")
    load.place(relx=0, rely=0, relwidth=1, relheight=1)
    tk.Label(load, text="BubbleOS", font=("Arial", 50, "bold"), fg="cyan", bg="black").pack(pady=150)
    bar = ttk.Progressbar(load, length=500, mode="determinate")
    bar.pack(pady=20)
    status = tk.Label(load, text="Booting...", fg="white", bg="black")
    status.pack()

    try: subprocess.Popen(['afplay', '/System/Library/Sounds/Ping.aiff'])
    except: pass

    def run_progress(v):
        if v <= 1000:
            bar["value"] = v / 10
            if v == 200: status.config(text="Initializing BubbleOS...")
            if v == 340: status.config(text="Booting up exposition...")
            if v == 500: status.config(text="Reading code...")
            if v == 750: status.config(text="Finalizing UI...")
            if v == 950: status.config(text="Finished!")
            root.after(5, lambda: run_progress(v + 1))
        else:
            load.destroy()
            setup_main_ui()

            log_event("SYSTEM: BubbleOS v1.3.0 is online!")

    run_progress(0)


show_loading_screen()
root.mainloop()
