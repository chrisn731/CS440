import graph
import window
import a_star
import theta_star
import sys
import time
from bfs import bfs

if len(sys.argv) != 2:
    print("Usage: python main.py [graph_path_name]")
    print("Example: python main.py 'graphs/graph21.txt'")
    exit(1)

win = window.Window(1600, 900)
G = graph.GridGraph(sys.argv[1])
win.set_graph(G)
win.run()
