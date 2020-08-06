from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import time
import math
from tkinter import messagebox
import dxfgrabber
from operator import itemgetter
import sqlite3
import os
""" multi
line
comment"""


__version__ = 0.9

current_state = None
previous_state = None
cached_num = None
f_num = None
ready_to_math = False
ready_to_equal = False
history = ""
path_save = ""
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None



    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def unbind(self):
        self.widget.unbind("<Enter>")
        self.widget.unbind("<Leave>")
        self.widget.unbind("<ButtonPress>")

    def rebind(self):
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)



def make_menu(w):
    global the_menu
    the_menu = Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


root = Tk()
root.iconbitmap('icon.ico')
root.title('DXF Files Elevation Engine')
make_menu(root)


first_text_value = ["Enter-any-value"]
second_text_value = ["Enter-any-value"]
file_path = ""
history_elev=""
history_floor=""
entry3_allowed = False
entry4_allowed = False
entry5_allowed = False


clicked = StringVar()
clicked2 = StringVar()
clicked.set(first_text_value[0])
clicked2.set(second_text_value[0])


def shift_up(*args):
    text_pre = e1.get()
    e1.delete(0, END)
    e1.insert(0, text_pre.upper())

def shift_down(*args):
    text_pre = e1.get()
    e1.delete(0, END)
    e1.insert(0, text_pre.lower())

def shift_right(*args):
    text_pre = e1.get()
    e1.delete(0, END)
    result = ""
    for letter in text_pre:
        result += letter.swapcase()
    e1.insert(0, result)

def shift_left(*args):
    text_pre = e1.get()
    result = ""
    for letter in reversed(text_pre):
        result += letter
    e1.delete(0, END)
    e1.insert(0, result)

def upper_key_elev(*args):
    global history_elev
    if history_elev != "":
        e1.delete(0, END)
        e1.insert(0, history_elev)

def upper_key_floor(*args):
    global history_floor
    if history_floor != "":
        e2.delete(0, END)
        e2.insert(0, history_floor)

def button_add():
    global file_path
    global status_path
    file = askopenfilename(filetypes=[("DXF files", "*.dxf")])
    file_path = file
    if file_path != "":
        messagebox.showinfo("File path added successfully", "File path added successfully")
        button_add["state"] = "disabled"
        filemenu.entryconfig(0, state="disabled")
        status_path.grid_forget()
        status_path = Label(status_frame, text="Ready to load!", fg="dark orange", anchor="center")
        status_path.grid(row=5, column=0, sticky=W+E+N+S)
    else:
        messagebox.showwarning("You must add your DXF file!", "You must add your DXF file!")


def entry5_not_allowed(action_code):
    global entry5_allowed
    if action_code == '0':
        return True
    else:
        if entry5_allowed == True:
            entry5_allowed = False
            return True
        else:
            return False


def cancel1():
    global first_text_value
    global ElevDrop
    global status_elev
    if first_text_value == ["Enter-any-value"]:
        messagebox.showwarning("Enter any data in order to remove it", "You must enter any data to your list"
                                                                       " before you can remove it.")
    else:
        remove = clicked.get()
        first_text_value.remove(remove)
        if first_text_value == []:
            first_text_value = ["Enter-any-value"]
            status_elev.grid_forget()
            status_elev = Label(status_frame, text="Waiting to enter data", anchor="w", justify=CENTER, fg="dark orange")
            status_elev.grid(row=1, column=0, sticky=W + E)
        ElevDrop.grid_forget()
        ElevDrop = OptionMenu(root, clicked, *first_text_value)
        ElevDrop.grid(row=1, column=1, sticky=W + E + N + S, padx=0)
        clicked.set(first_text_value[0])

def cancel2():
    global second_text_value
    global FlorDrop
    global status_floor
    if second_text_value == ["Enter-any-value"]:
        messagebox.showwarning("Enter any data in order to remove it", "You must enter any data to your list"
                                                                       " before you can remove it.")
    else:
        remove = clicked2.get()
        second_text_value.remove(remove)
        if second_text_value == []:
            second_text_value = ["Enter-any-value"]
            status_floor.grid_forget()
            status_floor = Label(status_frame, text="Waiting to enter data", anchor="w", justify=CENTER, fg="dark orange")
            status_floor.grid(row=3, column=0, sticky=W+E)
        FlorDrop.grid_forget()
        FlorDrop = OptionMenu(root, clicked2, *second_text_value)
        FlorDrop.grid(row=4, column=1, sticky=W+E+N+S, padx=0)
        clicked2.set(second_text_value[0])


def cancel3():
    global file_path
    global status_path
    if file_path == "":
        messagebox.showwarning("Add your file!", "You must add your DXF file "
                                                                       " before you can remove it.")
    else:
        file_path = ""
        button_add["state"] = "normal"
        filemenu.entryconfig(0, state="normal")
        status_path.grid_forget()
        status_path = Label(status_frame, text="Waiting to enter data", fg="dark orange", anchor="w", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)

def button_add_elev(*args):
    global history_elev
    global first_text_value
    global ElevDrop
    global clicked
    global status_elev
    add_elevation = e1.get()
    good_to_go = False
    if add_elevation != "":
        for char in add_elevation:
            if char.isalnum():
                good_to_go = True
    if good_to_go ==False:
        messagebox.showwarning("Incorrect text value!", "Your text value must be at least 1 character long string with"
                                                        "one alphanumerical character ")
    elif first_text_value == ["Enter-any-value"] and good_to_go==True:
        first_text_value = []
        first_text_value.append(add_elevation)
        clicked.set(first_text_value[0])
        ElevDrop.grid_forget()
        ElevDrop = OptionMenu(root, clicked, *first_text_value)
        ElevDrop.grid(row=1, column=1, sticky=W + E)
        status_elev.grid_forget()
        status_elev = Label(status_frame, text="Ready to load!", anchor="center", fg="dark orange", justify=CENTER)
        status_elev.grid(row=1, column=0, sticky=W + E)
        history_elev = add_elevation
        e1.delete(0, END)
        messagebox.showinfo("Added first text value successfully", f"Added *{add_elevation}* successfully. You can add more than one value")
    elif first_text_value != ["Enter-any-value"] and good_to_go == True:
        first_text_value.append(add_elevation)
        ElevDrop.grid_forget()
        ElevDrop = OptionMenu(root, clicked, *first_text_value)
        ElevDrop.grid(row=1, column=1, sticky=W + E)
        history_elev = add_elevation
        e1.delete(0, END)
        messagebox.showinfo("Added first text value successfully",f"Added {add_elevation} successfully. You can add more values")


