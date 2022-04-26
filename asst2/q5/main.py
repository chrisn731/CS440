import window
import sys

if len(sys.argv) != 1:
    print("Usage: python main.py")
    exit(1)

win = window.Window(1600, 900)
win.run()
