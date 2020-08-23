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
            self.maze = [[[0,0,0,0,0,0] for _ in range(size)] for _ in range(size)]
            self.maze[size-1][0] = [0,0,0,0,0,1]
            self.frame = frame_maze
            self.agent_pos = pos
            self.draw_agent()
        
        def draw_agent(self):
                agent_img = Image.open(r'../Image/right.png')
                agent_img = agent_img.resize(
                        (block_size, block_size), Image.ANTIALIAS)
                agent_img = ImageTk.PhotoImage(agent_img)
                self.agent = self.frame.create_image(
                        self.agent_pos[1]*block_size, self.agent_pos[0]*block_size, anchor=NW, image=agent_img)
                self.frame.image.append(agent_img)

    def __init__(self, path_file, master=None):
        super().__init__(master)
        self.filename = "../Map/" + path_file
        self.arrow, self.score, self.gold = 0, 10000, 5
        self.w_pos, self.maze = [], []
        self.readFile()
        self.frame_maze = Canvas(width=self.size*block_size,height = self.size*block_size, bg='black')
        self.draw_map()
        self.agent = Wumpus_game.Agent(self.frame_maze,(self.size-1,0),self.size,master)
        self.frame_maze.pack()

    def draw_map(self):
        self.frame_maze = Canvas(width=self.size*block_size,height = self.size*block_size +50, bg='black')

        #draw initial bricks
        b_square = Image.open(r'../Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))

        for r in range(self.size):  # get x
            for c in range(self.size):  # get y
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square)
        self.frame_maze.image = [b_square]

        #draw visited_brick: initial agent's position
        v_square = Image.open(r'../Image/visited_brick.jpg')
        v_square = ImageTk.PhotoImage(v_square.resize((block_size, block_size), Image.ANTIALIAS))
        self.frame_maze.create_image(0*block_size, (self.size-1)*block_size, anchor = NW, image = v_square)
        self.frame_maze.image.append(v_square)

        #draw lines between squares
        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,55*self.size,r,fill='#E5FFCC')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,55*self.size,fill='#E6E6FA')

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
            #[0,0,0,0,0,0]: P B W S G OK
            self.maze = [[[0,0,0,0,0,0] for _ in range(self.size)] for _ in range(self.size)]
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