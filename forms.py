from tkinter import *
from tkinter.filedialog import askopenfilename

root = Tk()

first_text_value = ""
second_text_value = ""
file_path = ""
entry3_allowed = False
entry4_allowed = False
entry5_allowed = False

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




myLabel1 = Label(root, text="enter first text value:", anchor="w",justify=LEFT)
e1 = Entry(root)
myLabel2 = Label(root, text="enter second text value:", anchor="w",justify=LEFT)
e2 = Entry(root)
myLabel3 = Label(root, text="add dxf file:", anchor="w",justify=LEFT)
button_add = Button(root, text='Add .dxf file', command=button_add)
myLabel4 = Label(root, text="your first text value:", anchor="w",justify=LEFT)
e3 = Entry(root)
myLabel5 = Label(root, text="your second text value:", anchor="w",justify=LEFT)
e4 = Entry(root)
myLabel6 = Label(root, text="path to your file:", anchor="w",justify=LEFT)
e5 = Entry(root)

button_go = Button(root, text='GO!', command=button_go)


myLabel1.grid(row=0, column=0, sticky=W+E)
e1.grid(row=1, column=0)
myLabel2.grid(row=2, column=0, sticky=W+E)
e2.grid(row=3, column=0)
myLabel3.grid(row=4, column=0, sticky=W+E)
button_add.grid(row=5, column=0, sticky=W+E)

myLabel4.grid(row=0, column=1, sticky=W+E)
e3.grid(row=1, column=1)
myLabel5.grid(row=2, column=1, sticky=W+E)
e4.grid(row=3, column=1)
myLabel6.grid(row=4, column=1, sticky=W+E)
e5.grid(row=5, column=1)

button_go.grid(row=6, column=0, columnspan=2, sticky=W+E)

reg= root.register(entry3_not_allowed)
reg2= root.register(entry4_not_allowed)
reg3= root.register(entry5_not_allowed)
e3.config(validate='key', validatecommand=(reg, '%d'))
e4.config(validate='key', validatecommand=(reg2, '%d'))
e5.config(validate='key', validatecommand=(reg3, '%d'))




root.mainloop()