from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import sqlite3

"""SQL SELECTS - WRITING DATA TO PYTHON VARIABLES"""
elevations = []
elevations_floors = {}
blocks = []
blocks_numbers = {}
floors = []
floors_numbers = {}
con = sqlite3.connect('dxf.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM dxf")
    rows = cur.fetchall()
    for elev in rows:
        if elev[2] not in elevations:
            elevations.append(elev[2])


for elevation in elevations:
    floors = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM dxf where elevation=?"
        cur.execute(query, (elevation,))
        rows = cur.fetchall()
        for row in rows:
            if row[3] not in floors:
                floors.append(row[3])
    elevations_floors[elevation] = floors



with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM dxf")
    rows = cur.fetchall()
    for block in rows:
        if block[1] not in blocks:
            blocks.append(block[1])

for block in blocks:
    count = 0
    with con:
        cur = con.cursor()
        query = "SELECT * FROM dxf where name=?"
        cur.execute(query, (block,))
        rows = cur.fetchall()
        for row in rows:
            count +=1
    blocks_numbers[block] = count

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM dxf")
    rows = cur.fetchall()
    for floor in rows:
        if floor[3] not in floors:
            floors.append(floor[3])

for floor in floors:
    count = 0
    with con:
        cur = con.cursor()
        query = "SELECT * FROM dxf where level=?"
        cur.execute(query, (floor,))
        rows = cur.fetchall()
        for row in rows:
            count +=1
    floors_numbers[floor] = count

test_mode = True
if test_mode == True:
    print(blocks)
    print(blocks_numbers)
    print("*" * 40)
    print(elevations)
    print(elevations_floors)
    print("*" * 40)
    print(floors)
    print(floors_numbers)

"""TKINTER - RAPORT FROM THE DATABASE"""

root = Tk()
root.iconbitmap('icon.ico')
root.title('DXF Files Elevation Engine Raport')

myLabel1 = Label(root, text="YOUR STATUS RAPORT:", anchor="w",justify=LEFT, font="-weight bold")
myLabel1.grid(row=0, column=0)
status_frame = Frame(root, relief='sunken', bd=1)
status_frame.grid(row=0, column=1, sticky=W+E+N+S)

root.mainloop()