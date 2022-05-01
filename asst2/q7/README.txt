Assignment 2: Probabilistic Reasoning (Question 7)

How to setup your environment
========================================
To ensure proper usage on ilab please run the following commands in your terminal:
	$ export PATH="$PATH:/koko/system/anaconda/bin"
	$ source activate python38

Note: You may not need the above commands on some machines!

How to use
========================================

1. Value Iteration
    * Simply call:
        $ python value_iteration.py
    * This will output all currently calculated utility values and policy at 
        each iteartion. 
    * It will also print out a one last final line to show your result utility
        and policy.

Other Notes
========================================
* If you are here from reading the assignment, we did our best commenting the
    code so that you can trace through the python code and the pseudocode (from
    question 7 of the assignment) at the same time and follow our thought process.

* If for some reason you want to change the values of the MDP, edit ONLY mdp.py file.
    This contains all the relevant data for the MDP.