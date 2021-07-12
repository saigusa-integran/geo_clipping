#------------------import packages------------------------
import numpy as np
import pandas as pd
import os
import shapely
import fiona
import geopandas as gpd
import tkinter as tk
import geoalchemy2 as gal
import sqlalchemy as sal
import matplotlib.pyplot as plts
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

#------------------variables-----------------------------

#------------------GUI part start------------------------
root = tk.Tk()
root.title =('Area Clipper')

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('clip_image.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
inst = tk.Label(root, text="Select the clipping area from the list", font="Raleway")
inst.grid(columnspan=3, column=0, row=1)

def selected(event):
    myLabel = clicked.get()
    print(myLabel)

options = [1,2,3,4,5,67]

clicked = tk.StringVar()
clicked.set(options[0])

drop = tk.OptionMenu(root, clicked, *options, command=selected)
drop.grid(column=1, row=2)

# ----practice PDF----
# def open_file():
#     browse_text.set("loading...")
#     file = askopenfile(parent=root, mode='rb', title="Choose a file", filetype=[("Pdf file, "*.pdf)])
#     if file:
#         print("file was successfully loaded")

# #Browse button
# browse_text = tk.StringVar()
# browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
# browse_text.set("Browse")
# browse_btn.grid(column=1, row=2)

# ----prac pdf end-----

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)


root.mainloop()



#------------------GUI part end--------------------------
