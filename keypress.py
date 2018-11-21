import curses, time

def main(stdscr):
    # checking for key presses
    stdscr.nodelay(True) # don't wait for input when calling getch
    return stdscr.getch()

while True:
    print("Key: ", curses.wrapper(main))
    time.sleep(1)