from importlib.metadata import entry_points
import random
import time

cell = "c"
wall = "w"
border="b"

univisited = "u"


def maze_intit(x, y):

    global maze
    maze = []

    
    for j in range(y):
        maze.append([])

        for i in range(x):
            maze[j].append(univisited)
    #for row in range(len(maze)):
        #print(str(maze[row]).replace("'","").replace("[",'').replace("]","").replace(",",''))

    return maze


def create_inner_walls():
    for i in range(0,len(maze)):
        for j in range(0,len(maze[i]), 2):
            maze[i][j] = wall
            
    for i in range(2,len(maze),2):
        for j in range(0,len(maze[0])):
            maze[i][j] = wall


    #for row in range(len(maze)):
     #   print(str(maze[row]).replace("'","").replace("[",'').replace("]","").replace(",",''))
    
    return maze


def create_walls():
    for i in range(len(maze)):
        maze[i][0] = border
        maze[i][-1] = border
        for j in range(len(maze[i])):
            maze[0][j] = border
            maze[-1][j] = border
    

    #debug
    #for row in range(len(maze)):
     #   print(str(maze[row]).replace("'","").replace("[",'').replace("]","").replace(",",''))

    return maze


open_points = []
def createEnterExit():
    forbidden_point = []
    for i in range(2):
        entry_side = random.randint(1,4)
        forbidden_point.append(entry_side)
        while entry_side in forbidden_point:
            entry_side = random.randint(1,4)
        forbidden_point.append(entry_side)

        
        if entry_side == 1:
            entry_y = random.randrange(1,len(maze[0])-2,2)
            entry_x = 0
        elif entry_side == 2:
            entry_y = random.randrange(1,len(maze[0])-2,2)
            entry_x = -1
        elif entry_side == 3: 
            entry_y = 0  
            entry_x = random.randrange(1,len(maze)-2,2)
        elif entry_side == 4:
            entry_y = -1
            entry_x = random.randrange(1,len(maze)-2,2)
       # j'utilise 1 et -2 pour ne pas générer de points dans les coins 
        
        maze[entry_x][entry_y] = cell
        open_points.append([entry_x,entry_y])

    #for row in range(len(maze)):
     #  print(str(maze[row]).replace("'","").replace("[",'').replace("]","").replace(",",''))
    return maze


def createWay():
    current_cell = open_points[0]
    for i in range(5):
        path = []
        print(current_cell)

   # vérifier qu'il n'y a pas > 1 cellules c à côté sinon ne pas append le path
        if maze[current_cell[0]][current_cell[1]-1] == univisited:
            path.append([[current_cell[0]],[current_cell[1]-1]])
                

        if maze[current_cell[0]][current_cell[1]+1] == univisited:
            path.append([[current_cell[0]],[current_cell[1]+1]])


        if maze[current_cell[0]-1][current_cell[1]] == univisited:
            path.append([[current_cell[0]-1],[current_cell[1]]])


        if maze[current_cell[0]+1][current_cell[1]] == univisited:
            path.append([[current_cell[0]+1],[current_cell[1]]])

        
        choosenPath = random.choice(path)
        print(path, choosenPath)

        print(choosenPath, choosenPath[0][0], choosenPath[1][0])
        maze[choosenPath[0][0]][choosenPath[1][0]] = cell
        current_cell = [choosenPath[0][0],choosenPath[1][0]]

        #for row in range(len(maze)):
         #   print(str(maze[row]).replace("'","").replace("[",'').replace("]","").replace(",",''))

    
    return maze


def recursive_backtracking():
    
    current_cell = [1, 1]
    cells = []
    maze[current_cell[0]][current_cell[1]] = cell
    

    while True:
        if len(cells) > 1:
            if current_cell[0]+2 >= len(maze) or current_cell[0]-2 <= 0 or current_cell[1]+2 >= len(maze[0]) or current_cell[1]-2 <= 0 :
                #print("went back")
                #print(cells)
                cells.pop()
                try:
                    current_cell=cells[len(cells)-1]
                except:
                    break
            
    
        
        #print(current_cell[0]+2,len(maze))
        # probleme : des fois cellSouth > height max, donc crash
        cellNorth = maze[current_cell[0]-2][current_cell[1]]
        cellSouth = maze[current_cell[0]+2][current_cell[1]]
        cellEast = maze[current_cell[0]][current_cell[1]+2]
        cellWest = maze[current_cell[0]][current_cell[1]-2]

        #while cellNorth != cell and cellSouth != cell and cellEast != cell and cellWest != cell:
        possiblePath = []
        if cellNorth == univisited:
            possiblePath.append("N")

        if cellSouth == univisited:
            possiblePath.append("S")

        if cellEast == univisited:
            possiblePath.append("E")

        if cellWest == univisited:
            possiblePath.append("W")
        
        
        
        if len(possiblePath) != 0:
            choosenPath = random.choice(possiblePath)
            #print(possiblePath, choosenPath, current_cell)

            if choosenPath == "N":
                maze[current_cell[0]-1][current_cell[1]] = cell
                maze[current_cell[0]-2][current_cell[1]] = cell
                current_cell = [current_cell[0]-2,current_cell[1]]
                

            if choosenPath == "S":
                maze[current_cell[0]+1][current_cell[1]] = cell
                maze[current_cell[0]+2][current_cell[1]] = cell
                current_cell = [current_cell[0]+2,current_cell[1]]
                

            if choosenPath == "E":
                maze[current_cell[0]][current_cell[1]+1] = cell
                maze[current_cell[0]][current_cell[1]+2] = cell
                current_cell = [current_cell[0],current_cell[1]+2]
                

            if choosenPath == "W":
                maze[current_cell[0]][current_cell[1]-1] = cell
                maze[current_cell[0]][current_cell[1]-2] = cell
                current_cell = [current_cell[0],current_cell[1]-2]
            cells.append(current_cell)

        else:
            #print("went back")
            #print(cells)
            cells.pop()
            try:
                current_cell=cells[len(cells)-1]
            except:
                break
            

        print("\r\n")
        #Affichage du labyrinthe et de sa construction
        showMaze=[]
        for row in range(len(maze)):
                showMaze.append(str(maze[row]).replace("'","").replace("u",' ').replace("[",'').replace("]","").replace(",",'').replace('b','■').replace("w",'■').replace("c",' '))
                showMaze.append("\n")
        print("".join(showMaze),end="\r")
        time.sleep(0.01)


    return maze

#la cellule vérifie si apres c'est déja visité (cellule + 2 car mur entre) et si oui il part de + 1 donc forcement mur + 2 ca sera un mur.
maze_intit(41,41)
create_inner_walls()
create_walls()
createEnterExit()
recursive_backtracking()

#ajouter 1 élement qui ne sera pas affiché dans la matrice mais ca décalerait tout

#createWay()
