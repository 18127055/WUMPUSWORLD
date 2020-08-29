from tkinter import *
from PIL import Image, ImageTk
from agent import *
import tkinter.font as tkFont

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

def back_menu_d():
    end_frame.destroy()
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

def back_menu_c():
    congra_frame.destroy()
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

def close_program():
    end_frame.destroy()

def end_dlg(s):
    draw_map.destroy()
    if s == 'd':
        global end_frame
        end_frame = Tk()
        end_frame.geometry('300x300+500+150')
        end_frame.resizable(width=False, height=False)
        end_frame.title('GAME OPTION')

        end_game = Canvas(end_frame, width=300, height=300, bg='indigo')

        # resize font
        fontStyleNoti = tkFont.Font(family="Lucida Grande", size=28)
        Label_noti = Label(end_frame, text='GAME OVER', width=10,
                        height=4, bg='indigo', fg='lavender', font=fontStyleNoti)
        Label_noti.place(x=35, y=60)

        # Buttons
        quit_btn = Button(end_game, text="QUIT", command=close_program)
        quit_btn.pack(padx=50, pady=20)
        quit_btn.place(x=40, y=260)

        menu_btn = Button(end_game, text="MENU", command=back_menu_d)
        menu_btn.pack(padx=50, pady=20)
        menu_btn.place(x=220, y=260)

        end_game.pack()
        end_frame.mainloop()

    elif s == 'c':
        global congra_frame
        congra_frame = Tk()
        congra_frame.geometry('300x300+500+150')
        congra_frame.resizable(width=False, height=False)
        congra_frame.title('GAME OPTION')

        end_game = Canvas(congra_frame, width=300, height=300, bg='black')

        # resize font
        fontStyleNoti = tkFont.Font(family="Lucida Grande", size=20) 
        Label_noti = Label(end_frame, text='CONGRATUATIONS', width=20, height=4, bg='mint cream', fg='light coral', font=fontStyleNoti) 
        Label_noti.place(x=0, y=60)

        # Label_score = Label(congra_frame, text=self.score, width=20,
        #                     height=4, fg='#00ffff', bg='black', font=fontStyleScore)
        # Label_score.place(relx=0.5, rely=0.5, anchor='center')

        # Buttons
        quit_btn = Button(end_game, text="QUIT", command=close_program)
        quit_btn.pack(padx=50, pady=20)
        quit_btn.place(x=40, y=260)

        menu_btn = Button(end_game, text="MENU", command=back_menu_c)
        menu_btn.pack(padx=50, pady=20)
        menu_btn.place(x=220, y=260)

        end_game.pack()
        congra_frame.mainloop()

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