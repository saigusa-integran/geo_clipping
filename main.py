#------------------import packages------------------------
import numpy as np
import pandas as pd
import os
import shapely
import fiona
import geopandas as gpd
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import geoalchemy2 as gal
import sqlalchemy as sal
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from secret import engine_int

#------------------Start postgres engine-----------------------------
engine = sal.create_engine(engine_int)

#------------------GUI part start------------------------
##  Variables-----
#Create instance
root = tk.Tk()
#Add title
root.title("Area Clipper")
#Define the area
root.geometry("300x600")
#Adding a Label
ttk.Label(root, text="Select area types to clip.").pack(pady=5)


##--------Global variable--------------------
# type = ['LGA','SA2']
# type_op = tk.StringVar()
# type_chosen = ttk.Combobox(root, width=12, textvariable=type_op)
# type_chosen['values'] = type
# type_chosen.current(0)
# type_chosen.pack(pady=5)
# type_out = type_chosen.get()


##--------Variables for LGA clip----------------------
#Listings for LGA option
sql_select = 'SELECT LOWER("ABBREV_NAME") abbrev, geom FROM boundaries.lga_20_08'
listings_lga = gpd.GeoDataFrame.from_postgis(sql_select, engine, geom_col='geom')

#Options to select
options = listings_lga['abbrev'].tolist()


##--------Variables for SA2 clip----------------------
#Listings for LGA option
sa2_region_option = ['Greater Brisbane', 'Rest of Qld']

##Variables for extension
extension = ['shp','gpkg']
driver = ['MapInfo File','GPKG']


##------------LGA Clip Class----------------------
class Clip:
    """This is  a class to clip the LGA area"""

# ---LGA part-----
    def lga_selected(self, event):
        self.LGA_select = self.chosen.get()
        ttk.Label(root, text="Select extension.").pack()
        self.ext_sel = tk.StringVar()
        self.ext_sel.set(extension[0])
        self.ext_chosen = ttk.Combobox(root, width=12, textvariable=self.ext_sel)
        self.ext_chosen['values'] = extension
        self.ext_chosen.current(0)
        self.ext_chosen.bind("<<ComboboxSelected>>", self.ext_selected)
        self.ext_chosen.pack(pady=5)


    def ext_selected(self, event):
        self.ext_out = self.ext_chosen.get()
        # 3 Execute --> pass input variables to to_file script
        self.exc_text = tk.StringVar()
        self.exc_btn = ttk.Button(root, textvariable=self.exc_text, command=lambda: self.query())
        self.exc_text.set("Execute Clipping")
        self.exc_btn.pack(pady=5)


#---sa2 part------
    def sa_region_selected(self, event):
        self.sa2_region_select = self.chosen.get()
        self.sql_sa2_select = f"""SELECT * FROM (SELECT LOWER(sa2_name11) AS name, gcc_name11 as area, shape as geom FROM """ \
                              f"""boundaries.sa2_19_10) AS sa2 WHERE sa2.area = '{self.sa2_region_select}' ORDER BY name ASC"""
        self.listings_sa2 = gpd.GeoDataFrame.from_postgis(self.sql_sa2_select, engine, geom_col='geom')
        # Regional options to select
        self.sa2_options = self.listings_sa2['name'].tolist()
        # Area
        self.op2 = tk.StringVar()
        self.sa2_chosen = ttk.Combobox(root, width=30, textvariable=self.op2)
        self.sa2_chosen['values'] = self.sa2_options
        self.sa2_chosen.current(0)
        self.sa2_chosen.bind("<<ComboboxSelected>>", self.sa_area_selected)
        self.sa2_chosen.pack(pady=5)

    def sa_area_selected(self, event):
        self.sa2_area_select = self.sa2_chosen.get()
        ttk.Label(root, text="Select extension.").pack()
        self.ext_sel = tk.StringVar()
        self.ext_sel.set(extension[0])
        self.ext_chosen = ttk.Combobox(root, width=12, textvariable=self.ext_sel)
        self.ext_chosen['values'] = extension
        self.ext_chosen.current(0)
        self.ext_chosen.bind("<<ComboboxSelected>>", self.ext_selected)
        self.ext_chosen.pack(pady=5)


    def __init__(self, root):
        # 1. GUI combobox start
        self.type = ['LGA', 'SA2']
        self.type_op = tk.StringVar()
        self.type_chosen = ttk.Combobox(root, width=12, textvariable=self.type_op)
        self.type_chosen['values'] = self.type
        self.type_chosen.current(0)
        self.type_chosen.bind("<<ComboboxSelected>>", self.second)
        self.type_chosen.pack(pady=5)

    def second(self, type_out):
        # 2. Choose LGA or SA
        self.type_out = self.type_chosen.get()
        ttk.Label(root, text="Select Area to be clipped.").pack(pady=5)
        self.op = tk.StringVar()
        self.chosen = ttk.Combobox(root, width=30, textvariable=self.op)
        if self.type_out == 'LGA':
            self.chosen['values'] = options
            self.chosen.current(0)
            self.chosen.bind("<<ComboboxSelected>>", self.lga_selected)
            self.chosen.pack(pady=5)

        elif self.type_out == 'SA2':
            self.chosen['values'] = sa2_region_option
            self.chosen.current(0)
            self.chosen.bind("<<ComboboxSelected>>", self.sa_region_selected)
            self.chosen.pack(pady=5)


    def query(self):
        # Saving file function
        self.exc_text.set("Finished.")

        if self.type_out == 'LGA':
            self.sql_cut = f"""SELECT dc.* FROM dcdb.qld_dcdb_21_07 dc, (SELECT LOWER("ABBREV_NAME") AS abbrev, LOWER("LGA") AS lga,geom """ \
                       f"""FROM boundaries.lga_20_08) AS lga WHERE lga.abbrev = '{self.LGA_select}' AND ST_Within(dc.o_shape, lga.geom)"""
        elif self.type_out == 'SA2':
            self.sql_cut = f"""SELECT dc.* FROM dcdb.qld_dcdb_21_07 dc, (SELECT LOWER(sa2_name11) AS name, gcc_name11 as region, shape as geom FROM boundaries.sa2_19_10) AS sa2 """ \
                           f"""WHERE sa2.region = '{self.sa2_region_select}' AND sa2.name = '{self.sa2_area_select}' AND ST_Within(dc.o_shape, ST_Transform(geom, 4283))"""

        self.listings = gpd.GeoDataFrame.from_postgis(self.sql_cut, engine, geom_col='o_shape')

        if self.ext_out == 'shp':
            if self.type_out == 'LGA':
                self.listings.to_file(f"output/{self.LGA_select}.shp")
            elif self.type_out == 'SA2':
                self.listings.to_file(f"output/{self.sa2_area_select}.shp")
        # elif self.ext_out == 'tab':
        #     self.listings.to_file(f"output/{self.LGA_select}.tab", driver=driver[0])
        elif self.ext_out == 'gpkg':
            if self.type_out == 'LGA':
                self.self.listings.to_file(f"output/{self.LGA_select}.gpkg", driver=driver[1])
            elif self.type_out == 'SA2':
                self.listings.to_file(f"output/{self.sa2_area_select}.gpkg", driver=driver[1])

        fig, ax = plt.subplots(figsize=(12, 8))
        self.listings.plot(ax=ax)
        plt.axis('equal')
        ax.set_axis_off()
        plt.show()




tt = Clip(root)
root.mainloop()