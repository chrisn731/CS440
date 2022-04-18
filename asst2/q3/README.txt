Assignment 2: Probabilistic Reasoning (Question 3 Part b)

How to setup your environment
========================================
To ensure proper usage on ilab please run the following commands in your terminal:
	$ export PATH="$PATH:/koko/system/anaconda/bin"
	$ source activate python38

Note: You may not need the above commands on some machines!

How to use
========================================

1. Rejection Sampling
	* Simply run:
		$ python reject.py
	* This will generate a CSV file of the probabilities as a function of the
		number of samples used.

2. Weighted Sampling
	* Simply run:
		$ python weighted.py
	* This will generate a CSV file of the probabilities as a function of the
		number of samples used.

General Notes
========================================
* To change the desired query, simply change the variables inside of main()
	--> They follow the format of: (query, evidence)