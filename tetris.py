#################################################
# 15-112-n19 hw-tetris
# Your Name:Haoyuan Wei
# Your Andrew ID:haoyuanw
# Your Section:A
# Collaborators: no
#################################################

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *
import math
import random
# et's define how we'll represent the pieces.
# In this design, the falling piece is represented
# by a 2-dimensional list of booleans, indicating
# whether the given cell is or is not painted in this piece.
def pieces():
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False],[True, True, True]]
    lPiece = [[False, False, True],[True, True, True]]
    oPiece = [[True, True],[True, True]]
    sPiece = [[False, True, True],[True, True, False]]
    tPiece = [[False, True, False],[True, True, True]]
    zPiece = [[True, True, False],[False, True, True]]
    #  Put 7 of these piece types into a single list, tetrisPieces
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    # define colors corresponding to each of these pieces,
    # and place them in a list of the same size
    tetrisPieceColors =\
        ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    return (tetrisPieces, tetrisPieceColors)
# The newFallingPiece function (which takes one parameter,
# data, and returns nothing) is responsible for randomly
# choosing a new piece, setting its color,
# and positioning it in the middle of the top row.
# Then we set the data values holding the fallingPiece and
# the fallingPieceColor to the randomIndex-ed elements from
# the lists of tetrisPieces and tetrisPieceColors.
def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    pieceWidth = len(data.fallingPiece[0])
    data.fallingPieceCol = data.cols // 2 - pieceWidth // 2
# After calling drawBoard, you should then call a new function
# drawFallingPiece (which takes canvas and data), so that the
# falling piece is drawn over the board
# However, we have to add the offset of the left-top row and column
# (that is, fallingPieceRow and fallingPieceCol) so that the it
# is properly positioned on the board. Also, note that this step
# requires that we add an additional parameter to the drawCell
# function -- the color to fill the cell.
def drawFallingPiece(canvas, data):
    for rows in range(len(data.fallingPiece)):
        for cols in range(len(data.fallingPiece[0])):
            if data.fallingPiece[rows][cols]:
                data.board[data.fallingPieceRow + rows]\
                    [cols + data.fallingPieceCol] = data.fallingPieceColor
                drawCell(canvas,data,
                         rows + data.fallingPieceRow,
                         cols + data.fallingPieceCol)
                data.board[data.fallingPieceRow + rows]\
                        [cols + data.fallingPieceCol] = ''
# see whether the block is at the bottom by
# looping though the board under the piece
def pieceStop(data):
    rowBelow = data.fallingPieceRow + len(data.fallingPiece)
    while rowBelow > data.fallingPieceRow:
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece\
                    [rowBelow - data.fallingPieceRow - 1][col] == True and\
                    (rowBelow >= data.rows or
                     data.board[rowBelow][col + data.fallingPieceCol]!=''):
                return True
        rowBelow -= 1
    return False
# put the piece onto the board
def placeFallingPiece(data):
    for rows in range(len(data.fallingPiece)):
        for cols in range(len(data.fallingPiece[0])):
            if data.fallingPiece[rows][cols]:
                data.board[data.fallingPieceRow + rows]\
                    [cols + data.fallingPieceCol] = data.fallingPieceColor
# Writing the fallingPieceIsLegal() function:
# it confirms that: (1) the cell is in
# fact on the board; and (2) the color at that location
# on the board is the emptyColor. If either of these
# checks fails, the function immediately returns False.
# If all the checks succeed for every True cell in the
# fallingPiece, the function returns True.
def fallingPieceIsLegal(data):
    pieceWidth = len(data.fallingPiece[0])
    #  the cell is in fact on the board
    if pieceWidth + data.fallingPieceCol > data.cols:
        return False
    elif data.fallingPieceCol < 0:
        return False
    elif data.fallingPieceRow + len(data.fallingPiece) > data.rows:
        return False
    elif data.fallingPieceRow < 0:
        return False
    # the color at that location on the board is the emptyColor.
    # doing it by looping through the blocks in falling piece
    else:
        for rows in range(len(data.fallingPiece)):
            for cols in range(len(data.fallingPiece[0])):
                if data.fallingPiece[rows][cols] and \
                        data.board[data.fallingPieceRow + rows]\
                                [cols + data.fallingPieceCol] != "":
                    return False
    return True


# First, we simply
# make the move by modifying the data values storing
# the location of the left-top corner of the falling
# piece. Next, we test if this new location of the
# falling piece is legal. We do this using top-down
# design, so we assume the function fallingPieceIsLegal
# exists at this point (we'll actually write it in a moment).
def moveFallingPiece(data,x,y):
    if x == -1:
        data.fallingPieceCol -= 1
        if not fallingPieceIsLegal(data):
            data.fallingPieceCol += 1
    elif x == 1:
        data.fallingPieceCol += 1
        if not fallingPieceIsLegal(data):
            data.fallingPieceCol -= 1
    elif y == 1:
        data.fallingPieceRow += 1
        if not fallingPieceIsLegal(data):
            data.fallingPieceRow -= 1
# rotate the falling piece in the following steps
# Store the data associated with the old piece
# (its dimensions, location, and the piece itself)
# into temporary local variables.
# Compute the number of new rows and new
# columns according to the old dimensions.
# Compute the new location of the piece
# according to the old location.
# Generate a new 2D list based on the new
# dimensions, and fill it with None values.
# Iterate through each of the cells in the
# original piece, and move each value to its new location in the new piece.
# Set fallingPiece and the other variables equal to their new values.
def rotateFallingPiece(data):
    oldRow = data.fallingPieceRow
    oldNumRows = len(data.fallingPiece)
    newNumRows = len(data.fallingPiece[0])
    newRow = oldRow + oldNumRows // 2 - newNumRows // 2
    oldCol = data.fallingPieceCol
    oldNumCols = len(data.fallingPiece[0])
    newNumCols = len(data.fallingPiece)
    newCol = oldCol + oldNumCols // 2 - newNumCols // 2
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    newPiece = []
    for col in range(len(data.fallingPiece[0])):
        row = []
        for rows in data.fallingPiece:
            row.append(rows[col])
        newPiece = [row] + newPiece
    data.fallingPiece = newPiece
