from tkinter import *
import main
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

        b_square = Image.open(r'../Image/ini_brick.jpg')
        b_square = ImageTk.PhotoImage(b_square.resize((block_size, block_size), Image.ANTIALIAS))

        for r in range(self.size[0]):  # get x
            for c in range(self.size[1]):  # get y
                self.frame_maze.create_image(c*block_size, r*block_size, anchor = NW, image = b_square)
        self.frame_maze.image = [b_square]

        for r in range(0,3025,55):
            self.frame_maze.create_line(0,r,550,r,fill='#E5FFCC')

        for col in range(0,3025,55):
            self.frame_maze.create_line(col,0,col,550,fill='#E6E6FA')

        self.frame_maze.create_text(50,570,fill = "navajo white", font="verdana 15", text = "Score: " )
        self.frame_maze.create_text(100,570,fill = "peru", font="verdana 15", text = self.score )

        self.frame_maze.create_text(455,570,fill = "navajo white", font="verdana 15", text = "Used Arrows: " )
        self.frame_maze.create_text(535,570,fill = "peru", font="verdana 15", text = self.arrow)

    def draw_agent(self):
        agent_img = Image.open(r'../Image/forward.png')
        agent_img = agent_img.resize(
            (block_size, block_size), Image.ANTIALIAS)
        agent_img = ImageTk.PhotoImage(agent_img)
        self.agent = self.frame_maze.create_image(
            self.agent_pos[1]*block_size, self.agent_pos[0]*block_size, anchor=NW, image=agent_img)
        self.frame_maze.image.append(agent_img)