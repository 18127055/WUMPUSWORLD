from tkinter import *
import main
from PIL import Image, ImageTk
from random import randint

block_size = 55

class Wumpus_game(Frame):
    class Agent(Frame):
        def __init__(self, frame_maze, pos, size, master=None):
            super().__init__(master)
            self.agent = None
            self.arrow = 0
            self.score = 0
            self.w_pos = []
            self.KB = [] #in menh de cho vi tri hien tai agent dang dung
            self.maze = [[[0,0,0,0,0,0,0] for _ in range(size)] for _ in range(size)]
            self.agent_pos = pos[randint(0,len(pos)-1)]
            self.maze[self.agent_pos[0]][self.agent_pos[1]] = [0,0,0,0,0,1,0]
            self.frame = frame_maze
            self.visited, self.path = [], []
            if self.agent_pos[0] == 0:
                if self.agent_pos[1] == 0:
                    self.maze[0][1], self.maze[1][0] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[10][1] -> (OK[9][1] ^ OK[10][2])')
                elif self.agent_pos[1] == size - 1:
                    self.maze[0][size - 2], self.maze[1][size - 1] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[10][10] -> (OK[10][9] ^ OK[9][10])')
                else:
                    self.maze[0][self.agent_pos[1]+1],self.maze[0][self.agent_pos[1]-1], self.maze[1][self.agent_pos[1]+1] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[10][{i}] -> (OK[10][{j}] ^ OK[10][{k}] ^ OK[9][{i}])'.format(i = self.agent_pos[1] + 1, j = self.agent_pos[1], k = self.agent_pos[1] + 2))
            elif self.agent_pos[0] == size - 1:
                if self.agent_pos[1] == 0:
                    self.maze[size -1][1], self.maze[size -2][0] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[1][1] -> (OK[2][1] ^ OK[1][2])')
                elif self.agent_pos[1] == size - 1:
                    self.maze[size -1][size - 2], self.maze[size -2][size - 1] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[1][10] -> (OK[1][9] ^ OK[2][10])')
                else:
                    self.maze[size -1][self.agent_pos[1]+1],self.maze[0][self.agent_pos[1]-1], self.maze[1][self.agent_pos[1]+1] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[1][{i}] -> (OK[1][{j}] ^ OK[1][{k}] ^ OK[2][{i}])'.format(i = self.agent_pos[1] + 1, j = self.agent_pos[1], k = self.agent_pos[1]+2))
            else:
                if self.agent_pos[1] == 0:
                    self.maze[self.agent_pos[0]][1], self.maze[self.agent_pos[0]-1][0], self.maze[self.agent_pos[0]+1][0] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[{i}][1] -> (OK[{j}][1] ^ OK[{i}][2] ^ OK[{k}][1])'.format(i = size - self.agent_pos[0], j = size - self.agent_pos[0] -1, k = size - self.agent_pos[0] + 1 ))
                elif self.agent_pos[1] == size - 1:
                    self.maze[self.agent_pos[0]][size - 2], self.maze[self.agent_pos[0] - 1][size - 1], self.maze[self.agent_pos[0] + 1][size - 1] = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[{i}][10] -> (OK[{j}][10] ^ OK[{i}][9] ^ OK[{k}][10])'.format(i = size - self.agent_pos[0], j = size - self.agent_pos[0] -1, k = size - self.agent_pos[0] + 1 ))
                else:
                    self.maze[self.agent_pos[0]][self.agent_pos[1]+1],self.maze[self.agent_pos[0]][self.agent_pos[1]-1], self.maze[self.agent_pos[0]+1][self.agent_pos[1]], self.maze[self.agent_pos[0]-1][self.agent_pos[1]]  = [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]
                    self.KB.append('OK[{i1}][{j1}] -> (OK[{i2}][{j1}] ^ OK[{i3}][{j1}] ^ OK[{i1}][{j2}] ^ OK[{i1}][{j3}])'.format(i1 = size - self.agent_pos[0], j1 = self.agent_pos[1]+1, i2 = size - self.agent_pos[0] -1, i3 = size - self.agent_pos[0] +1, j2 = self.agent_pos[1], j3 = self.agent_pos[1] +2))
            self.KB.append('V[{i}][{j}]'.format(i = size - self.agent_pos[0], j = self.agent_pos[1] + 1))
            #self.draw_agent()
        
        def draw_agent(self):
                agent_img = Image.open(r'../Image/right.png')
                agent_img = agent_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
                agent_img = ImageTk.PhotoImage(agent_img)
                self.agent = self.frame.create_image(
                        self.agent_pos[1]*block_size, self.agent_pos[0]*block_size, anchor=NW, image=agent_img)
                self.frame.image.append(agent_img)
                self.maze[self.agent_pos[0]][self.agent_pos[1]][6] = 1
                print(self.KB)
                print('P, B, W, S, G, OK, V')
    
    def __init__(self, path_file, master=None):
        super().__init__(master)
        self.filename = "../Map/" + path_file
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
        b_square = Image.open(r'../Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))

        for r in range(self.size):  # get x
            for c in range(self.size):  # get y
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square)
        self.frame_maze.image.append(b_square)

        #draw visited_brick: initial agent's position
        v_square = Image.open(r'../Image/visited_brick.jpg')
        v_square = ImageTk.PhotoImage(v_square.resize((block_size, block_size), Image.ANTIALIAS))
        self.frame_maze.create_image(self.agent.agent_pos[1]*block_size, self.agent.agent_pos[0]*block_size, anchor = NW, image = v_square)
        self.frame_maze.image.append(v_square)

        #draw lines between squares
        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,55*self.size,r,fill='black')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,55*self.size,fill='black')

        #draw score
        score_img = Image.open(r'../Image/score.png')
        score_img = ImageTk.PhotoImage(score_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(15, 55*self.size + 10, anchor = NW, image = score_img)
        self.frame_maze.image.append(score_img)

        self.frame_maze.create_text(70,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Score: " )
        self.frame_maze.create_text(120,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.score )

        #draw used arrows
        arrow_img = Image.open(r'../Image/arrow.png')
        arrow_img = ImageTk.PhotoImage(arrow_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(410, 55*self.size + 10, anchor = NW, image = arrow_img)
        self.frame_maze.image.append(arrow_img)

        self.frame_maze.create_text(485,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Used Arrows: " )
        self.frame_maze.create_text(535,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.arrow)

        #draw golds
        gold_img = Image.open(r'../Image/gold.png')
        gold_img = ImageTk.PhotoImage(gold_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(190, 55*self.size + 10, anchor = NW, image = gold_img)
        self.frame_maze.image.append(gold_img)

        self.frame_maze.create_text(280,55*self.size + 25,fill = "navajo white", font="verdana 10", text = "Remaining Golds: " )
        self.frame_maze.create_text(340,55*self.size + 25,fill = "#E6E6FA", font="verdana 10", text = self.gold)
    
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