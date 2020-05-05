#Jessica Qinying Wu
#This is the Sudoku project
#Start: April 29, 2020

import random
import warnings
import math
import time
import numpy as np
from colorama import Fore

INDICES={1,2,3,4,5,6,7,8,9}
HINTS=3
INSTRUCTIONS='\nInput Command Instruction\n\n P:Place a number in a cell\n R: Remove a number from a cell\n H: Request 1 more number clue (hints left: %d)\n C: Clear the board (restart the current game)\n L: Look at the solution (will end game automatically)\n S: Start a new game\n Q: Quit the current game\n\n Prompts will appear after input for command' %HINTS
VALID_PROMPT='Please enter a valid option (e.g. 3)'
QUIT_PROMPT='You have chosen to quit the game. Have a nice day! :)'
WIN_PROMPT='Congratulations! You have successfully solved the board!'
#Function to fill the diagonal units of the Sudoku board
#returns the filled board
# # # #  0 0 0  0 0 0
# # # #  0 0 0  0 0 0
# # # #  0 0 0  0 0 0

# 0 0 0  # # #  0 0 0
# 0 0 0  # # #  0 0 0
# 0 0 0  # # #  0 0 0

# 0 0 0  0 0 0  # # #
# 0 0 0  0 0 0  # # #
# 0 0 0  0 0 0  # # #
def FillDiagonalUnits():
    board=[[],[],[],[],[],[],[],[],[]]
    sequence=[1,2,3,4,5,6,7,8,9]
    for i in range(9):
        if i%3==0:
            random.shuffle(sequence)
        for j in range(9):
            board[i].append(sequence[j%3+(i%3)*3] if (math.floor(i/3)==math.floor(j/3)) else 0)

    return np.array(board)


#function that fills in the adjacency unit squares using the backtracking algorithm
#parameter board is the Sudoku board, rowIndex and colIndex are the eow and column indices, respectively
#returns a valid filled Sudoku board
def FillAdjacencyUnits(board,rowIndex,colIndex):
    if colIndex>=9 and rowIndex<8: #if reached the end of a row, start at a new row with colIndex=0
        rowIndex+=1
        colIndex=0
    if rowIndex<3:
        if colIndex<3:
            colIndex+=3
    elif rowIndex<6:
        if colIndex>=3 and colIndex<6:
            colIndex+=3
    else:
        if colIndex>=6:#go to new row if column index equals or exceeds 6 in the last three rows
            rowIndex+=1
            colIndex=0
            if rowIndex>=9:
                return board
    for num in range(1,10):
        if not (FoundInRow(board,num,rowIndex) or  FoundInCol(board,num,colIndex) or FoundInUnit(board,num,rowIndex,colIndex)):
            board[rowIndex,colIndex]=num
            tempBoard=FillAdjacencyUnits(board,rowIndex,colIndex+1)
            if len(np.setdiff1d(tempBoard,board))!=0 or 0 not in tempBoard:
                return tempBoard
            else:
                board[rowIndex,colIndex]=0
    return board

#determine whether a number already exists within the row of the position or not
#parameter board is the Sudoku board, num is the given number, rowIndex is the row index
#returns truw if found, else false
def FoundInRow(board,num,rowIndex):
    return num in board[rowIndex,:]

#determine whether a number already exists within the column of the position or not
#parameter board is the Sudoku board, num is the given number, colIndex is the column index
#returns truw if found, else false
def FoundInCol(board,num,colIndex):
    return num in board[:,colIndex]

#determine whether a number already exists within the unit square of the position or not
#parameter board is the Sudoku board, num is the given number, rowIndex and colIndex are the row and column indices, respectively
#returns truw if found, else false
def FoundInUnit(board,num,rowIndex,colIndex):
    return num in board[math.floor(rowIndex/3)*3:math.floor(rowIndex/3)*3+3,math.floor(colIndex/3)*3:math.floor(colIndex/3)*3+3]

#function that removes number from the filled board
#parameter board is the current Sudoku board with partially removed numbers (initially full)
#parameter rowIndex and colIndex are the row and column indices, respectively
#parameter removeCount is the count of numbers to remove from the board
#returns the Sudoku board with removed numbers
def RemoveNumbers(board,rowIndex,colIndex):
    if board[rowIndex,colIndex]!=0:
        board[rowIndex,colIndex]=0
    return board



#Function that determines whether the current partially filled board has a unique solution or not
#parameter board is the current Sudoku board with removed numbers
#solution is the intended unique solution of the Sudoku board
#returns the count of solutions of the board
def UniqueSolution(board,solution):
    isUnique=True #initially assume unique solution
    if 0 in board:
        blanks=np.where(board==0)
        rowIndex=blanks[0][0]
        colIndex=blanks[1][0] #obtain the first blank from the list returned
        tempBoard=board.copy()
        for num in range(9):
            if not (FoundInRow(board,num,rowIndex) or  FoundInCol(board,num,colIndex) or FoundInUnit(board,num,rowIndex,colIndex)):
                tempBoard[rowIndex,colIndex]=num
                if UniqueSolution(tempBoard,solution)==False:
                    return False
                
    else: #the board is entirely filled with numbers but does not equal to the expected solution, then there is no unique solution
        if np.array_equal(board,solution)==False:
            isUnique=False
    return isUnique