def button_add_floor(*args):
    global history_floor
    global second_text_value
    global FlorDrop
    global clicked2
    global status_floor

    add_floor = e2.get()
    good_to_go = False
    if add_floor != "":
        for char in add_floor:
            if char.isalnum():
               good_to_go = True
    if good_to_go == False:
        messagebox.showwarning("Incorrect text value!", "Your text value must be at least 1 character long string with"
                                                        "one alphanumerical character ")
    elif second_text_value == ["Enter-any-value"] and good_to_go == True:
        second_text_value = []
        second_text_value.append(add_floor)
        clicked2.set(second_text_value[0])
        FlorDrop.grid_forget()
        FlorDrop = OptionMenu(root, clicked2, *second_text_value)
        FlorDrop.grid(row=4, column=1, sticky=W + E)
        status_floor.grid_forget()
        status_floor = Label(status_frame, text="Ready to load!", anchor="center", fg="dark orange", justify=CENTER)
        status_floor.grid(row=3, column=0, sticky=W+E)
        history_floor = add_floor
        e2.delete(0, END)
        messagebox.showinfo("Added second text value successfully",
                            f"Added *{add_floor}* successfully. You can add more than one value")
    elif second_text_value != ["Enter-any-value"] and good_to_go == True:
        second_text_value.append(add_floor)
        FlorDrop.grid_forget()
        FlorDrop = OptionMenu(root, clicked2, *second_text_value)
        FlorDrop.grid(row=4, column=1, sticky=W + E)
        history_floor = add_floor
        e2.delete(0, END)
        messagebox.showinfo("Added second text value successfully",
                            f"Added {add_floor} successfully. You can add more values")

def button_go():
    global first_text_value
    global second_text_value
    global file_path
    global entry5_allowed
    global status_path
    global status_elev
    global status_floor
    global status_head

    if file_path != "":
        entry5_allowed = True
        e5.delete(0, END)
        e5.insert(0, str(file_path))
        entry5_allowed = False
        status_path.grid_forget()
        status_path = Label(status_frame, text="File loaded!", fg="green", anchor="center", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)
    else:
        status_path.grid_forget()
        status_path = Label(status_frame, text="Failed to load!", fg="red", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)
    if first_text_value != ["Enter-any-value"]:
        status_elev.grid_forget()
        status_elev = Label(status_frame, text="Elevation loaded!", anchor="center", fg="green", justify=CENTER)
        status_elev.grid(row=1, column=0, sticky=W + E)
    else:
        status_elev.grid_forget()
        status_elev = Label(status_frame, text="Failed to load!", anchor="center", fg="red", justify=CENTER)
        status_elev.grid(row=1, column=0, sticky=W + E)
    if second_text_value != ["Enter-any-value"]:
        status_floor.grid_forget()
        status_floor = Label(status_frame, text="Floors loaded!", anchor="center", fg="green", justify=CENTER)
        status_floor.grid(row=3, column=0, sticky=W + E)
    else:
        status_floor.grid_forget()
        status_floor = Label(status_frame, text="Failed to load!", anchor="center", fg="red", justify=CENTER)
        status_floor.grid(row=3, column=0, sticky=W + E)

    if first_text_value != ["Enter-any-value"] and second_text_value != ["Enter-any-value"] and file_path != "":
        button_start["state"] = "normal"
        status_head.grid_forget()
        status_head = Label(root, text="All data loaded!", fg="green", anchor="center", justify=CENTER, borderwidth=1, relief='sunken')
        status_head.grid(row=7, column=2, columnspan=2, sticky=W+E+N+S)
        button_go["state"] = "disabled"
        button_cancel1["state"] = "disabled"
        button_cancel2["state"] = "disabled"
        button_cancel3["state"] = "disabled"
