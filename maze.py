import json
import random,datetime,csv,os
from enum import Enum
from collections import deque

class COLOR(Enum):
    '''
    This class is created to use the Tkinter colors easily.
    Each COLOR object has two color values.
    The first two objects (dark and light) are for theme and the two color
    values represent the Canvas color and the Maze Line color respectively.
    The rest of the colors are for Agents.
    The first value is the color of the Agent and the second is the color of
    its footprint
    '''
    dark=('gray11','white')
    light=('white','black')
    black=('black','dim gray')
    red=('red3','tomato')
    cyan=('cyan4','cyan4')
    green=('green4','pale green')
    blue=('DeepSkyBlue4','DeepSkyBlue2')
    yellow=('yellow2','yellow2')


class maze:
    '''
    This is the main class to create maze.
    '''
    def __init__(self,rows=10,cols=10):
        '''
        rows--> No. of rows of the maze
        cols--> No. of columns of the maze
        Need to pass just the two arguments. The rest will be assigned automatically
        maze_map--> Will be set to a Dicationary. Keys will be cells and
                    values will be another dictionary with keys=['E','W','N','S'] for
                    East West North South and values will be 0 or 1. 0 means that 
                    direction(EWNS) is blocked. 1 means that direction is open.
        grid--> A list of all cells
        path--> Shortest path from start(bottom right) to goal(by default top left)
                It will be a dictionary
        _win,_cell_width,_canvas -->    _win and )canvas are for Tkinter window and canvas
                                        _cell_width is cell width calculated automatically
        _agents-->  A list of aganets on the maze
        markedCells-->  Will be used to mark some particular cell during
                        path trace by the agent.
        _
        '''
        self.rows=rows
        self.cols=cols
        self.maze_map={}
        self.grid=[]
        self.path={} 
        self._cell_width=50  
        self._win=None 
        self._canvas=None
        self._agents=[]
        self.markCells=[]

    @property
    def grid(self):
        return self._grid
    @grid.setter        
    def grid(self,n):
        self._grid=[]
        y=0
        for n in range(self.cols):
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x,y))
                self.maze_map[x,y]={'E':0,'W':0,'N':0,'S':0}
                x = x + 1 
    def _Open_East(self,x, y):
        '''
        To remove the East Wall of the cell
        '''
        self.maze_map[x,y]['E']=1
        if y+1<=self.cols:
            self.maze_map[x,y+1]['W']=1
    def _Open_West(self,x, y):
        self.maze_map[x,y]['W']=1
        if y-1>0:
            self.maze_map[x,y-1]['E']=1
    def _Open_North(self,x, y):
        self.maze_map[x,y]['N']=1
        if x-1>0:
            self.maze_map[x-1,y]['S']=1
    def _Open_South(self,x, y):
        self.maze_map[x,y]['S']=1
        if x+1<=self.rows:
            self.maze_map[x+1,y]['N']=1
    
    def CreateMaze(self,x=1,y=1,pattern=None,loopPercent=0,saveMaze=False,loadMaze=None,theme:COLOR=COLOR.dark):
        '''
        One very important function to create a Random Maze
        pattern-->  It can be 'v' for vertical or 'h' for horizontal
                    Just the visual look of the maze will be more vertical/horizontal
                    passages will be there.
        loopPercent-->  0 means there will be just one path from start to goal (perfect maze)
                        Higher value means there will be multiple paths (loops)
                        Higher the value (max 100) more will be the loops
        saveMaze--> To save the generated Maze as CSV file for future reference.
        loadMaze--> Provide the CSV file to generate a desried maze
        theme--> Dark or Light
        '''
        _stack=[]
        _closed=[]
        self.theme=theme
        self._goal=(x,y)
        if(isinstance(theme,str)):
            if(theme in COLOR.__members__):
                self.theme=COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')
        def blockedNeighbours(cell):
            n=[]
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d]==0:
                    if d=='E' and (cell[0],cell[1]+1) in self.grid:
                        n.append((cell[0],cell[1]+1))
                    elif d=='W' and (cell[0],cell[1]-1) in self.grid:
                        n.append((cell[0],cell[1]-1))
                    elif d=='N' and (cell[0]-1,cell[1]) in self.grid:
                        n.append((cell[0]-1,cell[1]))
                    elif d=='S' and (cell[0]+1,cell[1]) in self.grid:
                        n.append((cell[0]+1,cell[1]))
            return n
        def removeWallinBetween(cell1,cell2):
            '''
            To remove wall in between two cells
            '''
            if cell1[0]==cell2[0]:
                if cell1[1]==cell2[1]+1:
                    self.maze_map[cell1]['W']=1
                    self.maze_map[cell2]['E']=1
                else:
                    self.maze_map[cell1]['E']=1
                    self.maze_map[cell2]['W']=1
            else:
                if cell1[0]==cell2[0]+1:
                    self.maze_map[cell1]['N']=1
                    self.maze_map[cell2]['S']=1
                else:
                    self.maze_map[cell1]['S']=1
                    self.maze_map[cell2]['N']=1
        def isCyclic(cell1,cell2):
            '''
            To avoid too much blank(clear) path.
            '''
            ans=False
            if cell1[0]==cell2[0]:
                if cell1[1]>cell2[1]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['S']==1 and self.maze_map[cell2]['S']==1:
                    if (cell1[0]+1,cell1[1]) in self.grid and self.maze_map[(cell1[0]+1,cell1[1])]['E']==1:
                        ans= True
                if self.maze_map[cell1]['N']==1 and self.maze_map[cell2]['N']==1:
                    if (cell1[0]-1,cell1[1]) in self.grid and self.maze_map[(cell1[0]-1,cell1[1])]['E']==1:
                        ans= True
            else:
                if cell1[0]>cell2[0]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['E']==1 and self.maze_map[cell2]['E']==1:
                    if (cell1[0],cell1[1]+1) in self.grid and self.maze_map[(cell1[0],cell1[1]+1)]['S']==1:
                        ans= True
                if self.maze_map[cell1]['W']==1 and self.maze_map[cell2]['W']==1:
                    if (cell1[0],cell1[1]-1) in self.grid and self.maze_map[(cell1[0],cell1[1]-1)]['S']==1:
                        ans= True
            return ans
        def BFS(cell):
            '''
            Breadth First Search
            To generate the shortest path.
            This will be used only when there are multiple paths (loopPercent>0) or
            Maze is loaded from a CSV file.
            If a perfect maze is generated and without the load file, this method will
            not be used since the Maze generation will calculate the path.
            '''
            frontier = deque()
            frontier.append(cell)
            path = {}
            visited = {(self.rows,self.cols)}
            while len(frontier) > 0:
                cell = frontier.popleft()
                if self.maze_map[cell]['W'] and (cell[0],cell[1]-1) not in visited:
                    nextCell = (cell[0],cell[1]-1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['S'] and (cell[0]+1,cell[1]) not in visited:    
                    nextCell = (cell[0]+1,cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['E'] and (cell[0],cell[1]+1) not in visited:
                    nextCell = (cell[0],cell[1]+1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['N'] and (cell[0]-1,cell[1]) not in visited:
                    nextCell = (cell[0]-1,cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
            fwdPath={}
            cell=self._goal
            while cell!=(self.rows,self.cols):
                try:
                    fwdPath[path[cell]]=cell
                    cell=path[cell]
                except:
                    print('Path to goal not found!')
                    return
            return fwdPath
        # if maze is to be generated randomly
        if not loadMaze:
            _stack.append((x,y))
            _closed.append((x,y))
            biasLength=2 # if pattern is 'v' or 'h'
            if(pattern is not None and pattern.lower()=='h'):
                biasLength=max(self.cols//10,2)
            if(pattern is not None and pattern.lower()=='v'):
                biasLength=max(self.rows//10,2)
            bias=0

            while len(_stack) > 0:
                cell = []
                bias+=1
                if(x , y +1) not in _closed and (x , y+1) in self.grid:
                    cell.append("E")
                if (x , y-1) not in _closed and (x , y-1) in self.grid:
                    cell.append("W")
                if (x+1, y ) not in _closed and (x+1 , y ) in self.grid:
                    cell.append("S")
                if (x-1, y ) not in _closed and (x-1 , y) in self.grid:
                    cell.append("N") 
                if len(cell) > 0:    
                    if pattern is not None and pattern.lower()=='h' and bias<=biasLength:
                        if('E' in cell or 'W' in cell):
                            if 'S' in cell:cell.remove('S')
                            if 'N' in cell:cell.remove('N')
                    elif pattern is not None and pattern.lower()=='v' and bias<=biasLength:
                        if('N' in cell or 'S' in cell):
                            if 'E' in cell:cell.remove('E')
                            if 'W' in cell:cell.remove('W')
                    else:
                        bias=0
                    current_cell = (random.choice(cell))
                    if current_cell == "E":
                        self._Open_East(x,y)
                        self.path[x, y+1] = x, y
                        y = y + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "W":
                        self._Open_West(x, y)
                        self.path[x , y-1] = x, y
                        y = y - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "N":
                        self._Open_North(x, y)
                        self.path[(x-1 , y)] = x, y
                        x = x - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "S":
                        self._Open_South(x, y)
                        self.path[(x+1 , y)] = x, y
                        x = x + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                else:
                    x, y = _stack.pop()

            ## Multiple Path Loops
            if loopPercent!=0:
                
                x,y=self.rows,self.cols
                pathCells=[(x,y)]
                while x!=self.rows or y!=self.cols:
                    x,y=self.path[(x,y)]
                    pathCells.append((x,y))
                notPathCells=[i for i in self.grid if i not in pathCells]
                random.shuffle(pathCells)
                random.shuffle(notPathCells)
                pathLength=len(pathCells)
                notPathLength=len(notPathCells)
                count1,count2=pathLength/3*loopPercent/100,notPathLength/3*loopPercent/100
                
                #remove blocks from shortest path cells
                count=0
                i=0
                while count<count1: #these many blocks to remove
                    if len(blockedNeighbours(pathCells[i]))>0:
                        cell=random.choice(blockedNeighbours(pathCells[i]))
                        if not isCyclic(cell,pathCells[i]):
                            removeWallinBetween(cell,pathCells[i])
                            count+=1
                        i+=1
                            
                    else:
                        i+=1
                    if i==len(pathCells):
                        break
                #remove blocks from outside shortest path cells
                if len(notPathCells)>0:
                    count=0
                    i=0
                    while count<count2: #these many blocks to remove
                        if len(blockedNeighbours(notPathCells[i]))>0:
                            cell=random.choice(blockedNeighbours(notPathCells[i]))
                            if not isCyclic(cell,notPathCells[i]):
                                removeWallinBetween(cell,notPathCells[i])
                                count+=1
                            i+=1
                                
                        else:
                            i+=1
                        if i==len(notPathCells):
                            break
                self.path=BFS((self.rows,self.cols))
        else:
            # Load maze from CSV file
            with open(loadMaze,'r') as f:
                last=list(f.readlines())[-1]
                c=last.split(',')
                c[0]=int(c[0].lstrip('"('))
                c[1]=int(c[1].rstrip(')"'))
                self.rows=c[0]
                self.cols=c[1]
                self.grid=[]

            with open(loadMaze,'r') as f:
                r=csv.reader(f)
                next(r)
                for i in r:
                    c=i[0].split(',')
                    c[0]=int(c[0].lstrip('('))
                    c[1]=int(c[1].rstrip(')'))
                    self.maze_map[tuple(c)]={'E':int(i[1]),'W':int(i[2]),'N':int(i[3]),'S':int(i[4])}
            self.path=BFS((self.rows,self.cols))
        if saveMaze:
            dt_string = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            with open(f'maze--{dt_string}.csv','w',newline='') as f:
                writer=csv.writer(f)
                writer.writerow(['  cell  ','E','W','N','S'])
                for k,v in self.maze_map.items():
                    entry=[k]
                    for i in v.values():
                        entry.append(i)
                    writer.writerow(entry)
                f.seek(0, os.SEEK_END)
                f.seek(f.tell()-2, os.SEEK_SET)
                f.truncate()

    def _redrawCell(self,x,y,theme):
        '''
        To redraw a cell.
        With Full sized square agent, it can overlap with maze lines
        So the cell is redrawn so that cell lines are on top
        '''
        w=self._cell_width
        cell=(x,y)
        x=x*w-w+self._LabWidth
        y=y*w-w+self._LabWidth
        if self.maze_map[cell]['E']==False:
            self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['W']==False:
            self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['N']==False:
            self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1])
        if self.maze_map[cell]['S']==False:
            self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1])

    def enableArrowKey(self,a):
        '''
        To control an agent a with Arrow Keys
        '''
        self._win.bind('<Left>',a.moveLeft)
        self._win.bind('<Right>',a.moveRight)
        self._win.bind('<Up>',a.moveUp)
        self._win.bind('<Down>',a.moveDown)
    
    def enableWASD(self,a):
        '''
        To control an agent a with keys W,A,S,D
        '''
        self._win.bind('<a>',a.moveLeft)
        self._win.bind('<d>',a.moveRight)
        self._win.bind('<w>',a.moveUp)
        self._win.bind('<s>',a.moveDown)



    _tracePathList=[]
    def _tracePathSingle(self,a,p,kill,showMarked,delay):
        '''
        An interal method to help tracePath method for tracing a path by agent.
        '''
        
        def killAgent(a):
            '''
            if the agent should be killed after it reaches the Goal or completes the path
            '''
            for i in range(len(a._body)):
                self._canvas.delete(a._body[i])
            self._canvas.delete(a._head) 
        w=self._cell_width
        if((a.x,a.y) in self.markCells and showMarked):
            w=self._cell_width
            x=a.x*w-w+self._LabWidth
            y=a.y*w-w+self._LabWidth
            self._canvas.create_oval(y + w/2.5+w/20, x + w/2.5+w/20,y + w/2.5 +w/4-w/20, x + w/2.5 +w/4-w/20,fill='red',outline='red',tag='ov')
            self._canvas.tag_raise('ov')
       
        if (a.x,a.y)==(a.goal):
            del maze._tracePathList[0][0][a]
            if maze._tracePathList[0][0]=={}:
                del maze._tracePathList[0]
                if len(maze._tracePathList)>0:
                    self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
            if kill:
                self._win.after(300, killAgent,a)         
            return
        # If path is provided as Dictionary
        if(type(p)==dict):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                return
            if a.shape=='arrow':
                old=(a.x,a.y)
                new=p[(a.x,a.y)]
                o=a._orient
                
                if old!=new:
                    if old[0]==new[0]:
                        if old[1]>new[1]:
                            mov=3#'W' #3
                        else:
                            mov=1#'E' #1
                    else:
                        if old[0]>new[0]:
                            mov=0#'N' #0

                        else:
                            mov=2#'S' #2
                    if mov-o==2:
                        a._RCW()

                    if mov-o==-2:
                        a._RCW()
                    if mov-o==1:
                        a._RCW()
                    if mov-o==-1:
                        a._RCCW()
                    if mov-o==3:
                        a._RCCW()
                    if mov-o==-3:
                        a._RCW()
                    if mov==o:
                        a.x,a.y=p[(a.x,a.y)]
                else:
                    del p[(a.x,a.y)]
            else:    
                a.x,a.y=p[(a.x,a.y)]
        # If path is provided as String
        if (type(p)==str):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
                if kill:
                    
                    self._win.after(300, killAgent,a)         
                return
            if a.shape=='arrow':
                old=(a.x,a.y)
                new=p[0]
                o=a._orient
                if new=='N': mov=0
                elif new=='E': mov=1
                elif new=='S': mov=2
                elif new=='W': mov=3
                
                if mov-o==2:
                    a._RCW()

                if mov-o==-2:
                    a._RCW()
                if mov-o==1:
                    a._RCW()
                if mov-o==-1:
                    a._RCCW()
                if mov-o==3:
                    a._RCCW()
                if mov-o==-3:
                    a._RCW()
            if a.shape=='square' or mov==o:    
                move=p[0]
                if move=='E':
                    if a.y+1<=self.cols:
                        a.y+=1
                elif move=='W':
                    if a.y-1>0:
                        a.y-=1
                elif move=='N':
                    if a.x-1>0:
                        a.x-=1
                        a.y=a.y
                elif move=='S':
                    if a.x+1<=self.rows:
                        a.x+=1
                        a.y=a.y
                elif move=='C':
                    a._RCW()
                elif move=='A':
                    a._RCCW()
                p=p[1:]
        # If path is provided as List
        if (type(p)==list):
            if(len(p)==0):
                del maze._tracePathList[0][0][a]
                if maze._tracePathList[0][0]=={}:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList)>0:
                        self.tracePath(maze._tracePathList[0][0],kill=maze._tracePathList[0][1],delay=maze._tracePathList[0][2])
                if kill:                    
                    self._win.after(300, killAgent,a)  
                return
            if a.shape=='arrow':
                old=(a.x,a.y)
                new=p[0]
                o=a._orient
                
                if old!=new:
                    if old[0]==new[0]:
                        if old[1]>new[1]:
                            mov=3#'W' #3
                        else:
                            mov=1#'E' #1
                    else:
                        if old[0]>new[0]:
                            mov=0#'N' #0

                        else:
                            mov=2#'S' #2
                    if mov-o==2:
                        a._RCW()

                    elif mov-o==-2:
                        a._RCW()
                    elif mov-o==1:
                        a._RCW()
                    elif mov-o==-1:
                        a._RCCW()
                    elif mov-o==3:
                        a._RCCW()
                    elif mov-o==-3:
                        a._RCW()
                    elif mov==o:
                        a.x,a.y=p[0]
                        del p[0]
                else:
                    del p[0]
            else:    
                a.x,a.y=p[0]
                del p[0]

        self._win.after(delay, self._tracePathSingle,a,p,kill,showMarked,delay)    

    def tracePath(self,d,kill=False,delay=300,showMarked=False):
        '''
        A method to trace path by agent
        You can provide more than one agent/path details
        '''
        self._tracePathList.append((d,kill,delay))
        if maze._tracePathList[0][0]==d: 
            for a,p in d.items():
                if a.goal!=(a.x,a.y) and len(p)!=0:
                    self._tracePathSingle(a,p,kill,showMarked,delay)
    def run(self):
        '''
        Finally to run the Tkinter Main Loop
        '''
        self._win.mainloop()

def maze_to_json(maze):
    data={
        "end_x": 0,
        "end_y": 0,
    }
    data["height"]=maze.rows
    data["weight"]=maze.cols
    data["start_x"]=maze.rows-1
    data["start_y"]=maze.cols-1
    cells = []
    for c in maze.maze_map.keys():
        tmp={}
        tmp["x"]=c[0]-1
        tmp["y"]=c[1]-1
        tmp["content"]=""
        if tmp["x"]==0 and tmp["y"]==0:
            tmp["content"]="\u2665"
        if tmp["x"]==data["start_x"] and tmp["y"]==data["start_y"]:
            tmp["content"]="\u2605"
        tmp["borders"]=[1-maze.maze_map[c]['N'],1-maze.maze_map[c]['E'],1-maze.maze_map[c]['S'],1-maze.maze_map[c]['W']]
        cells.append(tmp)
    cells = sorted(cells, key=lambda d: d['x']) 
    data["cells"]=cells
    return data

m = maze(10,10)
m.CreateMaze(loopPercent= 30)
#print(m.maze_map)

with open("src/maze_easy.json","w") as f:
    f.write(json.dumps(maze_to_json(m)))
#m.run()

m = maze(15,15)
m.CreateMaze(loopPercent= 25)

with open("src/maze_medium.json","w") as f:
    f.write(json.dumps(maze_to_json(m)))

m = maze(20,20)
m.CreateMaze(loopPercent= 22)

with open("src/maze_hard.json","w") as f:
    f.write(json.dumps(maze_to_json(m)))

m = maze(30,30)
m.CreateMaze(loopPercent= 20)

with open("src/maze_ex.json","w") as f:
    f.write(json.dumps(maze_to_json(m)))

