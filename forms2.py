from tkinter import *
from tkinter.filedialog import askopenfilename
import time
import dxfgrabber
from operator import itemgetter

root = Tk()

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
    file = askopenfilename(filetypes=[("DXF files","*.dxf")])
    file_path = file

def entry3_not_allowed(action_code):
    global entry3_allowed
    if action_code == '0':
        return True
    else:
        if entry3_allowed == True:
            entry3_allowed = False
            return True
        else:
            return False
def entry4_not_allowed(action_code):
    global entry4_allowed
    if action_code == '0':
        return True
    else:
        if entry4_allowed == True:
            entry4_allowed = False
            return True
        else:
            return False

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




def button_go():
    global first_text_value
    global second_text_value
    global file_path
    global entry3_allowed
    global entry4_allowed
    global entry5_allowed

    entry3_allowed = True
    entry4_allowed = True
    entry5_allowed = True

    first_text_value = e1.get()
    second_text_value = e2.get()
    e3.delete(0, END)
    e3.insert(0, str(first_text_value))
    e4.delete(0, END)
    e4.insert(0, str(second_text_value))
    e5.delete(0, END)
    e5.insert(0, str(file_path))

    if first_text_value != "" and second_text_value != "" and file_path != "":
        button_start["state"] = "normal"

def button_start():
    global file_path
    global first_text_value
    global second_text_value
    start = time.time()
    path = file_path


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
            if first_text_value in entity.raw_text:
                elevation_temp_data[int(entity.insert[0])] = entity.raw_text.strip()
            if entity.raw_text[1] == second_text_value:
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
    print(end - start)


myLabel1 = Label(root, text="Enter first text value:", anchor="w",justify=LEFT)
e1 = Entry(root)
myLabel2 = Label(root, text="Enter second text value:", anchor="w",justify=LEFT)
e2 = Entry(root)
myLabel3 = Label(root, text="Add dxf file:", anchor="w",justify=LEFT)
button_add = Button(root, text='Add .dxf file', command=button_add)
myLabel4 = Label(root, text="Your first text values:", anchor="w",justify=LEFT)
e3 = Entry(root)
myLabel5 = Label(root, text="Your second text values:", anchor="w",justify=LEFT)
e4 = Entry(root)
myLabel6 = Label(root, text="Path to your dxf file:", anchor="w",justify=LEFT)
e5 = Entry(root)

button_go = Button(root, text='LOAD!', command=button_go)
button_start = Button(root, text='START!', command=button_start, state='disabled')


myLabel1.grid(row=0, column=0, sticky=W+E)
e1.grid(row=1, column=0)
myLabel2.grid(row=3, column=0, sticky=W+E)
ElevDrop = OptionMenu(root, clicked, *first_text_value)
ElevDrop.grid(row=1, column=1, sticky=W+E)
FlorDrop = OptionMenu(root, clicked2, *second_text_value)
FlorDrop.grid(row=4, column=1, sticky=W+E)
button_add_elev = Button(root, text='Add first text values')
button_add_elev.grid(row=2, column=0, columnspan=2, sticky=W+E)
button_add_flor = Button(root, text='Add second text values')
button_add_flor.grid(row=6, column=0, columnspan=2, sticky=W+E)
e2.grid(row=4, column=0)
myLabel3.grid(row=7, column=0, sticky=W+E)
button_add.grid(row=8, column=0, sticky=W+E)

myLabel4.grid(row=0, column=1, sticky=W+E)
#e3.grid(row=1, column=1)
myLabel5.grid(row=3, column=1, sticky=W+E)
#e4.grid(row=3, column=1)
myLabel6.grid(row=7, column=1, sticky=W+E)
e5.grid(row=8, column=1)

button_go.grid(row=10, column=0, columnspan=2, sticky=W+E)
button_start.grid(row=11, column=0, columnspan=2, sticky=W+E)

reg= root.register(entry3_not_allowed)
reg2= root.register(entry4_not_allowed)
reg3= root.register(entry5_not_allowed)
e3.config(validate='key', validatecommand=(reg, '%d'))
e4.config(validate='key', validatecommand=(reg2, '%d'))
e5.config(validate='key', validatecommand=(reg3, '%d'))




root.mainloop()