def button_start():
    global file_path
    global first_text_value
    global second_text_value
    start = time.time()
    path = file_path


    if os.path.isfile('./dxf.db') == True:
        os.remove('./dxf.db')

    connection = sqlite3.connect("dxf.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS dxf
    (id INTEGER PRIMARY KEY,
    name text,
    elevation text,
    level text)""")
    connection.commit()
    connection.close()

    path = file_path

    def distance(a, b, c, d):
        return int(math.sqrt((a - c) ** 2 + (b - d) ** 2))

    def bracket_remouver(text_data):
        temp_text_data = text_data.replace("{", "").replace("}", "")
        return temp_text_data

    def distance_checker(a, b):
        #print(f"{a} {b}")
        Y_origin = (a['Y2'] - a['Y1']) / 2 + a['Y1']
        result = False
        if b['X1'] <= a['X2'] <= b['X2'] and b['Y1'] <= Y_origin <= b['Y2']:
            result = True
        if b['X1'] <= a['X2'] <= b['X2'] and b['Y1'] <= a['Y1'] <= b['Y2']:
            result = True
        if b['X1'] <= a['X2'] <= b['X2'] and b['Y1'] <= a['Y2'] <= b['Y2']:
            result = True
        Y_origin = (b['Y2'] - b['Y1']) / 2 + b['Y1']
        if a['X1'] <= b['X1'] <= a['X2'] and a['Y1'] <= Y_origin <= a['Y2']:
            result = True
        if a['X1'] <= b['X1'] <= a['X2'] and a['Y1'] <= b['Y1'] <= a['Y2']:
            result = True
        if a['X1'] <= b['X1'] <= a['X2'] and a['Y1'] <= b['Y2'] <= a['Y2']:
            result = True
        return result

    def module_size(temp_size):
        '''calculation the sizes of the frame when the frame has the insert point
        in bottom left corner, the main frame must be created by POLYLINE'''
        temp_data_size = []
        if int(temp_size[0][0]) < int(temp_size[2][0]) and int(temp_size[0][1]) < int(temp_size[2][1]):
            temp_data_size.append("BL")  # Bottom Left corner as a insert point of a frame
        if int(temp_size[0][0]) > int(temp_size[2][0]) and int(temp_size[0][1]) < int(temp_size[2][1]):
            temp_data_size.append("BR")  # Bottom Right corner as a insert point of a frame
        if int(temp_size[0][0]) > int(temp_size[2][0]) and int(temp_size[0][1]) > int(temp_size[2][1]):
            temp_data_size.append("TR")  # Top Right corner as a insert point of a frame
        if int(temp_size[0][0]) < int(temp_size[2][0]) and int(temp_size[0][1]) > int(temp_size[2][1]):
            temp_data_size.append("TL")  # Top Left corner as a insert point of a frame
        calc_data = int(abs(temp_size[0][0] - temp_size[2][0]))
        temp_data_size.append(calc_data)
        calc_data = int(abs(temp_size[0][1] - temp_size[2][1]))
        temp_data_size.append(calc_data)
        return temp_data_size

    def central_point(name, X_temp_size, Y_temp_size):
        '''calculation the sizes of the frame when the frame has the insert point
        in bottom left corner, the main frame must be created by POLYLINE'''
        if temp_code_W_H[name][0] == "BL":
            temp_data_size = []
            temp_data_size.append(int(X_temp_size + temp_code_W_H[name][1] / 2))
            temp_data_size.append(int(Y_temp_size + temp_code_W_H[name][2] / 2))
        if temp_code_W_H[name][0] == "BR":
            temp_data_size = []
            temp_data_size.append(int(X_temp_size - temp_code_W_H[name][1] / 2))
            temp_data_size.append(int(Y_temp_size + temp_code_W_H[name][2] / 2))
        if temp_code_W_H[name][0] == "TL":
            temp_data_size = []
            temp_data_size.append(int(X_temp_size + temp_code_W_H[name][1] / 2))
            temp_data_size.append(int(Y_temp_size - temp_code_W_H[name][2] / 2))
        if temp_code_W_H[name][0] == "TR":
            temp_data_size = []
            temp_data_size.append(int(X_temp_size - temp_code_W_H[name][1] / 2))
            temp_data_size.append(int(Y_temp_size - temp_code_W_H[name][2] / 2))
        return temp_data_size

    def calculate_radius(name):
        W = temp_code_W_H[name][1]
        H = temp_code_W_H[name][2]
        return int(math.sqrt((W) ** 2 + (H) ** 2) / 2)

    dxf = dxfgrabber.readfile(path)
    temp_code_W_H_total = []

    '''calculation the main size (width x height; WxH) of the frame'''
    temp_code_W_H = {}

    for blocks in dxf.blocks:
        if blocks.name:
            for elements in blocks:
                if elements.dxftype == "LWPOLYLINE":
                    temp_size_W_H = []
                    temp_size_W_H.append(module_size(elements.points)[0])
                    temp_size_W_H.append(module_size(elements.points)[1])
                    temp_size_W_H.append(module_size(elements.points)[2])
                    temp_code_W_H[blocks.name] = temp_size_W_H
    level_temp_data = {}  # dict of location the "level" text
    main_elevation_temp_data = []  # dict of location the "elevation" text
    list_module_coordinate = []
    ''' searching location the text referred to the levels and the elevation, '''
    for entity in dxf.entities:
        if entity.dxftype == "MTEXT":
            for el in first_text_value:
                if el in entity.raw_text:
                    elevation_temp_data = {}
                    elevation_temp_data['X'] = int(entity.insert[0])
                    elevation_temp_data['elev'] = bracket_remouver(entity.raw_text)
                    main_elevation_temp_data.append(elevation_temp_data)
            for el in second_text_value:
                if el in entity.raw_text and len(entity.raw_text) in range(2, 5):
                    level_temp_data[int(entity.insert[1])] = bracket_remouver(entity.raw_text)
    temp_global_list = []
    temp_local_list = ()
    radius = ''
    '''calculation the location of the middle point of the frames by analysisi insert point of them,
    preparing the temporary data about the "radius", the radius is a half of hypotenuse the frame'''
    temp_C_X = ''

    for entity in dxf.entities:
        if entity.dxftype == "INSERT":
            x_coordinate = int(entity.insert[0])
            y_coordinate = int(entity.insert[1])
            if type(entity.name) is str:
                dict_module_coordinate = {}
                dict_module_coordinate['name'] = entity.name
                W_frame = temp_code_W_H[entity.name][1]  # szerokość modułu
                H_frame = temp_code_W_H[entity.name][2]  # wysokość modułu
                radius = calculate_radius(entity.name)
                central_point_data = central_point(entity.name, x_coordinate, y_coordinate)
                dict_module_coordinate['C_X'] = central_point_data[0]  # C_X-calculation the middle point in horizontal direction - X-direction
                dict_module_coordinate['C_Y'] = central_point_data[1]  # C_Y-calculation the middle point in horizontal direction - Y-direction
                dict_module_coordinate['radius'] = radius
                temp_global_list.append(dict_module_coordinate)

    sorted_list = sorted(temp_global_list, key=itemgetter("C_X", "C_Y"))

    temp_C_X = ''
    temp_global_list = []
    final_temp_global_list = []
    group_list = {}
    Y_stop = ''
    name_stop = ''
    '''finding the neighbour' groups'''

    zip_list = list(zip(sorted_list, sorted_list[1:]))

    for i in zip_list:
        if not group_list:
            group_list['X_pattern'] = i[0]['C_X']
            group_list['Y_start'] = i[0]['C_Y']
            group_list['name_start'] = i[0]['name']
        radius_distance = calculate_radius(i[0]['name']) + calculate_radius(i[1]['name'])
        frame_distance = abs(i[0]['C_Y'] - i[1]['C_Y'])
        if i[0]['C_X'] == i[1]['C_X'] and frame_distance < radius_distance:
            group_list['Y_stop'] = i[1]['C_Y']
            group_list['name_stop'] = i[1]['name']
            group_list['X1'] = (group_list['X_pattern'] - calculate_radius(group_list['name_stop']))
            group_list['X2'] = (group_list['X_pattern'] + calculate_radius(group_list['name_stop']))
            group_list['Y1'] = (group_list['Y_start'] - calculate_radius(group_list['name_start']))
            group_list['Y2'] = (group_list['Y_stop'] + calculate_radius(group_list['name_stop']))
            group_list['elev'] = 0
        else:
            final_temp_global_list.append(group_list)
            group_list = {}
        if i == zip_list[-1]:
            final_temp_global_list.append(group_list)

    ##############################################
    '''finding the neighbours'''

    temp_A = []
    temp_C = []
    complex_temp_table = []

    for A, B in enumerate(final_temp_global_list):
        for C, D in enumerate(final_temp_global_list):
            status = distance_checker(B, D)
            if status and A != C:
                temp_A.append(A)
                temp_C.append(C)
                temp_table = []
                temp_table.append(A)
                temp_table.append(C)
                complex_temp_table.append(temp_table)

    ##############################################
    '''finding the borders between the neighbour' groups'''
    sorted_temp_A = sorted(set(temp_A))
    sorted_temp_C = sorted(set(temp_C))
    primary_temp_list = list(set(sorted_temp_A) - set(sorted_temp_C))
    ##############################################
    previous = complex_temp_table[0]
    secondary_temp_list = []
    zip_complex_temp_table = list(zip(complex_temp_table, complex_temp_table[1:]))

    for i in zip_complex_temp_table:
        if i[0][1] < i[1][0] < i[1][1]:
            secondary_temp_list.append(i[1][0])
            secondary_temp_list.append(i[1][1])
    result = sorted(set(primary_temp_list).intersection(secondary_temp_list))
    #############################################
    frame_elevation_level = []
    # '''sorting location of the "elevation" text'''
    sorted_main_elevation_temp_data = sorted(main_elevation_temp_data, key=itemgetter("X"), reverse=False)
    '''calculation the location'''
    elevation = 0
    for i, j in enumerate(final_temp_global_list):
        if i in result:
            elevation = elevation + 1
        j['elev'] = sorted_main_elevation_temp_data[elevation]['elev']
    ##############################################
    for i in sorted_list:
        for j in final_temp_global_list:
            if i['C_X'] == j['X_pattern'] and j['Y_start'] <= i['C_Y'] <= j['Y_stop']:
                i['elev'] = j['elev']
        temp_data = []
        temp_data = {abs(k - i['C_X']): v for k, v in level_temp_data.items()}
        temp_lambda = lambda temp_data: min(temp_data.items())
        i['level'] = temp_lambda(temp_data)[1]

    '''create a list of data: frame, elevation, level'''
    frame_elevation_level = list(map(itemgetter('name', 'elev', 'level'), sorted_list))
    # for i in frame_elevation_level:
    #     print(i)
    ##############################################
    con = sqlite3.connect('dxf.db')
    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO dxf (name, elevation, level) VALUES(?, ?, ?)", frame_elevation_level)
        con.commit()

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM dxf")
        rows = cur.fetchall()
        number_of_rows = 0
        for _ in rows:
            number_of_rows += 1

    end = time.time()
    messagebox.showinfo("Operation run successfully", f"Operation run successfully in {int(end-start)} seconds")
    messagebox.showinfo("Number of rows in DB", f"There are {number_of_rows} rows in your database")
    openNewWindow()

def openNewWindow():


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
                count += 1
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
            for _ in rows:
                count += 1
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

    newWindow = Toplevel(root)
    newWindow.title('DXF Files Elevation Engine Raport')
    make_menu(newWindow)

    """TKINTER VARS TO DROPDOWN MENUS"""
    blocks_var = StringVar()
    elev_var = StringVar()
    floor_var = StringVar()
    blocks_var.set(list(blocks_numbers.keys())[0])
    elev_var.set(list(elevations_floors.keys())[0])
    floor_var.set(list(floors_numbers.keys())[0])

    status_frame = Frame(newWindow, relief='sunken', bd=1)
    ee1 = Entry(status_frame)
    ee2 = Entry(status_frame)
    ee3 = Entry(status_frame)

    def show_blocks(*args):
        ee1.delete(0, END)
        insertion = blocks_numbers[blocks_var.get()]
        ee1.insert(0, insertion)
        statusLabel4["text"] = f"Number of {blocks_var.get()} occurrences:  "

    def show_elev(*args):
        ee2.delete(0, END)
        count = 0
        for _ in elevations_floors[elev_var.get()]:
            count += 1
        insertion = count
        ee2.insert(0, insertion)
        statusLabel5["text"] = f"Number of {elev_var.get()} occurrences:  "

    def show_floor(*args):
        ee3.delete(0, END)
        insertion = floors_numbers[floor_var.get()]
        ee3.insert(0, insertion)
        statusLabel6["text"] = f"Number of {floor_var.get()} occurrences:  "

    def save(*args):
        file1 = askopenfilename(filetypes=[("TXT files", "*.txt")])
        file_path1 = file1
        if file_path1 != "":
            messagebox.showinfo("Saving your report!", "File found. Saving your report!")
            f = open(file_path1, "a")
            f.write("Your report from DXF Files Elevation Engine \n")
            f.write(f"Number of blocks: {len(blocks)}  \n")
            f.write(f"Your blocks: {blocks} \n")
            f.write("Number of occurrences of each block: \n")
            for bl in blocks_numbers.keys():
                msg = " "
                msg+= str(bl)
                msg+= ": "
                msg+= str(blocks_numbers[bl])
                f.write(f"{msg} \n")
            f.close()
            messagebox.showinfo("Report saved!", f"Report saved in {file_path}")

        else:
            messagebox.showwarning("You must add your TXT file!", "You must add your TXT file"
                                                                  "to save the report!")


    myLabel1 = Label(newWindow, text="YOUR STATUS REPORT:", anchor="w", justify=CENTER, font="-weight bold")
    myLabel1.grid(row=0, column=0, columnspan=10)

    status_frame.grid(row=1, column=0, rowspan=5, columnspan=5, sticky=W + E + N + S)
    statusLabel1 = Label(status_frame, text="Blocks:", anchor="w", justify=LEFT)
    statusLabel1.grid(row=0, column=0, sticky=W)
    statusLabel2 = Label(status_frame, text="Elevations:", anchor="w", justify=LEFT)
    statusLabel2.grid(row=1, column=0, sticky=W)
    statusLabel3 = Label(status_frame, text="Floors:", anchor="w", justify=LEFT)
    statusLabel3.grid(row=2, column=0, sticky=W)
    separetor1 = ttk.Separator(status_frame, orient=VERTICAL)
    separetor1.grid(column=1, row=0, rowspan=3, sticky='ns')
    BlocksDrop = OptionMenu(status_frame, blocks_var, *blocks_numbers.keys(), command=show_blocks)
    BlocksDrop.grid(row=0, column=2, sticky=W + E + N + S, padx=0)
    ElevationDrop = OptionMenu(status_frame, elev_var, *elevations_floors.keys(), command=show_elev)
    ElevationDrop.grid(row=1, column=2, sticky=W + E + N + S, padx=0)
    FloorsDrop = OptionMenu(status_frame, floor_var, *floors_numbers.keys(), command=show_floor)
    FloorsDrop.grid(row=2, column=2, sticky=W + E + N + S, padx=0)
    separetor2 = ttk.Separator(status_frame, orient=VERTICAL)
    separetor2.grid(column=3, row=0, rowspan=3, sticky='ns')
    statusLabel4 = Label(status_frame, text=f"Number of {blocks_var.get()} occurrences:", anchor="w", justify=LEFT)
    statusLabel4.grid(row=0, column=4, sticky=W)
    statusLabel5 = Label(status_frame, text=f"Floors of {elev_var.get()}:", anchor="w", justify=LEFT)
    statusLabel5.grid(row=1, column=4, sticky=W)
    statusLabel6 = Label(status_frame, text=f"Number of {floor_var.get()} occurrences:  ", anchor="w", justify=LEFT)
    statusLabel6.grid(row=2, column=4, sticky=W)
    separetor3 = ttk.Separator(status_frame, orient=VERTICAL)
    separetor3.grid(column=5, row=0, rowspan=5, sticky='ns')

    ee1.grid(row=0, column=6)
    ee2.grid(row=1, column=6)
    ee3.grid(row=2, column=6)
    ee1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
    ee2.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
    ee3.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
    button_save = Button(newWindow, text='SAVE!', command=save)
    button_save.grid(row=6, column=0, columnspan=5, sticky=W + E)

    """FUNCTIONS"""

    show_floor()
    show_elev()
    show_blocks()

    menubar = Menu(newWindow)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="SAVE", state='disabled')
    filemenu.add_separator()
    filemenu.add_command(label="Exit All", command=newWindow.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Deactivate tips", state='normal')
    helpmenu.add_command(label="Activate tips", state='disabled')
    helpmenu.add_separator()
    helpmenu.add_command(label="Version", command=show_version)
    menubar.add_cascade(label="Help", menu=helpmenu)

    toolsmenu = Menu(menubar, tearoff=0)
    toolsmenu.add_command(label="Calculator")
    toolsmenu.add_command(label="CM/IN Converter")
    menubar.add_cascade(label="Tools", menu=toolsmenu)
    newWindow.config(menu=menubar)
    newWindow.bind("<Control-s>", save)


def calculator():
    calcWindow = Toplevel(root)
    calcWindow.title('Simple Calculator')
    calcWindow.iconbitmap(r'calc.ico')

    operation = Entry(calcWindow, width=35, borderwidth=5)
    operation.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    e = Entry(calcWindow, width=35, borderwidth=5)
    e.grid(row=1, column=0, columnspan=3, padx=10, pady=10)



    def button_float():
        current = e.get()
        if len(current) == 0:
            e.delete(0, END)
            e.insert(0, str(current))
        elif "." in current:
            e.delete(0, END)
            e.insert(0, str(current))
        else:
            e.delete(0, END)
            e.insert(0, str(current) + str("."))

    def button_click(number):
        global current_state
        global previous_state
        global ready_to_equal
        global ready_to_math
        previous_state = current_state

        current_state = 'click'

        if previous_state in ['add', 'sub', 'mul', 'div'] and ready_to_equal == False:
            ready_to_equal = True
            button_equal['state'] = 'normal'

        current = e.get()
        e.delete(0, END)
        e.insert(0, str(current) + str(number))

        if current_state == 'click':
            if ready_to_math == False:
                button_add['state'] = 'normal'
                button_subtract['state'] = 'normal'
                button_divide['state'] = 'normal'
                button_multiply['state'] = 'normal'
            button_clear['state'] = 'normal'

    def button_clear():
        global current_state
        global previous_state
        global ready_to_math
        global ready_to_equal
        global cached_num
        global f_num
        global history
        previous_state = current_state

        current_state = 'clear'

        e.delete(0, END)
        ready_to_equal = False
        ready_to_math = False
        cached_num = None
        f_num = None
        history = ""

        operation.delete(0, END)

        button_equal['state'] = 'disabled'
        button_add['state'] = 'disabled'
        button_subtract['state'] = 'disabled'
        button_divide['state'] = 'disabled'
        button_multiply['state'] = 'disabled'

    def button_add():
        global current_state
        global previous_state
        global ready_to_equal
        global ready_to_math

        if ready_to_equal == True:
            ready_to_equal = False
            button_equal['state'] = 'disabled'

        if ready_to_math == False:
            ready_to_math = True
            button_add['state'] = 'disabled'
            button_subtract['state'] = 'disabled'
            button_divide['state'] = 'disabled'
            button_multiply['state'] = 'disabled'

        previous_state = current_state

        current_state = 'add'

        first_number = e.get()
        global f_num
        global math
        math = 'addition'

        f_num = float(first_number)
        e.delete(0, END)

        global history
        if previous_state != 'equal':
            history += str(f_num) + " + "
            operation.delete(0, END)
            operation.insert(0, history)
        if previous_state == 'equal':
            history += " + "
            operation.delete(0, END)
            operation.insert(0, history)

    def button_subtract():
        global current_state
        global previous_state
        global ready_to_equal
        global ready_to_math

        if ready_to_equal == True:
            ready_to_equal = False
            button_equal['state'] = 'disabled'

        if ready_to_math == False:
            ready_to_math = True
            button_add['state'] = 'disabled'
            button_subtract['state'] = 'disabled'
            button_divide['state'] = 'disabled'
            button_multiply['state'] = 'disabled'

        previous_state = current_state

        current_state = 'sub'

        first_number = e.get()
        global f_num
        global math
        math = 'subtraction'

        f_num = float(first_number)
        e.delete(0, END)

        global history
        if previous_state != 'equal':
            history += str(f_num) + " - "
            operation.delete(0, END)
            operation.insert(0, history)
        if previous_state == 'equal':
            history += " - "
            operation.delete(0, END)
            operation.insert(0, history)

    def button_multiply():
        global current_state
        global previous_state
        global ready_to_equal
        global ready_to_math

        if ready_to_equal == True:
            ready_to_equal = False
            button_equal['state'] = 'disabled'

        if ready_to_math == False:
            ready_to_math = True
            button_add['state'] = 'disabled'
            button_subtract['state'] = 'disabled'
            button_divide['state'] = 'disabled'
            button_multiply['state'] = 'disabled'

        previous_state = current_state

        current_state = 'mul'

        first_number = e.get()
        global f_num
        global math
        math = 'multiplication'

        f_num = float(first_number)
        e.delete(0, END)

        global history
        if previous_state != 'equal':
            history += str(f_num) + " x "
            operation.delete(0, END)
            operation.insert(0, history)
        if previous_state == 'equal':
            history += " x "
            operation.delete(0, END)
            operation.insert(0, history)

    def button_divide():
        global current_state
        global previous_state
        global ready_to_equal
        global ready_to_math

        if ready_to_equal == True:
            ready_to_equal = False
            button_equal['state'] = 'disabled'

        if ready_to_math == False:
            ready_to_math = True
            button_add['state'] = 'disabled'
            button_subtract['state'] = 'disabled'
            button_divide['state'] = 'disabled'
            button_multiply['state'] = 'disabled'

        previous_state = current_state

        current_state = 'div'

        first_number = e.get()
        global f_num
        global math
        math = 'division'

        f_num = float(first_number)
        e.delete(0, END)

        global history
        if previous_state != 'equal':
            history += str(f_num) + " / "
            operation.delete(0, END)
            operation.insert(0, history)
        if previous_state == 'equal':
            history += " / "
            operation.delete(0, END)
            operation.insert(0, history)

    def button_equal():
        global current_state
        global previous_state
        global cached_num
        global f_num
        global ready_to_math
        global history

        ready_to_math = False
        button_add['state'] = 'normal'
        button_subtract['state'] = 'normal'
        button_divide['state'] = 'normal'
        button_multiply['state'] = 'normal'

        if current_state != 'equal':
            previous_state = current_state

            current_state = 'equal'

            second_number = e.get()
            cached_num = float(second_number)
            e.delete(0, END)

            if math == 'addition':
                history += str(second_number)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, f_num + float(second_number))
                f_num += float(second_number)
            elif math == 'subtraction':
                history += str(second_number)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) - float(second_number))
                f_num -= float(second_number)
            elif math == 'multiplication':
                history += str(second_number)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) * float(second_number))
                f_num *= float(second_number)
            elif math == 'division':
                history += str(second_number)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) / float(second_number))
                f_num /= float(second_number)



        elif current_state == 'equal':
            previous_state = current_state

            e.delete(0, END)

            if math == 'addition':
                history += " + " + str(cached_num)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, f_num + float(cached_num))
                f_num += float(cached_num)
            elif math == 'subtraction':
                history += " - " + str(cached_num)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) - float(cached_num))
                f_num -= float(cached_num)
            elif math == 'multiplication':
                history += " x " + str(cached_num)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) * float(cached_num))
                f_num *= float(cached_num)
            elif math == 'division':
                history += " / " + str(cached_num)
                operation.delete(0, END)
                operation.insert(0, history)
                e.insert(0, float(f_num) / float(cached_num))
                f_num /= float(cached_num)

    button_1 = Button(calcWindow, text='1', padx=40, pady=20, command=lambda: button_click(1))
    button_2 = Button(calcWindow, text='2', padx=40, pady=20, command=lambda: button_click(2))
    button_3 = Button(calcWindow, text='3', padx=40, pady=20, command=lambda: button_click(3))
    button_4 = Button(calcWindow, text='4', padx=40, pady=20, command=lambda: button_click(4))
    button_5 = Button(calcWindow, text='5', padx=40, pady=20, command=lambda: button_click(5))
    button_6 = Button(calcWindow, text='6', padx=40, pady=20, command=lambda: button_click(6))
    button_7 = Button(calcWindow, text='7', padx=40, pady=20, command=lambda: button_click(7))
    button_8 = Button(calcWindow, text='8', padx=40, pady=20, command=lambda: button_click(8))
    button_9 = Button(calcWindow, text='9', padx=40, pady=20, command=lambda: button_click(9))
    button_0 = Button(calcWindow, text='0', padx=40, pady=20, command=lambda: button_click(0))
    button_add = Button(calcWindow, text='+', padx=39, pady=20, command=button_add, state=DISABLED)
    button_equal = Button(calcWindow, text='=', padx=40, pady=20, command=button_equal, state=DISABLED)
    button_clear = Button(calcWindow, text='Clear', padx=79, pady=20, command=button_clear, state=DISABLED)

    button_subtract = Button(calcWindow, text='-', padx=41, pady=20, command=button_subtract, state=DISABLED)
    button_multiply = Button(calcWindow, text='x', padx=40, pady=20, command=button_multiply, state=DISABLED)
    button_divide = Button(calcWindow, text='/', padx=41, pady=20, command=button_divide, state=DISABLED)

    button_1.grid(row=4, column=0, )
    button_2.grid(row=4, column=1, )
    button_3.grid(row=4, column=2, )

    button_4.grid(row=3, column=0, )
    button_5.grid(row=3, column=1, )
    button_6.grid(row=3, column=2, )

    button_7.grid(row=2, column=0, )
    button_8.grid(row=2, column=1, )
    button_9.grid(row=2, column=2, )

    button_0.grid(row=5, column=0)
    button_float = Button(calcWindow, text='.', padx=40, pady=20, command=button_float)

    button_clear.grid(row=5, column=1, columnspan=2)
    button_add.grid(row=6, column=0)
    button_equal.grid(row=6, column=1)
    button_float.grid(row=6, column=2)

    button_subtract.grid(row=7, column=0)
    button_multiply.grid(row=7, column=1)
    button_divide.grid(row=7, column=2)

def cm_in_converter():
    import cm_in_converter






myLabel1 = Label(root, text="ENTER NAMES:", anchor="w",justify=LEFT, font="-weight bold")
e1 = Entry(root)
myLabel2 = Label(root, text="Enter second text value:", anchor="w",justify=LEFT)
e2 = Entry(root)
myLabel3 = Label(root, text="Add dxf file:", anchor="w",justify=LEFT)
button_add = Button(root, text='Add .dxf file', command=button_add)
myLabel4 = Label(root, text="YOUR NAMES:", anchor="w",justify=LEFT, font="-weight bold")
e3 = Entry(root)
myLabel5 = Label(root, text="Your second text values:", anchor="w",justify=LEFT)
e4 = Entry(root)
myLabel6 = Label(root, text="Path to your dxf file:", anchor="w",justify=LEFT)
e5 = Entry(root)

button_go = Button(root, text='LOAD!', command=button_go)
button_start = Button(root, text='START!', command=button_start, state='disabled')
button_cancel1 = Button(root, text='CANCEL', command=cancel1)
button_cancel2 = Button(root, text='CANCEL', command=cancel2)
button_cancel3 = Button(root, text='CANCEL', command=cancel3)

myLabel1.grid(row=0, column=0, sticky=W+E)
e1.grid(row=1, column=0)
e1.bind("<Return>", button_add_elev)
e1.bind("<Control-Up>", shift_up)
e1.bind("<Control-Down>", shift_down)
e1.bind("<Control-Right>", shift_right)
e1.bind("<Control-Left>", shift_left)
e1.bind("<Up>", upper_key_elev)
e1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
myLabel2.grid(row=3, column=0, sticky=W+E+N+S)
ElevDrop = OptionMenu(root, clicked, *first_text_value)
ElevDrop.grid(row=1, column=1, sticky=W+E+N+S, padx=0)
FlorDrop = OptionMenu(root, clicked2, *second_text_value)
FlorDrop.grid(row=4, column=1, sticky=W+E+N+S, padx=0)
button_add_elev = Button(root, text='Add first text values', command=button_add_elev)
button_add_elev.grid(row=2, column=0, columnspan=2, sticky=W+E, padx=2)
button_add_flor = Button(root, text='Add second text values', command=button_add_floor)
button_add_flor.grid(row=5, column=0, columnspan=2, sticky=W+E, padx=2)
e2.grid(row=4, column=0, sticky=W+E+N+S)
e2.bind("<Return>", button_add_floor)
e2.bind("<Up>", upper_key_floor)
e2.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
myLabel3.grid(row=6, column=0, sticky=W+E)
button_add.grid(row=7, column=0, sticky=W+E)

myLabel4.grid(row=0, column=1, sticky=W+E)
#e3.grid(row=1, column=1)
myLabel5.grid(row=3, column=1, sticky=W+E)
#e4.grid(row=3, column=1)
myLabel6.grid(row=6, column=1, sticky=W+E)
e5.grid(row=7, column=1)

button_go.grid(row=10, column=0, columnspan=4, sticky=W+E)
button_start.grid(row=11, column=0, columnspan=4, sticky=W+E)
cancel_label = Label(root, text="CANCEL SETTINGS:", anchor="w",justify=LEFT, font="-weight bold")
cancel_label.grid(row=0, column=3, sticky=W+E)
button_cancel1.grid(row=1, column=3, rowspan=2, sticky=W+E+N+S)
button_cancel2.grid(row=3, column=3, rowspan=2, sticky=W+E+N+S)
button_cancel3.grid(row=5, column=3, rowspan=2, sticky=W+E+N+S)
reg3= root.register(entry5_not_allowed)

e5.config(validate='key', validatecommand=(reg3, '%d'))


status_frame = Frame(root, relief='sunken', bd=1)
status_frame.grid(row=1, column=2, rowspan=6, sticky=W+E+N+S)
status_head = Label(root, text="Data not loaded!", fg="red", borderwidth=1, relief='ridge', justify=CENTER)
status_head.grid(row=7, column=2, columnspan=2, sticky=W+E+N+S)
status_info = Label(root, text="STATUS INFO:", font="-weight bold")
status_info.grid(row=0, column=2, sticky=W+E)
status_label1 = Label(status_frame, text="Elevation:", fg="dodger blue", justify=CENTER)
status_label1.grid(row=0, column=0, sticky=W+E+N+S, pady=4)
status_elev = Label(status_frame, text="Waiting to enter data", anchor="center", fg="dark orange", justify=CENTER)
status_elev.grid(row=1, column=0, sticky=W+E)
status_label2 = Label(status_frame, text="Floors:", fg="dodger blue", justify=CENTER)
status_label2.grid(row=2, column=0, sticky=W+E, pady=4)
status_floor = Label(status_frame, text="Waiting to enter data", anchor="center",fg="dark orange", justify=CENTER)
status_floor.grid(row=3, column=0, sticky=W+E)
status_label3 = Label(status_frame, text="Your DXF file:", fg="dodger blue", justify=CENTER)
status_label3.grid(row=4, column=0, sticky=W+E, pady=4)
status_path = Label(status_frame, text="Waiting to enter data", fg="dark orange", anchor="center", justify=CENTER)
status_path.grid(row=5, column=0, sticky=W+E+N+S)

e1_ttp = CreateToolTip(e1, "Enter name of your elevation here")
e2_ttp = CreateToolTip(e2, "Enter name of your floor here")


def help_off():
    helpmenu.entryconfig(0, state="disabled")
    helpmenu.entryconfig(1, state="normal")
    e1_ttp.unbind()
    e2_ttp.unbind()

def help_on():
    helpmenu.entryconfig(1, state="disabled")
    helpmenu.entryconfig(0, state="normal")
    e1_ttp.rebind()
    e2_ttp.rebind()

def button_add_menu(*args):
    global file_path
    global status_path
    file = askopenfilename(filetypes=[("DXF files", "*.dxf")])
    file_path = file
    if file_path != "":
        messagebox.showinfo("File path added successfully", "File path added successfully")
        button_add["state"] = "disabled"
        filemenu.entryconfig(0, state="disabled")
        status_path.grid_forget()
        status_path = Label(status_frame, text="Ready to load!", fg="dark orange", anchor="center")
        status_path.grid(row=5, column=0, sticky=W+E+N+S)
    else:
        messagebox.showwarning("You must add your DXF file!", "You must add your DXF file!")

def button_go_menu(*args):
    global first_text_value
    global second_text_value
    global file_path
    global entry5_allowed
    global status_path
    global status_elev
    global status_floor
    global status_head

    if file_path != "":
        entry5_allowed = True
        e5.delete(0, END)
        e5.insert(0, str(file_path))
        entry5_allowed = False
        status_path.grid_forget()
        status_path = Label(status_frame, text="File loaded!", fg="green", anchor="center", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)
    else:
        status_path.grid_forget()
        status_path = Label(status_frame, text="Failed to load!", fg="red", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)
    if first_text_value != ["Enter-any-value"]:
        status_elev.grid_forget()
        status_elev = Label(status_frame, text="Elevation loaded!", anchor="center", fg="green", justify=CENTER)
        status_elev.grid(row=1, column=0, sticky=W + E)
    else:
        status_elev.grid_forget()
        status_elev = Label(status_frame, text="Failed to load!", anchor="center", fg="red", justify=CENTER)
        status_elev.grid(row=1, column=0, sticky=W + E)
    if second_text_value != ["Enter-any-value"]:
        status_floor.grid_forget()
        status_floor = Label(status_frame, text="Floors loaded!", anchor="center", fg="green", justify=CENTER)
        status_floor.grid(row=3, column=0, sticky=W + E)
    else:
        status_floor.grid_forget()
        status_floor = Label(status_frame, text="Failed to load!", anchor="center", fg="red", justify=CENTER)
        status_floor.grid(row=3, column=0, sticky=W + E)

    if first_text_value != ["Enter-any-value"] and second_text_value != ["Enter-any-value"] and file_path != "":
        button_start["state"] = "normal"
        status_head.grid_forget()
        status_head = Label(root, text="All data loaded!", fg="green", anchor="center", justify=CENTER, borderwidth=1, relief='sunken')
        status_head.grid(row=7, column=2, columnspan=2, sticky=W+E+N+S)
        button_go["state"] = "disabled"
        filemenu.entryconfig(1, state="disabled")
        button_cancel1["state"] = "disabled"
        button_cancel2["state"] = "disabled"
        button_cancel3["state"] = "disabled"


def show_version():
    messagebox.showinfo(f"Currently working on version {__version__}!", f"You are currently working on"
                                                                        f" version {__version__} of your"
                                                                        f" DXF Files Elevation Engine!")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open DXF file", command=button_add_menu)
filemenu.add_command(label="LOAD!", command=button_go_menu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Deactivate tips", state='normal', command=help_off)
helpmenu.add_command(label="Activate tips", state='disabled', command=help_on)
helpmenu.add_separator()
helpmenu.add_command(label="Version", command=show_version)
menubar.add_cascade(label="Help", menu=helpmenu)

toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Calculator", command=calculator)
toolsmenu.add_command(label="CM/IN Converter", command=cm_in_converter)
menubar.add_cascade(label="Tools", menu=toolsmenu)

setmenu = Menu(menubar, tearoff=0)
setmenu.add_command(label="Faster Algorithm", state="disabled")
setmenu.add_command(label="Advanced Algorithm", state="disabled")
menubar.add_cascade(label="Settings", menu=setmenu)
root.config(menu=menubar)

root.bind("<Control-o>", button_add_menu)
root.bind("<Control-l>", button_go_menu)



root.mainloop()