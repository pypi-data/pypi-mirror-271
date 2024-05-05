from tkinter import ttk
import tkinter
import os
import sys
from PIL import Image, ImageTk 
from tkinter import font
import platform

def ShowMSBox(master, Icon="Information", Title="Message Box", IconStyle="Windows 10", button1="", button2="", button3="", text="This is an info"):
    MsB = tkinter.Toplevel(master)
    StyleList = ["Windows 11","Windows 10", "Windows 7", "Personalized"]
    if not IconStyle in StyleList:
        raise ValueError("Invalid Style : " + IconStyle + ". It should be one of 'Windows 11', 'Windows 10', 'Windows 7' or 'Personalized'.")

    if IconStyle == "Windows 11":
        Style="W11"
    elif IconStyle == "Windows 10":
        Style="W10"
    elif IconStyle == "Windows 7":
        Style="W7"

    if Icon == "Warning":
        IconPath = "1.png"
    elif Icon == "Check":
        IconPath = "2.png"
    elif Icon == "Error":
        IconPath = "3.png"
    elif Icon == "Question":
        IconPath = "4.png"
    elif Icon == "Information":
        IconPath = "5.png"
    else:
        if IconStyle == "Personalized":
            Path = Icon
        else:
            raise ValueError("Invalid Icon : " + Icon + ". It should be one of 'Warning', 'Check', 'Error', 'Question', or 'Information'.")
    
    if IconStyle == "Personalized":
        Path = Icon
    else:
        Path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons', Style, IconPath)

    whiteWall = ttk.Frame(master=MsB, width=1000, height=1000, borderwidth=0)
    whiteWall.place(x=0, y=0)

    photo = Image.open(os.path.realpath(Path))
    photo = photo.resize((64, 64))
    photo = ImageTk.PhotoImage(photo)
    image = ttk.Label(master=MsB, text="", image=photo)
    image.place(x=20, y=35)

    colorFrame = tkinter.Frame(master=MsB, bg="#e2e2e2", width=400, height=100)
    colorFrame.place(x=0, y=140)

    button_pressed = None
    def btn1IsPushed():
        nonlocal button_pressed
        button_pressed = button1
        MsB.destroy()
        master.focus_set()
    def btn2IsPushed():
        nonlocal button_pressed
        button_pressed = button2
        MsB.destroy()
        master.focus_set()
    def btn3IsPushed():
        nonlocal button_pressed
        button_pressed = button3
        MsB.destroy()
        master.focus_set()

    if button1!="":
        MsBbtn1 = ttk.Button(master=MsB, text=button1, command=btn1IsPushed)
        MsBbtn1.place(x=10, y=155)
        style = ttk.Style()
        style.configure("BW.TButton", background=colorFrame.cget("bg"))
        MsBbtn1.config(style="BW.TButton")
    if button2!="":
        MsBbtn2 = ttk.Button(master=MsB, text=button2, command=btn2IsPushed)
        MsBbtn2.place(x=160, y=155)
        style = ttk.Style()
        style.configure("BW.TButton", background=colorFrame.cget("bg"))
        MsBbtn2.config(style="BW.TButton")
    if button3!="":
        MsBbtn3 = ttk.Button(master=MsB, text=button3, command=btn3IsPushed)
        MsBbtn3.place(x=315, y=155)
        style = ttk.Style()
        style.configure("BW.TButton", background=colorFrame.cget("bg"))
        MsBbtn3.config(style="BW.TButton")

    TKFONT = font.nametofont("TkDefaultFont")

    MsBtext = ttk.Label(MsB, text=text, font=(TKFONT, 10))
    MsBtext.place(x=100, y=60)

    if platform.system() == "Windows":
        WindowIcon = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons', 'transparent.ico')
        MsB.iconbitmap(WindowIcon)
    MsB.title(Title)
    MsB.geometry("400x200")
    MsB.resizable(False, False)
    MsB.transient(master)
    MsB.grab_set()
    MsB.wait_window(MsB)
    return button_pressed

root = tkinter.Tk()

ShowMSBox(root, Icon="Information", Title="Test Message Box", text="This is a test message.")

root.destroy()