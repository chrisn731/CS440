Assignment 1: Pathfinding with A* and Theta*

How to setup your environment
========================================
To ensure proper usage on ilab please run the following commands in your terminal:
	$ export PATH="$PATH:/koko/system/anaconda/bin"
	$ source activate python38

Note: You may not need the above commands on some machines!

How to use
========================================

1. Graph Generation
	* If you do not yet have graphs generated, you can generate them.
	* Use the following commands to generate graphs for your pathfinding:
		$ python gen_graph.py
	* After running, you should have a new directory called "graphs".
	* Within this directory, there should be 50 randomly generated graphs.
		i) Implementation Note: If you go into gen_graph.py you can change the percentage of blocked cells.
		ii) The relevant variable to change is BLOCKED_PERCENT. Default is .1 for 10% blocked.
	* You are now ready to begin simulations.

2. Pathfinding
	* The proper usage is:
		$ python main.py [path_to_graph]
		-> path_to_graph represents the path to the graph file that will be used in the pathfinding simulation.
	* Once ran, a GUI will appear that will have 2 nodes highlighted
		i) The green highlighted node represents the starting point.
		ii) The red highlighted node represents the ending point.
	* From the 'Alogrithms' drop-down menu, the user can select A* or Theta*
	* Upon selecting an algorithm, a large amount of blue lines will be drawn that visualize the paths that are being explored.
	* After all the explored paths have been displayed... the lowest cost path will be displayed in red.
	* You can then click on different nodes in the graph to check their g(s), h(s), and f(s) values.
		i) These values will be displayed in the top bar of the GUI.
	* The terminal will also display additional information such as how long it took for the path to be found.


Other
========================================

* As mentioned before, you can change the percentage of blocked nodes within gen_graph.py
	** This can be done by changing the decimal value of BLOCKED_PERCENT

* You can also change the size of the generated graphs within gen_graph.py
	** range_x holds the integer value of the number of cells in the x direction
	** range_y holds the integer value of the number of cells in the y direction
	** Both values can be modified to change the dimensions of the generated graphs
