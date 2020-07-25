from tkinter import *
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
        filemenu.entryconfig(1, state="disabled")
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
        filemenu.entryconfig(1, state="normal")
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

    class connection_insert_frame_X_elevation(dict):
        def __init__(self):
            self = dict()

        def add(self, key, value):
            self[key] = value

    start = time.time()
    path = file_path


    def export_data(shape_name, block_name,
                    block_points):  # calculation to export data about basic and intermediate geometry of the frame
        return f"{block_name}\{shape_name}\{export_data_X_Y(block_points)}\{len(export_data_X_Y(block_points))}\n"

    def module_size(temp_size):
        '''calculation the sizes of the frame when the frame has the insert point
        in bottom left corner, the main frame must be created by POLYLINE'''
        temp_data_size = []
        calc_data = int(abs(temp_size[0][0] - temp_size[2][0]))
        temp_data_size.append(calc_data)
        calc_data = int(abs(temp_size[0][1] - temp_size[2][1]))
        temp_data_size.append(calc_data)
        return temp_data_size

    dxf = dxfgrabber.readfile(path)
    temp_code_W_H_total = []

    file_X_Y = open('file_data_X_Y.txt', 'w')
    '''calculation the main size (width x height; WxH) of the frame'''
    for blocks in dxf.blocks:
        if blocks.name:
            for elements in blocks:
                temp_code_W_H = {}
                if elements.dxftype == "LWPOLYLINE":
                    temp_code_W_H['code'] = blocks.name
                    temp_code_W_H['W'] = module_size(elements.points)[0]
                    temp_code_W_H['H'] = module_size(elements.points)[1]
                    temp_code_W_H_total.append(temp_code_W_H)
                    file_X_Y.write(str(temp_code_W_H))
                    file_X_Y.write('\n')
    file_X_Y.close()
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
                    elevation_temp_data['elev'] = entity.raw_text
                    main_elevation_temp_data.append(elevation_temp_data)
            for el in second_text_value:
                if entity.raw_text[1] == el:
                    level_temp_data[int(entity.insert[1])] = entity.raw_text.replace("{", "").replace("}", "")
    # print(str(main_elevation_temp_data))
    temp_global_list = []
    temp_local_list = ()
    radius = ''
    file_X_Y = open('temp_global_list.txt', 'w')

    '''calculation the location of the middle point of the frames by analysisi insert point of them,
    preparing the temporary data about the "radius", the radius is a half of hypotenuse the frame'''

    for entity in dxf.entities:
        if entity.dxftype == "INSERT":
            x_coordinate = int(entity.insert[0])
            y_coordinate = int(entity.insert[1])
            if type(entity.name) is str:
                dict_module_coordinate = {}
                dict_module_coordinate['name'] = entity.name
                W_frame = list(filter(lambda W_data: W_data['code'] == entity.name, temp_code_W_H_total))[0][
                    'W']  # szerokość modułu
                H_frame = list(filter(lambda H_data: H_data['code'] == entity.name, temp_code_W_H_total))[0][
                    'H']  # wysokość modułu
                temp_local_list = (entity.name, x_coordinate)
                radius = math.sqrt((W_frame / 2) ** 2 + (H_frame / 2) ** 2)
                file_X_Y.write(str(temp_local_list))
                dict_module_coordinate['C_X'] = int(
                    x_coordinate + W_frame / 2)  # C_X-calculation the middle point in horizontal direction - X-direction
                dict_module_coordinate['C_Y'] = int(
                    y_coordinate + H_frame / 2)  # C_Y-calculation the middle point in vertical direction - Y-direction
                dict_module_coordinate['radius'] = int(radius)
                dict_module_coordinate['elev'] = ''
                dict_module_coordinate['level'] = ''
                temp_global_list.append(dict_module_coordinate)
                temp_local_list = ()

    file_X_Y.close()

    sorted_list = sorted(temp_global_list, key=itemgetter("C_X", "C_Y"))
    file_X_Y = open('temp_global_list_total.txt', 'w')
    for i in sorted_list:
        file_X_Y.write(f"{str(i)}\n")
    file_X_Y.close()

    line_list_X = []
    '''get the unique value of insert point to X-direction'''
    for i in sorted_list:
        line_list_X.append(i['C_X'])
    '''sorted list of the unique value of insert X-point on horizontal axis'''
    sorted_line_list_X = sorted(set(line_list_X))
    '''merging unique insert X-point and the radius'''
    total_line_list_X_R = []
    '''find the "radius" value for the X-unique value'''
    for i in sorted_line_list_X:
        line_list_X_R = {}
        line_list_X_R['X'] = i
        response = next((sub for sub in sorted_list if sub['C_X'] == i), None)
        line_list_X_R['R'] = response['radius']
        total_line_list_X_R.append(line_list_X_R)
    counter = 1
    '''create dict with data of location the elevation' text'''
    X_elev_dict_obj = connection_insert_frame_X_elevation()
    '''find the borders between the elevations'''
    previous_X = total_line_list_X_R[0]['X']
    previous_R = total_line_list_X_R[0]['R']
    X_elev_dict_obj.add(previous_X, counter)
    for i in total_line_list_X_R[1:]:
        current_X = i['X']
        current_R = i['R']
        temp_connection_insert_frame_X_elevation = {}
        if current_X - previous_X < current_R / 2 + previous_R / 2:
            X_elev_dict_obj.add(current_X, counter)
            previous_X = i['X']
            previous_R = i['R']
        else:
            counter += 1
            previous_X = i['X']
            previous_R = i['R']
            X_elev_dict_obj.add(previous_X, counter)

    frame_elevation_level = []
    '''sorting location of the "elevation" text'''
    sorted_main_elevation_temp_data = sorted(main_elevation_temp_data, key=itemgetter("X"), reverse=False)
    '''create a list of data: frame, elevation, level'''
    for i in temp_global_list:
        temp_frame_elevation_level = []
        i['elev'] = X_elev_dict_obj[i['C_X']]
        Y_temp = int(i['C_Y'])
        temp_data = []
        temp_data = {abs(k - Y_temp): v for k, v in level_temp_data.items()}
        temp_lambda = lambda temp_data: min(temp_data.items())
        i['level'] = temp_lambda(temp_data)[1].replace("{", "").replace("}", "")
        temp_frame_elevation_level.append(i['name'])
        temp_frame_elevation_level.append(
            sorted_main_elevation_temp_data[i['elev'] - 1]['elev'].replace("{", "").replace("}", ""))
        temp_frame_elevation_level.append(i['level'])
        frame_elevation_level.append(temp_frame_elevation_level)
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
            number_of_rows+=1

    end = time.time()
    messagebox.showinfo("Operation run successfully", f"Operation run successfully in {int(end-start)} seconds")
    messagebox.showinfo("Number of rows in DB", f"There are {number_of_rows} rows in your database")

def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)

    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")

    # sets the geometry of toplevel
    newWindow.geometry("200x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="This is a new window").pack()

def calculator():
    import calculator

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
        filemenu.entryconfig(1, state="disabled")
        status_path.grid_forget()
        status_path = Label(status_frame, text="Ready to load!", fg="dark orange", anchor="center")
        status_path.grid(row=5, column=0, sticky=W+E+N+S)
    else:
        messagebox.showwarning("You must add your DXF file!", "You must add your DXF file!")

def button_go_menu():
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
        filemenu.entryconfig(2, state="disabled")
        button_cancel1["state"] = "disabled"
        button_cancel2["state"] = "disabled"
        button_cancel3["state"] = "disabled"


def show_version():
    messagebox.showinfo(f"Currently working on version {__version__}!", f"You are currently working on"
                                                                        f" version {__version__} of your"
                                                                        f" DXF Files Elevation Engine!")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=openNewWindow)
filemenu.add_command(label="Open DXF file", command=button_add_menu)
filemenu.add_command(label="LOAD!", command=button_go_menu)
filemenu.add_command(label="START!", command=button_start, state='disabled')
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
root.config(menu=menubar)

root.bind("<Control-o>", button_add_menu)

root.mainloop()