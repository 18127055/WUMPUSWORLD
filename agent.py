from tkinter import *
import main
from PIL import Image, ImageTk
from random import randint
from copy import deepcopy

block_size = 55

def manhattan(x, y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

class Wumpus_game(Frame):
    class Agent(Frame):
        def __init__(self, frame_maze, pos, size, master=None):
            super().__init__(master)
            self.agent = None
            self.arrow = 0
            self.score = 0
            self.w_pos = []
            self.m_size = size
            self.KB = [] #in menh de cho vi tri hien tai agent dang dung
            #P, B, W, S, G, OK, V
            self.maze = [[[0,0,0,0,0,0,0] for _ in range(size)] for _ in range(size)]
            self.a_pos = pos[randint(0,len(pos)-1)]
            self.cave = self.a_pos
            self.maze[self.a_pos[0]][self.a_pos[1]] = [0,0,0,0,0,1,0]
            self.frame = frame_maze
            self.visited, self.path, self.moveable = [], [], []
            #self.draw_agent()
        
        def draw_agent(self):
                agent_img = Image.open(r'../WUMPUSWORLD/Image/right.png')
                agent_img = agent_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
                agent_img = ImageTk.PhotoImage(agent_img)
                self.agent = self.frame.create_image(
                        self.a_pos[1]*block_size, self.a_pos[0]*block_size, anchor=NW, image=agent_img)
                self.frame.image.append(agent_img)
                self.maze[self.a_pos[0]][self.a_pos[1]][6] = 1
                print(self.KB)
                #print('P, B, W, S, G, OK, V')

        def adj(self, p = None):
            adj_room = []
            if p == None:
                p = self.a_pos
            #right
            if p[1] != self.m_size -1:
                adj_room.append((p[0],p[1]+1))
            #left
            if p[1] != 0:
                adj_room.append((p[0],p[1]-1))
            #down
            if p[0] != self.m_size -1:
                adj_room.append((p[0]+1,p[1]))
            #up
            if p[0] != 0:
                adj_room.append((p[0]-1,p[1])) 
            return adj_room  
        
        def checkIfBSO(self,adj_r):
            p = self.a_pos
            step = []
            #BS
            if self.maze[p[0]][p[1]][1] != 0 and self.maze[p[0]][p[1]][3] != 0:
                st_kb = 'BS[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
                for room in adj_r:
                    if self.maze[room[0]][room[1]][5] == 0:
                        self.maze[room[0]][room[1]][0] +=1
                        self.maze[room[0]][room[1]][2] +=1
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        if len(st_kb) != 0:
                            st_kb += ' v '
                        st_kb += 'P[{i}][{j}] V W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                self.KB.append(st_kb + ')')
            #B
            elif self.maze[p[0]][p[1]][1] != 0:
                st_kb = 'B[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
                for room in adj_r:
                    if self.maze[room[0]][room[1]][5] == 0 or self.maze[room[0]][room[1]][2] == 0 :
                        self.maze[room[0]][room[1]][0] +=1
                    elif self.maze[room[0]][room[1]][2] != 0:
                        self.maze[room[0]][room[1]][2] = 0
                        self.KB.append('-W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        if self.maze[room[0]][room[1]][0] != 0:
                            self.maze[room[0]][room[1]][0] += 1
                        else:
                            self.maze[room[0]][room[1]][5] = 1
                            self.KB.append('OK[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                    if len(st_kb) != 0:
                        st_kb += ' v '
                    st_kb += 'P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                self.KB.append(st_kb)
            #S
            elif self.maze[p[0]][p[1]][3] != 0:
                st_kb = 'S[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
                for room in adj_r:
                    if self.maze[room[0]][room[1]][5] == 0 or self.maze[room[0]][room[1]][0] == 0 :
                        self.maze[room[0]][room[1]][2] +=1
                    elif self.maze[room[0]][room[1]][0] != 0:
                        self.maze[room[0]][room[1]][0] = 0
                        self.KB.append('-P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        if self.maze[room[0]][room[1]][2] != 0:
                            self.maze[room[0]][room[1]][2] += 1
                        else:
                            self.maze[room[0]][room[1]][5] = 1
                            self.KB.append('OK[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                    if len(st_kb) != 0:
                        st_kb += ' v '
                    st_kb += 'W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                self.KB.append(st_kb)
            #empty
            st_kb = 'OK[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
            if self.maze[p[0]][p[1]][3] == 0 and self.maze[p[0]][p[1]][1] == 0 and self.maze[p[0]][p[1]][0] == 0 and self.maze[p[0]][p[1]][2] == 0:
                for room in adj_r:
                    self.maze[room[0]][room[1]][5] = 1
                    if self.maze[room[0]][room[1]][0] == 1:
                        self.maze[room[0]][room[1]][0] = 0
                        self.KB.append('-P[{i}][{j}]'.format(i = self.m_size - room[0], j= room[1]+1))
                    if self.maze[room[0]][room[1]][2] == 1:
                        self.maze[room[0]][room[1]][2] = 0
                        self.KB.append('-W[{i}][{j}]'.format(i = self.m_size - room[0], j= room[1]+1))
                    if self.maze[room[0]][room[1]][6] == 0 and room not in self.moveable:
                        self.moveable.append(room)
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                    if len(st_kb) != 0:
                        st_kb += ' ^ '
                    st_kb += 'OK[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                self.KB.append(st_kb + ')')
            for room in adj_r:
                if self.maze[room[0]][room[1]][5] == 1:
                    step.append(room)
            return step

        def agent_path(self):
            adj_r = self.adj()
            step = self.checkIfBSO(adj_r)
            self.path = []
            for i in step:
                if i in self.moveable:
                    self.path.append(i)
                    del self.moveable[self.moveable.index(i)]
                    break
                self.path = []
            if len(self.path) == 0:
                dist_a_emp = [manhattan(self.a_pos,move) for move in self.moveable]
                move_min = self.moveable[dist_a_emp.index(min(dist_a_emp))]
                dist_m_step = [manhattan(st,move_min) for st in step]
                self.path.append(step[dist_m_step.index(min(dist_m_step))])
        
        def getPercept(self, maze):
            for i in range(7):
                if self.maze[self.a_pos[0]][self.a_pos[1]][i] == 0:
                    self.maze[self.a_pos[0]][self.a_pos[1]][i] = maze[self.a_pos[0]][self.a_pos[1]][i]

        def shoot(self, pos):
            self.maze[pos[0]][pos[1]][2] = 0
            self.maze[pos[0]][pos[1]][5] = 1
            return 's'
        
        def grab(self, pos):
            self.maze[pos[0]][pos[1]][4] = 0
            return 'g'
        
        def action(self): #do 1 action at a time
            #shoot, move, grab, climb, die
            #die
            if self.maze[self.a_pos[0]][self.a_pos[1]][0] != 0 or self.maze[self.a_pos[0]][self.a_pos[1]][2] != 0:
                print(self.KB)
                return 'd', 0
            #grab
            if self.maze[self.a_pos[0]][self.a_pos[1]][4] == 1:
                self.KB.append('G[{i}][{j}] -> Grab[{i}][{j}]'.format(i = self.size - self.a_pos[0], j = self.a_pos[1]+1))
                sign = self.grab(self.a_pos)
                print(self.KB)
                return sign, 0
            #shoot
            adj_r = self.adj(self.a_pos)
            for room in adj_r:
                if self.maze[room[0]][room[1]][2] == 2:
                    self.KB.append('W[{i}][{j}] -> Shoot[{i}][{j}]'.format(i = self.size - room[0], j = room[1]+1))
                    sign = self.shoot(room)
                    print(self.KB)
                    return sign, room
            #climb
            if len(self.moveable) == 0 and self.a_pos == self.cave:
                print(self.KB)
                return 'c', 0
            #move
            self.a_pos = self.path[0]
            self.maze[self.a_pos[0]][self.a_pos[1]][6] = 1
            self.KB.append('MoveTo[{i}][{j}] -> V[{i}][{j}]'.format(i= self.m_size - self.a_pos[0], j= self.a_pos[1]+1))
            self.path.pop(0)
            print(self.KB)
            return 'm', 0

        def play(self, maze):
            self.getPercept(maze)
            self.agent_path()
            return self.action()

    def __init__(self, path_file, master=None):
        super().__init__(master)
        self.filename = "../WUMPUSWORLD/Map/" + path_file
        self.arrow, self.score, self.gold = 0, 10000, 5
        self.w_pos, self.maze = [], []
        self.readFile()
        self.frame_maze = Canvas(width=self.size*block_size,height = self.size*block_size +50, bg='black')
        self.frame_maze.image = []
        self.agent = Wumpus_game.Agent(self.frame_maze,self.emp_tile,self.size,master)
        self.draw_map()
        self.agent.draw_agent()
        self.frame_maze.pack()

    def draw_map(self):
        #draw initial bricks
        b_square = Image.open(r'../WUMPUSWORLD/Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))

        for r in range(self.size):  # get x
            for c in range(self.size):  # get y
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square)
        self.frame_maze.image.append(b_square)

        #draw visited_brick: initial agent's position
        v_square = Image.open(r'../WUMPUSWORLD/Image/visited_brick.jpg')
        v_square = ImageTk.PhotoImage(v_square.resize((block_size, block_size), Image.ANTIALIAS))
        self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor = NW, image = v_square)
        self.frame_maze.image.append(v_square)

        #draw lines between squares
        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,55*self.size,r,fill='black')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,55*self.size,fill='black')

        #draw score
        score_img = Image.open(r'../WUMPUSWORLD/Image/score.png')
        score_img = ImageTk.PhotoImage(score_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(15, 55*self.size + 10, anchor = NW, image = score_img)
        self.frame_maze.image.append(score_img)

        self.frame_maze.create_text(70,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Score: " )
        self.frame_maze.create_text(120,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.score )

        #draw used arrows
        arrow_img = Image.open(r'../WUMPUSWORLD/Image/arrow.png')
        arrow_img = ImageTk.PhotoImage(arrow_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(410, 55*self.size + 10, anchor = NW, image = arrow_img)
        self.frame_maze.image.append(arrow_img)

        self.frame_maze.create_text(485,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Used Arrows: " )
        self.frame_maze.create_text(535,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.arrow)

        #draw golds
        gold_img = Image.open(r'../WUMPUSWORLD/Image/gold.png')
        gold_img = ImageTk.PhotoImage(gold_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(190, 55*self.size + 10, anchor = NW, image = gold_img)
        self.frame_maze.image.append(gold_img)

        self.frame_maze.create_text(280,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Remaining Golds: " )
        self.frame_maze.create_text(340,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.gold)
    
    def Play(self):
        sign, r = self.agent.play(deepcopy(self.maze))
        while sign not in ['c','d']:
            sign, r = self.agent.play(deepcopy(self.maze))
        

    def readFile(self):
        with open(self.filename) as f:
            self.size = int(f.readline())
            #[0,0,0,0,0,0,0]: P B W S G OK V
            self.maze = [[[0,0,0,0,0,0,0] for _ in range(self.size)] for _ in range(self.size)]
            self.emp_tile = []
            for i in range(self.size):
                t = f.readline().split('.')
                for j in range(self.size):
                    tem = t[j].strip()
                    for k in tem:
                        if k == 'P':
                            self.maze[i][j][0]=1
                        elif k == 'B':
                            self.maze[i][j][1]=1
                        elif k == 'W':
                            self.maze[i][j][2]=1
                        elif k == 'S':
                            self.maze[i][j][3]=1
                        elif k == 'G':
                            self.maze[i][j][4]=1
                        elif k == '-':
                            self.maze[i][j][5]=1
                            self.emp_tile.append((i,j))