#function that prints the Sudoku board for playing the game
#parameter board is the Sudoku board with zeros as placements for blanks
def PrintBoard(board):
    print(' COLUMN ',end='')
    for i in range(1,10):
        print('[',str(i),']',end='')
        if i<9:
            print('   ' if i%3==0 else '',end='')
    print('\n ROW   -----------------------------------------------------')
    for i in range(9):
        print('[',str(i+1),']',end=' ')
        for j in range(9):
            print('|  ' if j==0 else '','_' if board[i,j]==0 else board[i,j],'  |  ' if j%3==2 else '  ',end='')
        print('\n       -----------------------------------------------------'if i%3==2 else '\n')             

#function to fill a number on the Sudoku board
#parameter initBoard is the Sudoku board initially generated (for comparing with the full solution board to see which cells are initially empty
#parameter game is the current state of the Sudoku board
#parameter solution is the full Sudoku board solution
#parameter num is the number to be placed in the cell
#parameter rowIndex is a number between 1 and 9 inclusive representing the row index
#parameter colwIndex is a number between 1 and 9 inclusive representing the column index
#return the current status of the Sudoku game board after modification (if any)
def FillNumber(initBoard,game,solution,num,rowIndex,colIndex):
    if initBoard[rowIndex,colIndex]!=0: #trying to replace a clue number initially given by the system
        warnings.warn('Cannot modify a number given on the initial board, please fill in the blank slots only',Warning)
    elif num==0 or num==solution[rowIndex,colIndex]: #correct number selected for the blank or remove a number
        game[rowIndex,colIndex]=num
    else:
        print('Incorrect placement of number, please try again')
    return game

#user prompt to enter the value for the requested type
#parameter type is the type of information required (i.e. number, row index, column index)
#return the user input
def UserPrompt(type):
    while True:
        print('Select a ',type,' from the list: [1] [2] [3] [4] [5] [6] [7] [8] [9]')
        result=int(input())
        if result in INDICES:
            return result
        else:
            print(VALID_PROMPT)

#function to calculate the time used to finish the game
#parameter sec is the total time used in seconds
#returns the time used as a string in the format [h]hours:[m]minutes:[s]seconds
def TimeUsed(secs):
    minutes=int(secs/60)
    hours=int(minutes/60)
    seconds=secs%60
    result='%d seconds' %seconds
    if hours>0:
        results='%d hours % minutes '%(hours, minutes)+result
    else:
        if minutes>0:
            result='%d minutes '%minutes+result
    return result
        
while True:
    print('\n\n\nWelcome to the Sudoku Game\n','please choose a difficulty level by typing in the corresponding option name','\n','\n')
    gameOn=False
    remains=0
    while gameOn==False:
        print(Fore.CYAN+'(E) - EASY','\t','(M) - MEDIUM','\t','(H) - HARD','\t','(EX) - EXPERT')
        print(Fore.LIGHTCYAN_EX+"(Q) - QUIT the game")
        difficulty=input()
        if difficulty=='E':
            remains=random.randint(35,40)
            gameOn=True
        elif difficulty=='M':
            remains=random.randint(30,35)
            gameOn=True
        elif difficulty=='H':
            remains=random.randint(25,30)
            gameOn=True
        elif difficulty=='EX':
            remains=random.randint(20,25)
            gameOn=True
        elif difficulty=='Q':
            break
        else:
            print('Please enter a valid option')

    if not gameOn: #game quit indication
        print(QUITPROMPT)
        break
    print("Generating the Sudoku board ...")
    solution=FillAdjacencyUnits(FillDiagonalUnits(),0,0)
    game=solution.copy()
    blanks=0
    while blanks<81-remains:
        tempGame=RemoveNumbers(game.copy(),random.randint(0,8),random.randint(0,8))
        if UniqueSolution(tempGame.copy(),solution)==True: #if only one unique solution, remove next number
            game=tempGame.copy()
        blanks=np.count_nonzero(game==0)
    initBoard=game.copy()
    startTime=time.time()
    while gameOn:
        PrintBoard(game)
        print(INSTRUCTIONS)
        command=input()
        print('\n\n\n')
        if command=='P' or command=='R':
            num=0
            if command=='P':
                num=UserPrompt('number')
            game=FillNumber(initBoard,game,solution,num,UserPrompt('row position'),UserPrompt('column position'))
        elif command=='C':
            game=initBoard.copy()
            print('The Sudoku board is now cleared',end='\n')
        elif command=='H':
            if HINTS>0:
                blanks=np.where(game==0) #obtain an unfilled cell and fill it with a number from the solution
                rowIndex=blanks[0][random.randint(0,len(blanks[0])-1)]
                colIndex=blanks[1][random.randint(0,len(blanks[0])-1)]
                game=FillNumber(initBoard,game,solution,solution[rowIndex,colIndex],rowIndex,colIndex)
                print(str(solution[rowIndex,colIndex]),' is added to the board at row: ',str(rowIndex+1),', column: ',str(colIndex+1),'\n')
                HINTS-=1
            else:
                print('Sorry, there are no more hint chances left. You can do it!\n')
        elif command=='L':
            print('This is the solution for this Sudoku puzzle:')
            PrintBoard(solution)
            break
        elif command=='S':
            break
        elif command=='Q':
            gameOn=False
        if np.array_equal(game,solution):
            print(WIN_PROMPT)
            print('Time Used: '+TimeUsed(time.time()-startTime),'\n')
            break
        print('Time spent so far since the last input: '+TimeUsed(time.time()-startTime),'\n')
    if gameOn==False:
        print(QUIT_PROMPT)
        break