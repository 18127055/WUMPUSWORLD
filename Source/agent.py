from tkinter import *
import main
import GUI
from PIL import Image, ImageTk
from random import randint

block_size = 55

class agent(Frame):
    def __init__(self, path, master=None):
        super().__init__(master)
        self.size, self.agent_pos = (10,10), (0,0)
        self.path = path
        self.agent = None
        self.arrow = 0
        self.score = 0
        self.w_pos = []
        self.draw_map()
        self.draw_agent()
        self.frame_maze.pack()

    def draw_map(self):
        self.frame_maze = Canvas(width=self.size[1]*block_size,height = 600, bg='black')

        #draw initial squares
        b_square = Image.open(r'../Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))

        for r in range(self.size[0]):  # get x
            for c in range(self.size[1]):  # get y
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square)
        self.frame_maze.image = [b_square]

        #draw lines between squares
        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,550,r,fill='#E5FFCC')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,550,fill='#E6E6FA')

        #draw score
        score_img = Image.open(r'../Image/score.png')
        score_img = ImageTk.PhotoImage(score_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(15, 560, anchor = NW, image = score_img)
        self.frame_maze.image.append(score_img)

        self.frame_maze.create_text(70,575,fill = "navajo white", font="verdana 10", text = "Score: " )
        self.frame_maze.create_text(97,575,fill = "#E6E6FA", font="verdana 10", text = self.score )

        #draw used arrows
        arrow_img = Image.open(r'../Image/arrow.png')
        arrow_img = ImageTk.PhotoImage(arrow_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(410, 560, anchor = NW, image = arrow_img)
        self.frame_maze.image.append(arrow_img)

        self.frame_maze.create_text(485,575,fill = "navajo white", font="verdana 10", text = "Used Arrows: " )
        self.frame_maze.create_text(535,575,fill = "#E6E6FA", font="verdana 10", text = 0)

        #draw golds
        gold_img = Image.open(r'../Image/gold.png')
        gold_img = ImageTk.PhotoImage(gold_img.resize((30,30), Image.ANTIALIAS))

        self.frame_maze.create_image(190, 560, anchor = NW, image = gold_img)
        self.frame_maze.image.append(gold_img)

        self.frame_maze.create_text(280,575,fill = "navajo white", font="verdana 10", text = "Remaining Golds: " )
        self.frame_maze.create_text(340,575,fill = "#E6E6FA", font="verdana 10", text = 0)

    def draw_agent(self):
        agent_img = Image.open(r'../Image/forward.png')
        agent_img = agent_img.resize(
            (block_size, block_size), Image.ANTIALIAS)
        agent_img = ImageTk.PhotoImage(agent_img)
        self.agent = self.frame_maze.create_image(
            self.agent_pos[1]*block_size, self.agent_pos[0]*block_size, anchor=NW, image=agent_img)
        self.frame_maze.image.append(agent_img)