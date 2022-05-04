import sys
import time
from MaxConnect4Game import MaxConnect4game #import all the functions in from MaxConnect4Game.py

#Implementation of one-Move Mode of MaxConnect4 game
#CurrentGameBoard object is passed as the parameter

def oneMoveMode(currentGameBoard):
    #Time() is used to calculate the starting time of the problem
    start_time = time.time()

    #Check whether the count exceeded 42
    if currentGameBoard.piece_count >= 42:
        print("Game board is full!! \n....Game Over....")
        sys.exit(0)

    #Print the currentGameBoard before the opponents move 
    print (".....CurrentGameBoard before move.....")
    currentGameBoard.printcurrentGameBoard()
    currentGameBoard.aiPlay()

    #Print the currentGameBoard after the opponents move
    print (".....CurrentGameBoard after move.....")
    currentGameBoard.printcurrentGameBoard()
    currentGameBoard.countTotalScore()

    #Display the scores of both players
    print("Score: Player-1 = %d, Player-2 = %d\n" % (currentGameBoard.player1Score, currentGameBoard.player2Score))
    
    #Function call to append the output to output file
    currentGameBoard.printGameBoardToFile()  
    currentGameBoard.gameFile.close()
    end_time=time.time()

    #Display the time taken to get the ouptut for selected depth
    print("Time taken by the computer :",(end_time - start_time))



#Implementation of one-Move Mode of MaxConnect4 game
#CurrentGameBoard object and next player are passed as the parameters
    
def interactiveMode(currentGameBoard, nextPlayer):
    currentGameBoard.printcurrentGameBoard()
    currentGameBoard.countTotalScore()
    print("Score:: Player-1 = %d, Player-2 = %d\n" % (currentGameBoard.player1Score, currentGameBoard.player2Score))
    
    #Check if the next player is human or computer move
    if nextPlayer == "human-next":
        
        #Check if all moves have been completed 6*7=42 moves
        
        while currentGameBoard.getPieceCount() != 42:
            print("It is Human's turn.")
            humanMove = int(input("Enter the Column number between 1 - 7 where you want to play : "))
            if not 0 < humanMove < 8:
                print("Column not valid, Re-enter column number.")
                continue
            if not currentGameBoard.playPiece(humanMove - 1):
                print("Column number: %d is full. Try other column." % humanMove)
                continue
            print("Move made in Column:: " + str(humanMove))
            currentGameBoard.printcurrentGameBoard()
            currentGameBoard.gameFile = open("human.txt", 'w')
            currentGameBoard.printGameBoardToFile()
            currentGameBoard.gameFile.close()
            if currentGameBoard.getPieceCount() != 42:
                print("Computer is making a decision for next " + str(currentGameBoard.depth) + " steps...")
                currentGameBoard.change_move()
                currentGameBoard.aiPlay()
                currentGameBoard.printcurrentGameBoard()
                currentGameBoard.gameFile = open("computer.txt", 'w')
                currentGameBoard.printGameBoardToFile()
                currentGameBoard.gameFile.close()
                currentGameBoard.countTotalScore()
                print("Score: Player-1 = %d, Player-2 = %d\n" % (currentGameBoard.player1Score, currentGameBoard.player2Score))
            else:
                print("Game Over. No more moves are possible")
                currentGameBoard.countTotalScore()
                print("Score: Player-1 = %d, Player-2 = %d\n" % (currentGameBoard.player1Score, currentGameBoard.player2Score))
                break
                
    else:
        currentGameBoard.aiPlay()
        currentGameBoard.gameFile = open("computer.txt", 'w')
        currentGameBoard.printGameBoardToFile()
        currentGameBoard.gameFile.close()
        currentGameBoard.printcurrentGameBoard()
        currentGameBoard.countTotalScore()
        print('Score:: Player-1 = %d, Player-2 = %d\n' % (currentGameBoard.player1Score, currentGameBoard.player2Score))
        interactiveMode(currentGameBoard, 'human-next')

    # Display the result when the count reaches to 42
    if currentGameBoard.getPieceCount() == 42:
        print("Game Over")
        if currentGameBoard.player1Score > currentGameBoard.player2Score:
            print("Player 1 won the Game !")
        if currentGameBoard.player1Score < currentGameBoard.player2Score:
            print("Player 2 won the Game !")
        if currentGameBoard.player1Score == currentGameBoard.player2Score:
            print("The game is a Tie !")
        




#Reading the input file in the currentGameBoard

def main(a):
    currentGameBoard = MaxConnect4game()
    try:
        currentGameBoard.gameFile = open(a[2], 'r')
        input_lines = currentGameBoard.gameFile.readlines()
        currentGameBoard.currentGameBoard = [[int(char) for char in line[0:7]] for line in input_lines[0:-1]]
        currentGameBoard.presentMove = int(input_lines[-1][0])
        currentGameBoard.gameFile.close()
    except:
        print("\nError occured while opening input file. Please try with other file\n")
        currentGameBoard.presentMove = 1
    currentGameBoard.checkPieceCount()
    currentGameBoard.depth=a[4]
    
    #Call the Interactive mode or one-move mode based on the paraments passed in command line arguments
    if a[1] == "interactive":
        interactiveMode(currentGameBoard,a[3])
    else:
        try:
            currentGameBoard.gameFile = open(a[3], 'w')
        except:
            sys.exit("Error occured when opening output file!!")
        oneMoveMode(currentGameBoard)
         

#Initial start of the problem
#Call main function with command line arguments as arguments
arguments = sys.argv
main(arguments)
