import time
import os

OS_NAME = "BubbleOS"
OS_VERSION = "0.1"
BOOT_TIME = time.time()

# Filesystem (fake)
files = {}

# Current user
current_user = "guest"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_help():
    print("""
Available commands:
 help            - Show this help menu
 exit            - Shut down BubbleOS
 echo <text>     - Print text
 clear           - Clear the screen
 time            - Show current time
 uptime          - Show system uptime

 list            - List files
 create <name>   - Create a file
 read <name>     - Read a file
 write <name>    - Write to a file
 delete <name>   - Delete a file

 whoami          - Show current user
 about           - About BubbleOS
""")

print(f"Booting {OS_NAME} v{OS_VERSION}...")
print("Type 'help' to see available commands.\n")

# Main OS Loop

while True:
    cmd = input(f"{current_user}@tinyos> ").strip()

    # --- Core commands ---
    if cmd == "exit":
        print("Shutting down BubbleOS...")
        break

    elif cmd == "help":
        show_help()

    elif cmd.startswith("echo "):
        print(cmd[5:])

    elif cmd == "clear":
        clear_screen()

    elif cmd == "time":
        print(time.ctime())

    elif cmd == "uptime":
        seconds = int(time.time() - BOOT_TIME)
        print(f"Uptime: {seconds} seconds")

    # File System Commands
    elif cmd == "list":
        if files:
            for name in files:
                print(name)
        else:
            print("(no files)")

    elif cmd.startswith("create "):
        name = cmd[7:].strip()
        if name in files:
            print("File already exists.")
        else:
            files[name] = ""
            print(f"Created file '{name}'")

    elif cmd.startswith("read "):
        name = cmd[5:].strip()
        if name in files:
            print(files[name])
        else:
            print("File not found.")

    elif cmd.startswith("write "):
        name = cmd[6:].strip()
        if name in files:
            content = input("Enter file content: ")
            files[name] = content
            print(f"Wrote to '{name}'")
        else:
            print("File not found.")

    elif cmd.startswith("delete "):
        name = cmd[7:].strip()
        if name in files:
            del files[name]
            print(f"Deleted '{name}'")
        else:
            print("File not found.")

# About the user:
    elif cmd == "whoami":
        print(current_user)

# About the OS:
    elif cmd == "about":
        print(f"{OS_NAME} version {OS_VERSION}")
        print("A simple OS simulator written in Python.")

    else:
        print("Unknown command. Type 'help' for a list of commands.")

            
