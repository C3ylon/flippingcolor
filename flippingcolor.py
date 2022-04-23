import turtle
import random


def InitBoard():
    # define color set
    global COLORSET
    COLORSET = { 1:"red", 2:"orange", 3:"blue", 4:"green", 5:"purple" }

    # generate a 5*5 game BOARD, which is filled with random numbers from 1-5
    global BOARD
    BOARD = [[random.randint(1, 5) for _ in range(5)] for _ in range(5)]

    # set screen properties
    global SCREEN
    SCREEN = turtle.Screen()
    SCREEN.title("Flipping Color")
    SCREEN.onclick(ClickEvent)
    SCREEN.tracer(False)

    # set base tile properties, later will clone tiles from base tile
    basetile = turtle.Turtle()
    basetile.shape("square")
    basetile.shapesize(2)
    basetile.penup()

    # set selected tile's outline properties
    global OUTLINE
    OUTLINE = turtle.Turtle()
    OUTLINE.hideturtle()
    OUTLINE.width(10)

    # define whether a tile is selected from the game board
    global CHOSEN
    CHOSEN = False

    # define game board tiles in a list
    global TILELIST
    TILELIST = [[basetile.clone() for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            TILELIST[i][j].color(COLORSET.get(BOARD[i][j]))
            TILELIST[i][j].goto(-100+j*50, 180-i*50)

    # define color set in a list
    global SETLIST
    SETLIST = [basetile.clone() for _ in range(5)]
    for i in range(5):
        SETLIST[i].color(COLORSET.get(i + 1))
        SETLIST[i].goto(-100+i*50, -120)

    # make base tile unvisiable
    basetile.hideturtle()

    # refresh screen
    SCREEN.update()

def PaintOutline(i, j):
    # clear the previous outline before starting to draw a new one
    UnpaintOutline()

    global OUTLINE
    OUTLINE.penup()
    OUTLINE.goto(-75+j*50, 180-i*50)
    OUTLINE.pendown()
    OUTLINE.right(90)
    OUTLINE.forward(25)
    for _ in range(3):
        OUTLINE.right(90)
        OUTLINE.forward(50)
    OUTLINE.right(90)
    OUTLINE.forward(25)
    OUTLINE.left(90)

def UnpaintOutline():
    global OUTLINE
    OUTLINE.clear()

def WinCheck():
    color = BOARD[0][0]
    for i in range(5):
        for j in range(5):
            if BOARD[i][j] != color:
                return False
    return True

def ClickEvent(x, y):
    global CHOSEN, I_CHOSEN, J_CHOSEN

    # if click in game board: 
    if x >= -120 and x <= 120 and y>= -40 and y <= 200:
        for i in range(5):
            for j in range(5):
                if x >= -120+j*50 and x <= -80+j*50 and y >= 160-i*50 and y <= 200-i*50:
                    CHOSEN, I_CHOSEN, J_CHOSEN = True, i, j
                    PaintOutline(i, j)
                    SCREEN.update()

    # if click in color set area: 
    elif x >= -120 and x <= 120 and y >= -140 and y <= -100:
        for i in range(5):
            if x >= -120+i*50 and x <= -80+i*50 and CHOSEN:
                FlipTile(I_CHOSEN, J_CHOSEN, i + 1)
                CHOSEN = False
                UnpaintOutline()
                for i in range(5):
                    for j in range(5):
                        TILELIST[i][j].color(COLORSET.get(BOARD[i][j]))
                SCREEN.update()
                if(WinCheck()):
                    writer = turtle.Turtle()
                    writer.hideturtle()
                    writer.color("orange")
                    writer.penup()
                    writer.goto(0, -240)
                    writer.write("CONGRATULATIONS!",align="center",font=("Arial", 30, ("bold","italic")))
                    writer.color("gray")
                    writer.penup()
                    writer.goto(0, -280)
                    writer.write("press ESC to quit",align="center",font=("Arial", 24, "normal"))
                    SCREEN.update()
                    SCREEN.onkey(SCREEN.bye, "Escape")
                    SCREEN.listen()

    # if click in blank area： 
    else:
        UnpaintOutline()

def FlipTile(i, j, colornum):
    state = [[0]*5 for _ in range(5)]
    previous = BOARD[i][j]
    def DFS(i, j):
        # return if searched or if color is not equal to the selected tile's color
        if state[i][j] or BOARD[i][j] != previous:
            return
        state[i][j] = 1
        BOARD[i][j] = colornum
        if j - 1 >= 0:
            DFS(i, j - 1)
        if j + 1 < 5:
            DFS(i, j + 1)
        if i - 1 >= 0:
            DFS(i - 1, j)
        if i + 1 < 5:
            DFS(i + 1, j)
    DFS(i, j)

def main():
    InitBoard()
    return "game start"

if __name__ == "__main__":
    msg = main()
    print(msg)
    # begin event loop
    SCREEN.mainloop()