# check the new piece is at the top but cannot move
def isGameOver(data):
    if data.fallingPieceRow == 0 and pieceStop(data):
        data.gameOver = True
# loop through the board and pop the empty rows
def removeFullRows(data):
    rowIndex = len(data.board) - 1
    while rowIndex >= 0:
        if '' not in data.board[rowIndex]:
            data.board.pop(rowIndex)
            data.board = [[''for i in range(len(data.board[0]))]] + \
                         data.board
            data.score += 1
            rowIndex += 1
        rowIndex -= 1
# Setting up the game:
# In the init function, we'll set data.rows and data.cols to 15 for rows
# and 10 for cols with a data.margin of 25. We will then use the data.rows,
# data.cols, data.width, data.height, and data.margin values to determine
# the cellSize so the board just fits with the appropriate margins.
def init(data):
    data.rows = 15
    data.cols = 10
    data.margin = 25
    data.cellWidth = (data.width - 2 * data.margin) // data.cols
    data.cellHeight = (data.height - 2 * data.margin) // data.rows
    data.board = [["" for i in range(data.cols)] for j in range(data.rows)]
    data.tetrisPieces, data.tetrisPieceColors = pieces()
    newFallingPiece(data)
    data.gameOver = False
    data.timePassed = 0
    data.score = 0
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if event.keysym == "r":# restart
        init(data)
    # we modify the keyPressed handler to
    # call moveFallingPiece to move left,
    # right, or down in response to left-arrow,
    # right-arrow, or down-arrow key presses.
    elif event.keysym == "Left":
        moveFallingPiece(data, -1, 0)
    elif event.keysym == "Right":
        moveFallingPiece(data, 1, 0)
    elif event.keysym == "Down":
        moveFallingPiece(data, 0, 1)
    elif event.keysym == 'Up':
        rotateFallingPiece(data)
        if not fallingPieceIsLegal(data):
            rotateFallingPiece(data)
            rotateFallingPiece(data)
            rotateFallingPiece(data)
# he drawCell function must draw the given cell using
# the color stored in the board corresponding to that
# cell (that is, in board[row][col]). We'll draw the
# cell with a rectangle in the cell's color and an
# extra-large outline.
def drawCell(canvas, data, row, col):
    frameWidth = 5
    x0, y0 = col * data.cellWidth + data.margin, \
             row * data.cellHeight + data.margin
    x1, y1 = x0 + data.cellWidth, y0 + data.cellHeight
    canvas.create_rectangle(x0, y0, x1, y1,
                            fill=data.board[row][col], width=frameWidth)
# draw the grid in blue,and the yellow background
def drawBackground(canvas, data):
    frameWidth = 5
    fillColor = "#FFB266"
    canvas.create_rectangle(0,0,data.width,data.height,fill=fillColor)
    for i in range(data.cols):
        for j in range(data.rows):
            x0, y0 = i * data.cellWidth +\
                     data.margin, j * data.cellHeight + data.margin
            x1, y1 = x0 + data.cellWidth, y0 + data.cellHeight
            canvas.create_rectangle(x0,y0,x1,y1,
                                    fill="blue", width=frameWidth)
            drawCell(canvas, data, j, i)
def timerFired(data):
    halfSecond = 5
    data.timePassed += 1
    if not data.gameOver:
        if pieceStop(data):
            placeFallingPiece(data)
            removeFullRows(data)
            newFallingPiece(data)
            isGameOver(data)
        elif data.timePassed % halfSecond == 0:# move every half a second
            data.fallingPieceRow += 1

# To draw the board in the drawBoard function, we simply
# iterate over every cell (with two variables running over
# every row and column) and repeatedly call the drawCell
# function, which takes 4 parameters: the canvas, the data,
# the row of the cell, and the col of the cell.
def drawBoard(canvas, data):
    for i in range(data.cols):
        for j in range(data.rows):
            drawCell(canvas, data, j, i)
def drawGameOver(canvas, data):
    bandHeight = 3
    fontSize = 36
    # have a band
    canvas.create_rectangle(data.margin, data.margin + data.cellHeight,
                            data.width - data.margin,
                            data.margin + bandHeight * data.cellHeight,
                            fill='grey', width=0)
    canvas.create_text((data.width - data.margin)/2,
                       data.margin + data.cellHeight \
                       * (1 + bandHeight)//2,text="GAME OVER!",
                       fill='gold',font="Times "+str(fontSize))
# draw the score at the top of the screen
def drawScore(canvas, data):
    fontSize = 24
    fillColor = '#00008B'
    canvas.create_text(data.width//2, 0,
                       anchor=N, text="Score: " + str(data.score),
                       font='Times '+str(fontSize)+' bold',fill= fillColor)
def redrawAll(canvas, data):
    drawBackground(canvas, data)
    drawBoard(canvas,data)
    drawFallingPiece(canvas, data)
    drawScore(canvas,data)
    if data.gameOver:
        drawGameOver(canvas,data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


def playTetris(rows=15, cols=10):
    # use the rows and cols to compute the appropriate window size
    square = 35
    margin = 25
    width = cols * square + margin * 2
    height = rows * square + margin * 2
    run(width, height)

playTetris()
