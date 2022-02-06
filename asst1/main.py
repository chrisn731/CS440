import graph
import window
import a_star
import theta_star
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python main.py [graph_path_name]")
    print("Example: python main.py 'graphs/graph21.txt'")
    exit(1)

win = window.Window(1600, 900)
G = graph.GridGraph(sys.argv[1])
win.draw_graph(G)
start = time.time()
#res = a_star.a_star(win, G.src, G.dst, G.nodes, G.edges)
res = theta_star.theta_star(win, G.src, G.dst, G.nodes, G.edges)
end = time.time()
print("Found an answer in " + str(end - start) + " seconds!")
res.reverse()
win.draw_path(res)
win.run()
