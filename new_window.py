from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import ttk
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

"""TKINTER - MAKE MENU FOR ENTRIES"""
def make_menu(w):
    global the_menu
    the_menu = Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")


def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

"""TKINTER - RAPORT FROM THE DATABASE"""





root = Tk()
root.iconbitmap('icon.ico')
root.title('DXF Files Elevation Engine Raport')
make_menu(root)


"""TKINTER VARS TO DROPDOWN MENUS"""
blocks_var = StringVar()
elev_var = StringVar()
floor_var = StringVar()
blocks_var.set(list(blocks_numbers.keys())[0])
elev_var.set(list(elevations_floors.keys())[0])
floor_var.set(list(floors_numbers.keys())[0])

status_frame = Frame(root, relief='sunken', bd=1)
ee1 = Entry(status_frame)
ee2 = Entry(status_frame)
ee3 = Entry(status_frame)

def show_blocks(*args):
    ee1.delete(0, END)
    insertion = blocks_numbers[blocks_var.get()]
    ee1.insert(0, insertion )

def show_elev(*args):
    ee2.delete(0, END)
    count = 0
    for _ in elevations_floors[elev_var.get()]:
        count +=1
    insertion = count
    ee2.insert(0, insertion )

def show_floor(*args):
    ee3.delete(0, END)
    insertion = floors_numbers[floor_var.get()]
    ee3.insert(0, insertion )


myLabel1 = Label(root, text="YOUR STATUS RAPORT:", anchor="w",justify=CENTER, font="-weight bold")
myLabel1.grid(row=0, column=0, columnspan=10)

status_frame.grid(row=1, column=0, rowspan=5, columnspan=5, sticky=W+E+N+S)
statusLabel1 = Label(status_frame, text="Blocks:", anchor="w",justify=LEFT)
statusLabel1.grid(row=0, column=0, sticky=W)
statusLabel2 = Label(status_frame, text="Elevations:", anchor="w",justify=LEFT)
statusLabel2.grid(row=1, column=0, sticky=W)
statusLabel3 = Label(status_frame, text="Floors:", anchor="w",justify=LEFT)
statusLabel3.grid(row=2, column=0,  sticky=W)
separetor1 = ttk.Separator(status_frame, orient=VERTICAL)
separetor1.grid(column=1, row=0, rowspan=3, sticky='ns')
BlocksDrop = OptionMenu(status_frame, blocks_var, *blocks_numbers.keys(), command=show_blocks)
BlocksDrop.grid(row=0, column=2, sticky=W+E+N+S, padx=0)
ElevationDrop = OptionMenu(status_frame, elev_var, *elevations_floors.keys(), command=show_elev)
ElevationDrop.grid(row=1, column=2, sticky=W+E+N+S, padx=0)
FloorsDrop = OptionMenu(status_frame, floor_var, *floors_numbers.keys(), command=show_floor)
FloorsDrop.grid(row=2, column=2, sticky=W+E+N+S, padx=0)
separetor2 = ttk.Separator(status_frame, orient=VERTICAL)
separetor2.grid(column=3, row=0, rowspan=3, sticky='ns')
statusLabel4 = Label(status_frame, text=f"Number of {blocks_var.get()} occurrences:", anchor="w",justify=LEFT)
statusLabel4.grid(row=0, column=4, sticky=W)
statusLabel5 = Label(status_frame, text=f"Floors of {elev_var.get()}:", anchor="w",justify=LEFT)
statusLabel5.grid(row=1, column=4, sticky=W)
statusLabel6 = Label(status_frame, text=f"Number of {floor_var.get()} occurrences:  ", anchor="w",justify=LEFT)
statusLabel6.grid(row=2, column=4,  sticky=W)
separetor3 = ttk.Separator(status_frame, orient=VERTICAL)
separetor3.grid(column=5, row=0, rowspan=5, sticky='ns')

ee1.grid(row=0, column=6)
ee2.grid(row=1, column=6)
ee3.grid(row=2, column=6)
ee1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
ee2.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
ee3.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

"""FUNCTIONS"""


show_floor()
show_elev()
show_blocks()
root.mainloop()