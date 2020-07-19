from tkinter import *
from tkinter.filedialog import askopenfilename
import time
from tkinter import messagebox
import dxfgrabber
from operator import itemgetter
import sqlite3
import os



root = Tk()
root.iconbitmap('icon.ico')
root.title('DXF Files Elevation Engine')
first_text_value = ["Enter-any-value"]
second_text_value = ["Enter-any-value"]
file_path = ""
entry3_allowed = False
entry4_allowed = False
entry5_allowed = False


clicked = StringVar()
clicked2 = StringVar()
clicked.set(first_text_value[0])
clicked2.set(second_text_value[0])

def button_add():
    global file_path
    global status_path
    file = askopenfilename(filetypes=[("DXF files", "*.dxf")])
    file_path = file
    if file_path != "":
        messagebox.showinfo("File path added successfully", "File path added successfully")
        button_add["state"] = "disabled"
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
        status_path.grid_forget()
        status_path = Label(status_frame, text="Waiting to enter data", fg="dark orange", anchor="w", justify=CENTER)
        status_path.grid(row=5, column=0, sticky=W + E + N + S)

def button_add_elev():
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
        messagebox.showinfo("Added first text value successfully", f"Added *{add_elevation}* successfully. You can add more than one value")
    elif first_text_value != ["Enter-any-value"] and good_to_go == True:
        first_text_value.append(add_elevation)
        ElevDrop.grid_forget()
        ElevDrop = OptionMenu(root, clicked, *first_text_value)
        ElevDrop.grid(row=1, column=1, sticky=W + E)
        messagebox.showinfo("Added first text value successfully",f"Added {add_elevation} successfully. You can add more values")


def button_add_floor():
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
        messagebox.showinfo("Added second text value successfully",
                            f"Added *{add_floor}* successfully. You can add more than one value")
    elif second_text_value != ["Enter-any-value"] and good_to_go == True:
        second_text_value.append(add_floor)
        FlorDrop.grid_forget()
        FlorDrop = OptionMenu(root, clicked2, *second_text_value)
        FlorDrop.grid(row=4, column=1, sticky=W + E)
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


    def export_data(shape_name, block_name, block_points):
        return f"{block_name}\{shape_name}\{export_data_X_Y(block_points)}\{len(export_data_X_Y(block_points))}\n"

    def export_data_X_Y(block_points):
        final_temp_data = []
        temp_data = []
        for q in block_points:
            temp_data = []
            temp_data.append(int(q[0]))
            temp_data.append(int(q[1]))
            internal_temp_data = tuple(temp_data)
            final_temp_data.append(internal_temp_data)
        return final_temp_data

    def module_size(temp_size):
        temp_data_size = []
        calc_data = int(abs(temp_size[0][0] - temp_size[2][0]))
        temp_data_size.append(calc_data)
        calc_data = int(abs(temp_size[0][1] - temp_size[2][1]))
        temp_data_size.append(calc_data)
        return temp_data_size

    dxf = dxfgrabber.readfile(path)
    temp_code_W_H_total = []
    for blocks in dxf.blocks:
        if blocks.name:
            for elements in blocks:
                temp_code_W_H = {}
                if elements.dxftype == "LWPOLYLINE":
                    temp_code_W_H['code'] = blocks.name
                    temp_code_W_H['B'] = module_size(elements.points)[0]
                    temp_code_W_H['H'] = module_size(elements.points)[1]
                    temp_code_W_H_total.append(temp_code_W_H)
    print(str(temp_code_W_H_total))
    # defines your dxf object

    level_temp_data = {}
    elevation_temp_data = {}
    # print(dxf.entities)
    levels_data_base = set()
    for entity in dxf.entities:
        if entity.dxftype == "MTEXT":
            for el in first_text_value:
                if el in entity.raw_text:
                    elevation_temp_data[int(entity.insert[0])] = entity.raw_text.strip()
            for el in second_text_value:
                if entity.raw_text[1] == el:
                    level_temp_data[int(entity.insert[1])] = entity.raw_text.replace("{", "").replace("}", "")

    left_border = 3000
    right_border = 12000
    dict_module_coordinate = {}
    list_module_coordinate = []
    temp_global_list = []
    temp_local_list = ()

    # print(elevation_temp_data)
    file_X_Y = open('temp_global_list.txt', 'w')
    for entity in dxf.entities:
        if entity.dxftype == "INSERT":
            x_coordinate = int(entity.insert[0])
            y_coordinate = int(entity.insert[1])
            if type(entity.name):
                dict_module_coordinate = {}
                dict_module_coordinate['name'] = entity.name
                dict_module_coordinate['X'] = x_coordinate
                dict_module_coordinate['Y'] = y_coordinate
                x = list(filter(lambda W_data: W_data['code'] == entity.name, temp_code_W_H_total))[0]['B']
                dict_module_coordinate['X_R'] = x
                temp_local_list = (entity.name, x_coordinate, x_coordinate)
                temp_global_list.append(dict_module_coordinate)
                file_X_Y.write(str(temp_local_list))
                temp_local_list = ()

                # for k_b, v_b in elevation_temp_data.items():
    #               if dict_module_coordinate['X'] in range(k_b - left_border, k_b + right_border):
    #                   dict_module_coordinate['elev'] = v_b.replace("{", "").replace("}", "")
    #                  list_module_coordinate.append(dict_module_coordinate)
    #
    file_X_Y.close()

    sorted_list = sorted(temp_global_list, key=itemgetter("X", "Y"))

    # with open('temp_global_list_total.txt', 'w') as file_X_Y:
    #    file_X_Y.write(str(sorted_list))
    file_X_Y = open('temp_global_list_total.txt', 'w')
    for i in sorted_list:
        file_X_Y.write(f"{str(i)}\n")
    file_X_Y.close()
    # with open('temp_global_list.txt','w') as file_X_Y:
    #    file_X_Y.write(str(temp_global_list))
    # with open('file_data_X_Y.txt','wb') as file_X_Y:
    #    file_X_Y.write(pickle.dumps(list_module_coordinate())
    # print("ok")

    # x_data=open('file_data_X_Y.txt','rb'):
    # pickle_X_data=pickle.load(x_data)
    # x_data.close()
    # print(level_temp_data)
    for i in list_module_coordinate:
        Y_temp = int(i['Y'])
        temp_data = []
        temp_data = {abs(k - Y_temp): v for k, v in level_temp_data.items()}
        temp_lambda = lambda temp_data: min(temp_data.items())
        i['level'] = temp_lambda(temp_data)[1].replace("{", "").replace("}", "")

    with open('file_data_X_Y.txt', 'w') as file_X_Y:
        file_X_Y.write(str(list_module_coordinate))

    module_data = {}
    file = open('file_data.txt', 'w')
    # you can access info within each block with the following loop:
    # this will print a new line of points for each polyline it finds in each block

    for blocks in dxf.blocks:
        if "BL." in blocks.name:
            temp_x_y = []
            for elements in blocks:
                if elements.dxftype == "LWPOLYLINE":
                    file.write(export_data("LWPOLYLINE", blocks.name, elements.points))
                    temp = []
                    temp = export_data_X_Y(elements.points)
                    if len(temp) == 4:
                        module_data[blocks.name] = module_size(temp)
                if elements.dxftype == "LINE":
                    temp_x_y.append(elements.start)
                    temp_x_y.append(elements.end)
            if len(temp_x_y) != 0:
                file.write(export_data("LINE", blocks.name, temp_x_y))
    file.close()
    end = time.time()
    messagebox.showinfo("Operation run successfully", f"Operation run successfully in {int(end-start)} seconds")


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
root.mainloop()