from tkinter import *
import main
import GUI as g
from PIL import Image, ImageTk
from random import randint
from copy import deepcopy
from tkinter import messagebox
import time
import tkinter.font as tkFont
from BFS import A_star

block_size = 55

def manhattan(x, y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

class Wumpus_game(Frame):
    class Agent(Frame):
        def __init__(self, frame_maze, pos, size, master=None):
            super().__init__(master)
            self.agent = None
            self.w_pos = []
            self.m_size = size
            self.KB = [] #in menh de cho vi tri hien tai agent dang dung
            #P, B, W, S, G, OK, V
            self.maze = [[[0,0,0,0,0,0,0] for _ in range(size)] for _ in range(size)]
            self.a_pos = pos[randint(0,len(pos)-1)]
            self.cave = self.a_pos
            self.maze[self.a_pos[0]][self.a_pos[1]] = [0,0,0,0,0,1,0]
            self.frame = frame_maze
            self.path, self.moveable = [], []
            self.maze[self.a_pos[0]][self.a_pos[1]][6] = 1
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
            elif self.maze[p[0]][p[1]][1] != 0  and self.maze[p[0]][p[1]][6] == 0:
                st_kb = 'B[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
                for room in adj_r:
                    if self.maze[room[0]][room[1]][5] == 0 and self.maze[room[0]][room[1]][2] == 0 :
                        self.maze[room[0]][room[1]][0] +=1
                        if len(st_kb) != 0:
                            st_kb += ' v '
                        st_kb += 'P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                    elif self.maze[room[0]][room[1]][5] == 0 and self.maze[room[0]][room[1]][2] != 0:
                        self.maze[room[0]][room[1]][2] = 0
                        #self.maze[room[0]][room[1]][5] = 1
                        self.KB.append('-W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        if self.maze[room[0]][room[1]][0] != 0:
                            self.maze[room[0]][room[1]][0] += 1
                            if len(st_kb) != 0:
                                st_kb += ' v '
                            st_kb += 'P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                        else:
                            self.maze[room[0]][room[1]][5] = 1
                            self.KB.append('-W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                            self.KB.append('OK[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                self.KB.append(st_kb+')')
            #S
            elif self.maze[p[0]][p[1]][3] != 0:
                st_kb = 'S[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[0] + 1)
                for room in adj_r:
                    if self.maze[room[0]][room[1]][5] == 0 and self.maze[room[0]][room[1]][0] == 0 :
                        self.maze[room[0]][room[1]][2] +=1
                        if len(st_kb) != 0:
                            st_kb += ' v '
                        st_kb += 'W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                    elif self.maze[room[0]][room[1]][0] != 0 and self.maze[room[0]][room[1]][5] == 0 :
                        self.maze[room[0]][room[1]][0] = 0
                        #self.maze[room[0]][room[1]][5] = 1
                        self.KB.append('-P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        if self.maze[room[0]][room[1]][2] != 0:
                            self.maze[room[0]][room[1]][2] += 1
                            if len(st_kb) != 0:
                                st_kb += ' v '
                            st_kb += 'W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1)
                        else:
                            self.maze[room[0]][room[1]][5] = 1
                            self.KB.append('-W[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                            self.KB.append('OK[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                        #self.KB.append('P[{i}][{j}]'.format(i=self.m_size-room[0], j= room[1]+1))
                self.KB.append(st_kb+')')
            #empty
            st_kb = 'OK[{i}][{j}] -> ('.format(i = self.m_size-p[0], j= p[1] + 1)
            if self.maze[p[0]][p[1]][3] == 0 and self.maze[p[0]][p[1]][1] == 0 and self.maze[p[0]][p[1]][0] == 0 and self.maze[p[0]][p[1]][2] == 0:
                for room in adj_r:
                    self.maze[room[0]][room[1]][5] = 1
                    if self.maze[room[0]][room[1]][0] != 0:
                        self.maze[room[0]][room[1]][0] = 0
                        self.KB.append('-P[{i}][{j}]'.format(i = self.m_size - room[0], j= room[1]+1))
                    if self.maze[room[0]][room[1]][2] != 0:
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
            #self.path = []
            if len(self.moveable) == 0: #climb
                #dist_cave = [manhattan(self.cave,st) for st in step]
                #self.path.append(step[dist_cave.index(min(dist_cave))])
                self.path = A_star(self.maze,self.cave,self.a_pos)
            else:
                for i in step:
                    if i in self.moveable:
                        self.path= [i]
                        self.moveable.pop(self.moveable.index(i))
                        break
                    self.path = []
                if len(self.path) == 0:
                    dist_a_emp = [manhattan(self.a_pos,move) for move in self.moveable]
                    move_min = self.moveable[dist_a_emp.index(min(dist_a_emp))]
                    #dist_m_step = [manhattan(st,move_min) for st in step]
                    #self.path.append(step[dist_m_step.index(min(dist_m_step))])
                    self.path = A_star(self.maze,move_min, self.a_pos)
        
        def getPercept(self, maze):
            for i in range(7):
                if self.maze[self.a_pos[0]][self.a_pos[1]][i] == 0:
                    self.maze[self.a_pos[0]][self.a_pos[1]][i] = maze[self.a_pos[0]][self.a_pos[1]][i]

        def shoot(self, pos):
            #self.maze[pos[0]][pos[1]][2] = 0
            if self.maze[pos[0]][pos[1]][0] == 0 or self.maze[pos[0]][pos[1]][2] == 3 :
                self.maze[pos[0]][pos[1]][5] = 1
                self.maze[pos[0]][pos[1]][2] = 0
                self.maze[pos[0]][pos[1]][0] = 0
                self.moveable.append(pos)
            n_room = self.adj(pos)
            for room in n_room:
                if self.maze[room[0]][room[1]][3] == 1:
                    self.maze[room[0]][room[1]][2] = 0
                    w_r = self.adj(room)
                    self.maze[room[0]][room[1]][3] = 0
                    for r in w_r:
                        if self.maze[r[0]][r[1]][2] == 1:
                            self.maze[r[0]][r[1]][2] = 0
                        elif self.maze[r[0]][r[1]][2] == 2:
                            self.maze[r[0]][r[1]][3] = 1
            return 's'
        
        def grab(self, pos):
            self.maze[pos[0]][pos[1]][4] = 0
            return 'g'
        
        def action(self): #do 1 action at a time
            #die, grab, shoot, climb, move
            #die
            if self.maze[self.a_pos[0]][self.a_pos[1]][0] == 2 or self.maze[self.a_pos[0]][self.a_pos[1]][2] == 2:
                print(self.KB)
                return 'd', 0
            #grab
            if self.maze[self.a_pos[0]][self.a_pos[1]][4] == 1:
                self.KB.append('G[{i}][{j}] -> Grab[{i}][{j}]'.format(i = self.m_size - self.a_pos[0], j = self.a_pos[1]+1))
                sign = self.grab(self.a_pos)
                print(self.KB)
                if self.maze[self.path[0][0]][self.path[0][1]][6] == 0:
                    self.moveable.append(self.path[0])
                self.path.pop(0)
                return sign, 0
            #shoot
            adj_r = self.adj(self.a_pos)
            wum = [self.maze[room[0]][room[1]][2] for room in adj_r]
            w_ind = wum.index(max(wum))
            room = adj_r[w_ind]
            if self.maze[room[0]][room[1]][2] >= 2:
                self.KB.append('W[{i}][{j}] -> Shoot[{i}][{j}]'.format(i = self.m_size - room[0], j = room[1]+1))
                for ar in adj_r:
                    if room!=ar and self.maze[ar[0]][ar[1]][2] != 0:
                        self.maze[ar[0]][ar[1]][2] -= 1
                sign = self.shoot(room)
                self.maze[room[0]][room[1]][2] = 0
                print(self.KB)
                if self.maze[self.path[0][0]][self.path[0][1]][6] == 0:
                    self.moveable.append(self.path[0])
                self.path.pop(0)
                return sign, room
            #climb
            if len(self.moveable) == 0 and self.a_pos == self.cave:
                print(self.KB)
                return 'c', 0
            #move
            temp = self.a_pos            
            self.a_pos = self.path[0]
            self.maze[self.a_pos[0]][self.a_pos[1]][6] = 1
            self.KB.append('MoveTo[{i}][{j}] -> V[{i}][{j}]'.format(i= self.m_size - self.a_pos[0], j= self.a_pos[1]+1))
            self.path.pop(0)
            print(self.KB)
            return 'm', temp 

        def play(self, maze):
            self.getPercept(maze)
            self.agent_path()
            return self.action()

    def __init__(self, path_file, master=None):
        super().__init__(master)
        self.filename = path_file
        self.arrow, self.score, self.gold, self.wumpus = 0, 0, 0, 0
        self.w_pos, self.maze = [], []
        self.s, self.g, self.brick, self.w = [], [], [], []
        self.readFile()
        self.frame_maze = Canvas(width=self.size*block_size,height = self.size*block_size +50, bg='black')
        self.frame_maze.image = []
        self.a_img = None
        self.agent = Wumpus_game.Agent(self.frame_maze,self.emp_tile,self.size,master)
        self.imgdict = {}
        self.draw_map()
        self.frame_maze.pack()

    def draw_map(self):
        self.frame_maze = Canvas(width=self.size*block_size,height = self.size*block_size +50, bg='black')

        #draw initial bricks
        b_square = Image.open(r'../WUMPUSWORLD/Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))
        self.imgdict["Inital"] = b_square

        #visited bricks
        v_square = Image.open(r'../WUMPUSWORLD/Image/visited_brick.jpg')
        v_square = ImageTk.PhotoImage(v_square.resize((block_size, block_size), Image.ANTIALIAS))
        self.imgdict["Visited"] = v_square

        #gold_img
        gold_img = Image.open(r'../WUMPUSWORLD/Image/gold.png')
        gold_img = ImageTk.PhotoImage(gold_img.resize((30,30),Image.ANTIALIAS))
        self.imgdict["Gold"] = gold_img

        #breeze_img
        breeze_img = Image.open(r'../WUMPUSWORLD/Image/wind.png')
        breeze_img = ImageTk.PhotoImage(breeze_img.resize((30,30), Image.ANTIALIAS))
        self.imgdict["Breeze"] = breeze_img

        #stench_img
        stench_img = Image.open(r'../WUMPUSWORLD/Image/stench.png')
        stench_img = ImageTk.PhotoImage(stench_img.resize((30,30), Image.ANTIALIAS))
        self.imgdict["Stech"] = stench_img
        
        #wumpus_img
        wumpus_img = Image.open(r'../WUMPUSWORLD/Image/w1.png')
        wumpus_img = ImageTk.PhotoImage(wumpus_img.resize((70,50), Image.ANTIALIAS))
        self.imgdict["Wumpus"] = wumpus_img

        #pit_img
        pit_img = Image.open(r'../WUMPUSWORLD/Image/pit_1.png')
        pit_img = ImageTk.PhotoImage(pit_img.resize((50,50), Image.ANTIALIAS))
        self.imgdict["Pit"] = pit_img

        for r in range(self.size):  # get x
            for c in range(self.size):  # get y    
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = v_square)
        self.frame_maze.image = [v_square]

        #draw lines between squares
        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,55*self.size,r,fill='black')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,55*self.size,fill='black')

        for r in range(10):
            for c in range(10):
                if self.maze[r][c][1] == 1:
                    self.frame_maze.create_image(c*block_size+10, r*block_size+28, anchor = NW, image = breeze_img)
                if self.maze[r][c][0] == 1:
                    self.frame_maze.create_image(c*block_size+5, r*block_size+5, anchor = NW, image = pit_img)
                if self.maze[r][c][2] == 1:
                    self.w.append([self.frame_maze.create_image(c*block_size-2, r*block_size, anchor = NW, image = wumpus_img), (r,c)])
                    self.wumpus +=1
                if self.maze[r][c][3] == 1:
                    self.s.append([self.frame_maze.create_image(c*block_size+10, r*block_size-2, anchor = NW, image = stench_img), (r,c)])
                if self.maze[r][c][4] == 1:
                    self.g.append([self.frame_maze.create_image(c*block_size+20, r*block_size+5, anchor = NW, image = gold_img), (r,c)])
                    self.gold +=1

        self.frame_maze.image.append(gold_img)
        self.frame_maze.image.append(breeze_img)
        self.frame_maze.image.append(pit_img)
        self.frame_maze.image.append(wumpus_img)
        self.frame_maze.image.append(stench_img)

        for r in range(self.size):  # get y - i
            temp = []
            for c in range(self.size):  # get x - j   
                temp.append(self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square))
            self.brick.append(temp)
        self.frame_maze.image.append(b_square)

        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,55*self.size,r,fill='black')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,55*self.size,fill='black')

        #draw score
        score_img = Image.open(r'../WUMPUSWORLD/Image/score.png')
        score_img = ImageTk.PhotoImage(score_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(15, 55*self.size + 10, anchor = NW, image = score_img)
        self.frame_maze.image.append(score_img)

        # self.frame_maze.create_text(70,55*self.size + 25,fill = "navajo white", font="purisa 10", text = "Score: " )
        # self.frame_maze.create_text(120,55*self.size + 25,fill = "#E6E6FA", font="purisa 10", text = self.score )
        Label_score = Label(self.frame_maze, text='Score: ',bg = 'black', fg='navajo white', font = 'purisa 10') 
        Label_score.place(x=60, y=55*self.size+15)
        global r_score
        r_score = Label(self.frame_maze, text= self.score ,fg='#E6E6FA', bg = 'black', font = 'purisa 10') 
        r_score.place(x=110, y=55*self.size+15)

        #draw used arrows
        arrow_img = Image.open(r'../WUMPUSWORLD/Image/arrow.png')
        arrow_img = ImageTk.PhotoImage(arrow_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(410, 55*self.size + 10, anchor = NW, image = arrow_img)
        self.frame_maze.image.append(arrow_img)

        # self.frame_maze.create_text(485,55*self.size + 25,fill = "navajo white", font="purisa 10", text = "Used Arrows: " )
        # self.frame_maze.create_text(535,55*self.size + 25,fill = "#E6E6FA", font="purisa 10", text = self.arrow)
        Label_arrow = Label(self.frame_maze, text='Used Arrows: ',bg = 'black', fg='navajo white', font = 'purisa 10') 
        Label_arrow.place(x=445, y=55*self.size+14)
        global r_arrow
        r_arrow = Label(self.frame_maze, text= self.arrow ,fg='#E6E6FA', bg = 'black', font = 'purisa 10') 
        r_arrow.place(x=530, y=55*self.size+14)

        #draw golds
        gold_img = Image.open(r'../WUMPUSWORLD/Image/gold.png')
        gold_img = ImageTk.PhotoImage(gold_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(190, 55*self.size + 10, anchor = NW, image = gold_img)
        self.frame_maze.image.append(gold_img)

        # self.frame_maze.create_text(280,55*self.size + 25,fill = "navajo white", font="purisa 10", text = "Remaining Golds: " )
        # self.frame_maze.create_text(340,55*self.size + 25,fill = "#E6E6FA", font="purisa 10", text = self.gold)
        Label_gold = Label(self.frame_maze, text='Remainning Golds: ',bg = 'black', fg='navajo white', font = 'purisa 10') 
        Label_gold.place(x=220, y=55*self.size+14)
        global r_gold
        r_gold = Label(self.frame_maze, text= self.gold ,fg='#E6E6FA', bg = 'black', font = 'purisa 10') 
        r_gold.place(x=340, y=55*self.size+14)

        #agent_img
        agent_img = Image.open(r'../WUMPUSWORLD/Image/right.png')
        agent_img = agent_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
        agent_img = ImageTk.PhotoImage(agent_img)
        self.imgdict["Right"] = agent_img

        cave_img = Image.open(r'../WUMPUSWORLD/Image/cave.png')
        cave_img = ImageTk.PhotoImage(cave_img.resize((55,55), Image.ANTIALIAS))

        self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor=NW, image=cave_img)
        self.frame_maze.image.append(cave_img)

        self.frame_maze.delete(self.brick[self.agent.a_pos[0]][self.agent.a_pos[1]])
        self.brick[self.agent.a_pos[0]][self.agent.a_pos[1]] = None
        self.a_img = self.frame_maze.create_image(
                self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor=NW, image=agent_img)
        self.frame_maze.image.append(agent_img)

        left_img = Image.open(r'../WUMPUSWORLD/Image/left.png')
        left_img = left_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
        left_img = ImageTk.PhotoImage(left_img)
        self.frame_maze.image.append(left_img)
        self.imgdict["Left"] = left_img

        up_img = Image.open(r'../WUMPUSWORLD/Image/backward.png')
        up_img = up_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
        up_img = ImageTk.PhotoImage(up_img)
        self.frame_maze.image.append(up_img)
        self.imgdict["Up"] = up_img

        down_img = Image.open(r'../WUMPUSWORLD/Image/forward.png')
        down_img = down_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
        down_img = ImageTk.PhotoImage(down_img)
        self.frame_maze.image.append(down_img)
        self.imgdict["Down"] = down_img

    def Play(self):
        sign = 'm'
        while sign not in ['c','d','o']:
            sign, r = self.agent.play(deepcopy(self.maze))
            sign = self.spe_move(sign, r)
            self.agent.KB = []
            time.sleep(0.2)
        
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

    def direction(self, cur, n_pos):
        if cur[1] > n_pos[1]:
            return 'l'
        elif cur[1] < n_pos[1]:
            return 'r'
        elif cur[0] > n_pos[0]:
            return 'u'
        elif cur[0] < n_pos[0]:
            return 'd'
    
    def move(self, cur, n_pos):
        dir = self.direction(cur, n_pos)
        if dir == 'l':
            self.frame_maze.delete(self.a_img)
            self.a_img = self.frame_maze.create_image(cur[1]*block_size, cur[0]*block_size, anchor = NW, image = self.imgdict["Left"])
            self.frame_maze.after(50)
            self.frame_maze.update()
            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(self.brick[n_pos[0]][n_pos[1]])
            self.brick[n_pos[0]][n_pos[1]] = None
            self.a_img = self.frame_maze.create_image(n_pos[1]*block_size, n_pos[0]*block_size, anchor = NW, image = self.imgdict["Left"])
            self.frame_maze.after(50)
            self.frame_maze.update()
        elif dir == 'r':
            self.frame_maze.delete(self.a_img)
            self.a_img = self.frame_maze.create_image(cur[1]*block_size, cur[0]*block_size, anchor = NW, image = self.imgdict["Right"])
            self.frame_maze.after(50)
            self.frame_maze.update()
            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(self.brick[n_pos[0]][n_pos[1]])
            self.brick[n_pos[0]][n_pos[1]] = None
            self.a_img = self.frame_maze.create_image(n_pos[1]*block_size, n_pos[0]*block_size, anchor = NW, image = self.imgdict["Right"])
            self.frame_maze.after(50)
            self.frame_maze.update()
        elif dir == 'u':
            self.frame_maze.delete(self.a_img)
            self.a_img = self.frame_maze.create_image(cur[1]*block_size, cur[0]*block_size, anchor = NW, image = self.imgdict["Up"])
            self.frame_maze.after(50)
            self.frame_maze.update()
            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(self.brick[n_pos[0]][n_pos[1]])
            self.brick[n_pos[0]][n_pos[1]] = None
            self.a_img = self.frame_maze.create_image(n_pos[1]*block_size, n_pos[0]*block_size, anchor = NW, image = self.imgdict["Up"])
            self.frame_maze.after(50)
            self.frame_maze.update()
        elif dir == 'd':
            self.frame_maze.delete(self.a_img)
            self.a_img = self.frame_maze.create_image(cur[1]*block_size, cur[0]*block_size, anchor = NW, image = self.imgdict["Down"])
            self.frame_maze.after(50)
            self.frame_maze.update()
            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(self.brick[n_pos[0]][n_pos[1]])
            self.brick[n_pos[0]][n_pos[1]] = None
            self.a_img = self.frame_maze.create_image(n_pos[1]*block_size, n_pos[0]*block_size, anchor = NW, image = self.imgdict["Down"])
            self.frame_maze.after(50)
            self.frame_maze.update()
        
        self.maze[n_pos[0]][n_pos[1]][5] = 1
        self.maze[n_pos[0]][n_pos[1]][6] = 1
        self.frame_maze.pack()

    def shoot(self, wum_pos):
        dir = self.direction(self.agent.a_pos, wum_pos)
        if self.maze[wum_pos[0]][wum_pos[1]][2]==0:
            return
        if dir == 'l':
            tup_pos = [t[1] for t in self.w]
            i = tup_pos.index((wum_pos[0], wum_pos[1]))
            del_w = self.w[i][0]

            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(del_w)
            self.a_img = self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor = NW, image = self.imgdict["Left"])
            self.frame_maze.delete(self.brick[wum_pos[0]][wum_pos[1]])
            self.frame_maze.update()
            self.brick[wum_pos[0]][wum_pos[1]] = None

        elif dir == 'r':
            tup_pos = [t[1] for t in self.w]
            i = tup_pos.index((wum_pos[0], wum_pos[1]))
            del_w = self.w[i][0]

            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(del_w)
            self.a_img = self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor = NW, image = self.imgdict["Right"])
            self.frame_maze.delete(self.brick[wum_pos[0]][wum_pos[1]])
            self.frame_maze.update()
            self.brick[wum_pos[0]][wum_pos[1]] = None
        elif dir == 'u':
            tup_pos = [t[1] for t in self.w]
            i = tup_pos.index((wum_pos[0], wum_pos[1]))
            del_w = self.w[i][0]

            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(del_w)
            self.a_img = self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor = NW, image = self.imgdict["Up"])
            self.frame_maze.delete(self.brick[wum_pos[0]][wum_pos[1]])
            self.frame_maze.update()
            self.brick[wum_pos[0]][wum_pos[1]] = None
        elif dir == 'd':
            tup_pos = [t[1] for t in self.w]
            i = tup_pos.index((wum_pos[0], wum_pos[1]))
            del_w = self.w[i][0]

            self.frame_maze.delete(self.a_img)
            self.frame_maze.delete(del_w)
            self.a_img = self.frame_maze.create_image(self.agent.a_pos[1]*block_size, self.agent.a_pos[0]*block_size, anchor = NW, image = self.imgdict["Down"])
            self.frame_maze.delete(self.brick[wum_pos[0]][wum_pos[1]])
            self.frame_maze.update()
            self.brick[wum_pos[0]][wum_pos[1]] = None

        self.maze[wum_pos[0]][wum_pos[1]][2] = 0
        self.maze[wum_pos[0]][wum_pos[1]][5] = 1
        a_room = self.agent.adj(wum_pos)
        for room in a_room:
            n_room = self.agent.adj(room)
            check_s = 0
            for ad_n_room in n_room:
                if self.maze[ad_n_room[0]][ad_n_room[1]][2] == 1:
                    check_s += 1
            if check_s == 0:
                stench_pos = [t[1] for t in self.s]
                i = stench_pos.index((room[0], room[1]))
                del_s = self.s[i][0]
                self.frame_maze.delete(del_s)
                self.frame_maze.update()
                self.s.pop(i)
                self.maze[room[0]][room[1]][3] = 0

        self.frame_maze.pack()
    
    def g_score(self):
        self.gold -= 1
        self.score +=100
        r_score.config(text = self.score)
        r_score.update()
        r_gold.config(text = self.gold)
        r_gold.update()
    
    def m_score(self):
        self.score -=10
        r_score.config(text = self.score)
        r_score.update()

    def c_score(self):
        self.score +=10
        r_score.config(text = self.score)
        r_score.update()

    def s_score(self):
        self.wumpus -=1
        self.score -=100
        self.arrow +=1
        r_score.config(text = self.score)
        r_score.update()
        r_arrow.config(text = self.arrow)
        r_arrow.update()
    
    def d_score(self):
        self.score -=10000
        r_score.config(text = self.score)
        r_score.update()
    
    def spe_score(self):
        self.score = self.score
        r_score.config(text = self.score)
        r_score.update()

    def spe_move(self, sign, pos):
        if self.gold == 0 and self.wumpus == 0:
            self.spe_score()
            self.agent.moveable = []
            self.agent.a_pos = self.agent.cave
            self.frame_maze.destroy()
            g.end_dlg('c',self.score)
            return 'o'
        if sign == 'd':
            self.d_score()
            self.frame_maze.destroy()
            self.frame_maze.update()
            g.end_dlg('d', self.score)
            return 'd'
        elif sign == 'g':
            tup_pos = [t[1] for t in self.g]
            i = tup_pos.index((self.agent.a_pos[0], self.agent.a_pos[1]))
            del_food = self.g[i][0]
            self.frame_maze.delete(del_food)
            self.g_score()
            time.sleep(0.1)
            self.maze[self.agent.a_pos[0]][self.agent.a_pos[1]][4]=0
            return 'g'
        elif sign == 'c':
            self.c_score()
            self.frame_maze.destroy()
            g.end_dlg('c',self.score)
            return 'c'
        elif sign == 'm':
            self.move(pos, self.agent.a_pos)
            self.m_score()
            return 'm'
        elif sign == 's': #shoot
            self.shoot(pos)
            self.s_score()
            return 's'
