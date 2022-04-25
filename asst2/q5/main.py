import window
import sys

if len(sys.argv) != 2:
    print("Usage: python main.py [graph_path_name]")
    print("Example: python main.py 'graphs/world0.txt'")
    exit(1)

win = window.Window(1600, 900)
win.run()
