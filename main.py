#------------------import packages------------------------
import numpy as np
import pandas as pd
import os
import shapely
import fiona
import geopandas as gpd
import tkinter as tk
from tkinter import ttk
import geoalchemy2 as gal
import sqlalchemy as sal
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from secret import engine_int

#------------------Start postgres engine-----------------------------
engine = sal.create_engine(engine_int)
#------------------GUI part start------------------------
#Create instance
root = tk.Tk()
#Add title
root.title("Area Clipper")
#Define the area
root.geometry("300x200")
#Adding a Label
ttk.Label(root, text="Select a LGA.").pack(pady=10)

#Listings for LGA option

sql_select = 'SELECT LOWER("ABBREV_NAME") abbrev, geom FROM boundaries.lga_20_08'
listings_lga = gpd.GeoDataFrame.from_postgis(sql_select, engine, geom_col='geom')


#--- Option menu ver
def selected(event):
    myLabel = clicked.get()
    sql_cut = f"""SELECT dc.* FROM dcdb.qld_dcdb_20_07 dc, (SELECT LOWER("ABBREV_NAME") AS abbrev, LOWER("LGA") AS lga,geom """ \
              f"""FROM boundaries.lga_20_08) AS lga WHERE lga.abbrev = '{myLabel}' AND ST_Within(dc.o_shape, lga.geom)"""
    listings = gpd.GeoDataFrame.from_postgis(sql_cut, engine, geom_col='o_shape')
    #listings.to_file(f"DCDB_{myLabel}.shp")
    fig, ax = plt.subplots(figsize=(12, 8))
    listings.plot(ax=ax)
    plt.axis('equal')
    ax.set_axis_off()
    plt.show()

options = listings_lga['abbrev'].tolist()

clicked = tk.StringVar()
clicked.set(options[0])

# drop = tk.OptionMenu(root, clicked, *options, command=selected)
# drop.pack(pady=20)


op = tk.StringVar()
lga_chosen = ttk.Combobox(root, width=12, textvariable=op)
lga_chosen['values'] = options
lga_chosen.current(0)
lga_chosen.bind("<<ComboboxSelected>>", selected)
lga_chosen.pack(pady=20)


root.mainloop()
#------------------GUI part end--------------------------
