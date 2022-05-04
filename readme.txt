---------------------------------------------------------------------------------------------------------------------------------
Name: Lakshman Kolli
Name: Vineeth Reddy Naredla
---------------------------------------------------------------------------------------------------------------------------------
Game	: MaxConnect4
Language	: Python

-> The current code is executed in python and the version used is Python 3.10.2
-> It is compatible in Omega.
----------------------------------------------------------------------------------------------------------------------------------
Problem Description :

-> The game is built MaxConnect4 using minmax, Alpha Beta pruning and depth limited search.
-> The task is to calculate the streak of 4 and player gets one point for each streak. 
-> The game has two modes. They are:

	1. Interactive Mode
	2. One-move Mode

Syntax to run each mode:

Interactive Mode:
	$ python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]

One-move Mode:
	$ python maxconnect4.py one-move [input_file] [output_file] [depth]
------------------------------------------------------------------------------------------------------------------------------------
GAME MODES:

Interactive Mode:

-> In this mode, one player is computer and another player is human. On the move taken by the human, computer takes the counter move.
-> The final result of this mode gives which player won or loose or tie with and also prints their individual scores.

One-move Mode:

In this mode, based on the input state given, the computer will predict the next best possible move.
------------------------------------------------------------------------------------------------------------------------------------
STRUCTURE OF THE CODE :

The game has two python files.
	1. maxconnect4.py - It contains oneMoveMode and Interactive mode functions. 
	2. MaxConnect4Game.py - It contains minimax function, aiPlay function and evaluation_function


-> The algorithm is implemented in the function aiPlay()
-> It uses minimax with alpha-beta pruning.
-> The evaluation function is used to find the next possible move.
-------------------------------------------------------------------------------------------------------------------------------------
Evalution Function:

-> To get the next best possible move, we implemented an utility function to calculate the utility value.
-> We will find the consecutive fours, threes and twos for the opponent.
-> Then we calculate the number of possible fours, threes and twos that the human can make and subtract them from the opponent.
-> The column will be selected based on the calculated utility values, and then move is played. The column with highest utility value 
will be choosen.

Below is the Utility formulation:

selfScore = self_fours * 4 + self_threes * 3 + self_twos * 2
opponentScore = opponent_fours * 4 + opponent_threes * 3 + opponent_twos * 2

utilityValue = selfScore - opponentScore

--------------------------------------------------------------------------------------------------------------------------------------
DEPTH VS RUNTIME :

Runtime is calculated for each depth as shown as below and also stored in the excel sheet called Depth_Vs_Runtime.xlxs

Observation Found : It is observed that the time exceeds 1 min when the depth is beyond 8.

Note: The excel sheet is also present in the same folder.

---------------------------------------------------------------------------------------------------------------------------------------
Time Analysis in one-move mode for increasing depth levels.


    Depth   |   Time (in seconds)
   ---------|------------------------
    1       |   0.01587
    2       |   0.01606
    3       |   0.05740
    4       |   0.22850
    5       |   1.03433
    6       |   3.41592
    7       |   22.7656
    8       |   59.6229
    9       |   496.521

----------------------------------------------------------------------------------------------------------------------------------------