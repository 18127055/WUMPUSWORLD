from tkinter import *
from PIL import Image, ImageTk
from agent import *

def clear_entry(event, entry):
    entry.delete(0, END)

def myClick(event = NONE):
    path_file = input_entry.get()
    ini_frame.destroy()
    global draw_map
    draw_map = Tk()
    w, h = (draw_map.winfo_screenwidth()-10 *
            block_size)//2, (draw_map.winfo_screenheight()-10*block_size)//2
    draw_map.geometry('+'+str(w)+'+'+str(h-60))
    draw_map.resizable(width=False, height=False)
    draw_map.title('GAME')
    game = Wumpus_game(path_file,draw_map)
    game.Play()
    draw_map.mainloop()

def menu():
    global ini_frame
    ini_frame = Tk()
    ini_frame.geometry('700x500+300+80')
    ini_frame.resizable(width=False, height=False)
    ini_frame.title('WUMPUS WORLD')

    #create background
    background = Canvas(ini_frame, width=1000, height=1000, bg='black')
    bg_img = Image.open(r'../WUMPUSWORLD/Image/neon.jpg')
    bg_img = ImageTk.PhotoImage(bg_img.resize((700,500), Image.ANTIALIAS))
    background.create_image(0, 0, anchor= NW, image=bg_img)

    background_img = Image.open(r'../WUMPUSWORLD/Image/logo4.png')
    background_img = ImageTk.PhotoImage(background_img.resize((700, 400), Image.ANTIALIAS))
    background.create_image(0, 0, anchor= NW, image=background_img)

    #create input dialog
    global input_entry
    input_entry = Entry(ini_frame)
    input_entry.place(x = 240, y = 335, width = 300, height = 40)
    input_entry.config(highlightbackground="cadet blue", highlightthickness=2)
    placeholder_text = 'Input map path here: '
    input_entry.insert(0, placeholder_text)
    input_entry.bind("<Button-1>", lambda event: clear_entry(event, input_entry))
    input_entry.bind('<Return>', myClick)
    
    #create open button
    button_img = Image.open(r'../WUMPUSWORLD/Image/video-player.png')
    button_img = ImageTk.PhotoImage(button_img.resize((35, 35), Image.ANTIALIAS))
    lv2_btn = Button(ini_frame, text="LEVEL 2", command = myClick, borderwidth=0)
    lv2_btn.pack(padx=50, pady=20)
    lv2_btn.place(x = 550, y = 337)
    lv2_btn.config(height = 35, width = 35, activebackground='black', image=button_img)

    #create Wumpus image
    wumpus_img = Image.open(r'../WUMPUSWORLD/Image/wumpus.png')
    wumpus_img = ImageTk.PhotoImage(wumpus_img.resize((80, 120), Image.ANTIALIAS))
    background.create_image(150, 310, anchor= NW, image=wumpus_img)

    background.pack()
    ini_frame.mainloop()

#def end_dlg():



# from tkinter import *
# import time

# def update_the_label():
#     updated_text = time.strftime("The GM time now is %H:%M:%S.", time.gmtime())
#     w.config(text = updated_text)

# root = Tk()
# w = Label(root, text = "Hello, world!")
# b = Button(root, text = "Update the label", command = update_the_label)
# w.pack()
# b.pack()

# root.mainloop()