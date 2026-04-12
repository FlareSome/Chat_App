import curses
from curses import wrapper
import time

def main(stdscr):
    # --- Setup ---
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)

    # Colors
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    HEADER = curses.color_pair(1) | curses.A_BOLD

    messages = [
        "[system]: welcome to the chat",
        "[system]: type /help for commands"
    ]

    current_input = ""
    scroll = 0

    # Cursor blink
    cursor_visible = True
    last_toggle = time.time()

    while True:
        # Erase stdscr cleanly instead of full clear to reduce flicker
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        chat_h = h - 3

        # Recreating windows inside the loop handles terminal resizing
        chat_win = curses.newwin(chat_h, w, 0, 0)
        input_win = curses.newwin(3, w, chat_h, 0)

        # --- Chat Window ---
        chat_win.box()
        chat_win.addstr(0, 2, " CHAT ", HEADER)

        # Safely calculate slice indices to prevent negative bounds
        end_idx = max(0, len(messages) - scroll)
        start_idx = max(0, end_idx - (chat_h - 2))
        visible_msgs = messages[start_idx:end_idx]

        for i, msg in enumerate(visible_msgs):
            if msg.startswith("[system]"):
                chat_win.addstr(i+1, 1, msg[:w-2], curses.A_DIM)
            elif msg.startswith("[you]"):
                chat_win.addstr(i+1, 1, msg[:w-2], curses.A_BOLD)
            else:
                chat_win.addstr(i+1, 1, msg[:w-2])

        # --- Input Window ---
        input_win.box()
        input_win.addstr(0, 2, " INPUT ", HEADER)

        # Cursor blinking
        if time.time() - last_toggle > 0.5:
            cursor_visible = not cursor_visible
            last_toggle = time.time()

        cursor = "_" if cursor_visible else " "
        placeholder = "type a message..."

        if current_input:
            display_text = current_input + cursor
            input_win.addstr(1, 1, "> " + display_text[:w-4])
        else:
            display_text = placeholder + cursor
            input_win.addstr(1, 1, "> " + display_text[:w-4], curses.A_DIM)

        # --- Exit hint ---
        hint = "/exit ↵ to quit"
        # Draw the hint directly onto the input_win border
        input_win.addstr(2, w - len(hint) - 2, hint, curses.A_DIM)

        # --- Efficient Refresh (doupdate) ---
        stdscr.noutrefresh()
        chat_win.noutrefresh()
        input_win.noutrefresh()
        curses.doupdate()

        # --- Input handling ---
        try:
            key = stdscr.get_wch()
        except:
            key = None

        if key in ("\n", "\r"):
            cmd = current_input.strip()

            if cmd == "/exit":
                break

            elif cmd == "/clear":
                messages.clear()
                scroll = 0  # Reset scroll on clear

            elif cmd == "/help":
                messages.append("[system]: commands → /exit /clear /help")
                scroll = 0  # Auto-scroll to bottom

            elif cmd:
                messages.append(f"[you]: {cmd}")
                scroll = 0  # Auto-scroll to bottom

            current_input = ""

        elif key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            current_input = current_input[:-1]

        # Use the correct curses constant for UP
        elif key == curses.KEY_UP:
            # Prevent scrolling past the maximum available messages
            max_scroll = max(0, len(messages) - (chat_h - 2))
            if scroll < max_scroll:
                scroll += 1

        # Use the correct curses constant for DOWN
        elif key == curses.KEY_DOWN:
            scroll = max(0, scroll - 1)

        elif isinstance(key, str):
            current_input += key

        time.sleep(0.03)

wrapper(main)