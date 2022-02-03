import graph
import window
import a_star
import theta_star

win = window.Window(1600, 900)
G = graph.GridGraph("graph.txt")
win.draw_graph(G)
res = a_star.a_star(win, G.src, G.dst, G.edges)
#res = theta_star.theta_star(win, G.src, G.dst, G.nodes, G.edges)
res.reverse()
win.draw_path(res)
win.run()
