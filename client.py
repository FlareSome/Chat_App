import curses
from curses import wrapper
import time
import socketio
import sys

# NETWORKING SOCKET 
sio = socketio.Client()
messages = []
scroll = 0

# USERNAME FETCH   
print("--- Terminal Chat Setup ---")
try:
    MY_NAME = input("Enter your username: ").strip()
except EOFError:
    MY_NAME = "User[X]"

if not MY_NAME:
    MY_NAME = "User[X]"

@sio.on("server_response")
def on_message(data):
    global scroll
    if isinstance(data, dict):
        user = data.get("user", "unknown")
        text = data.get("text", "")
        messages.append(f"[{user}]: {text}")
    else:
        messages.append(f"[server]: {data}")
    scroll = 0 

# CURSES UI SETUP
def main(stdscr):
    global scroll
    global MY_NAME # Global to allow /name command to work
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    HEADER = curses.color_pair(1) | curses.A_BOLD

    current_input = ""
    cursor_visible = True
    last_toggle = time.time()

    # LOCAL SERVER CONNECTION
    try:
        sio.connect("http://localhost:3000")
        messages.append(f"[system]: Welcome {MY_NAME},")
        messages.append("[system]: /help for commands")
    except:
        messages.append("[system]: error: could not connect.")

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        
        if h < 10 or w < 40:
            stdscr.addstr(0, 0, "Terminal too small!")
            stdscr.refresh()
            time.sleep(0.1)
            continue

        chat_h = h - 3
        chat_win = curses.newwin(chat_h, w, 0, 0)
        input_win = curses.newwin(3, w, chat_h, 0)

        # CHAT WINDOW
        chat_win.box()
        chat_win.addstr(0, 2, f" CHAT | {MY_NAME} ", HEADER)

        end_idx = max(0, len(messages) - scroll)
        start_idx = max(0, end_idx - (chat_h - 2))
        visible_msgs = messages[start_idx:end_idx]

        for i, msg in enumerate(visible_msgs):
            try:
                if msg.startswith("[system]"):
                    chat_win.addstr(i+1, 1, msg[:w-2], curses.A_DIM)
                elif msg.startswith(f"[{MY_NAME}]"):
                    chat_win.addstr(i+1, 1, msg[:w-2], curses.A_BOLD)
                else:
                    chat_win.addstr(i+1, 1, msg[:w-2])
            except: pass

        # INPUT WINDOW
        input_win.box()
        input_win.addstr(0, 2, " MESSAGE ", HEADER)
        
        if time.time() - last_toggle > 0.5:
            cursor_visible = not cursor_visible
            last_toggle = time.time()

        cursor = "_" if cursor_visible else " "
        display_text = (current_input if current_input else "type...") + cursor
        input_win.addstr(1, 1, "> " + display_text[:w-4], 
                         curses.A_DIM if not current_input else curses.A_NORMAL)

        # COORDINATE CRASH HANDLE
        exit_hint = "/exit to quit"
        if w > len(exit_hint) + 4:
            try:
                input_win.addstr(2, w - len(exit_hint) - 2, exit_hint, curses.A_DIM)
            except: pass

        stdscr.noutrefresh()
        chat_win.noutrefresh()
        input_win.noutrefresh()
        curses.doupdate()

        try:
            key = stdscr.get_wch()
        except:
            key = None

        if key in ("\n", "\r"):
            cmd = current_input.strip()
            
            # COMMAND HANDLING 
            if cmd == "/exit":
                break
            
            elif cmd == "/help":
                messages.append("[system]: Commands: /help, /exit, /clear, /name <newname>")
                scroll = 0
                
            elif cmd == "/clear":
                messages.clear()
                messages.append("[system]: Chat cleared.")
                messages.append("[system]: /help for commands.")
                scroll = 0
                
            elif cmd.startswith("/name "):
                new_name = cmd[6:].strip()
                if new_name:
                    old_name = MY_NAME
                    MY_NAME = new_name
                    messages.append(f"[system]: Changed name from {old_name} to {MY_NAME}")
                else:
                    messages.append("[system]: Usage: /name <newname>")
            
            elif cmd.startswith("/"):
                messages.append(f"[system]: Unknown command '{cmd.split()[0]}'. Type /help for list.")

            elif cmd:
                sio.emit("chat_message", {"user": MY_NAME, "text": cmd})
            
            current_input = ""
            
        elif key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            current_input = current_input[:-1]
        elif key == curses.KEY_UP:
            max_scroll = max(0, len(messages) - (chat_h - 2))
            if scroll < max_scroll: scroll += 1
        elif key == curses.KEY_DOWN:
            scroll = max(0, scroll - 1)
        elif isinstance(key, str):
            current_input += key

        time.sleep(0.02)

    sio.disconnect()

if __name__ == "__main__":
    wrapper(main)