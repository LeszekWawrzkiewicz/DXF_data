"""Code reused from my old Celsius to Fahrenheit (and vice versa) Converter.
Don't be fooled by names of variables - it serves the purpose to convert
centimeters to inches and vice versa now!"""

from tkinter import *



root = Tk()
root.title('CM/IN Converter')
root.iconbitmap(r'calc.ico')

second_can_change = False

def correct_first(action_code, index, inp):
    if action_code == '0':
        return True
    if action_code == '1':
        if index < '6':
            if inp.isdigit():
                return True
            elif inp == '.':
                text = input_e.get()
                if text == "":
                    return False
                elif "." not in text:
                    if len(text) < 3:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

def correct_second(action_code):
    global second_can_change
    if action_code == '0':
        return True
    else:
        if second_can_change == True:
            second_can_change=False
            return True
        else:
            return False


def go(conversion_type):
    global second_can_change
    second_can_change = True
    if conversion_type == 'ctof':
        cel = float(input_e.get())
        fahr = (cel * 0.39370)
        output_e.delete(0, END)
        output_e.insert(0, fahr)
    if conversion_type == 'ftoc':
        fahr = float(input_e.get())
        cel = (fahr * 2.54)
        output_e.delete(0, END)
        output_e.insert(0, cel)

def F_to_C():
    global button_go
    button_go.grid_forget()
    button_go = Button(root, text='GO!', command=lambda: go('ftoc'))
    button_go.grid(row=2, column=3, columnspan=5, sticky=W+E+N+S, rowspan=2)
    button_CtoF['state'] = 'normal'
    button_FtoC['state'] = 'disabled'
    first_degrees['text'] = 'IN'
    second_degress['text'] = 'CM'
    text['text'] = 'Convert IN to CM below:'

def C_to_F():
    global button_go
    button_go.grid_forget()
    button_go = Button(root, text='GO!', command=lambda: go('ctof'))
    button_go.grid(row=2, column=3, columnspan=5, sticky=W+E+N+S, rowspan=2)
    button_CtoF['state'] = 'disabled'
    button_FtoC['state'] = 'normal'
    first_degrees['text'] = 'CM'
    second_degress['text'] = 'IN'
    text['text'] = 'Convert CM to IN below:'

text = Label(root, text = 'Convert CM to IN below:', font=(None, 15))
text.grid(row=0, column=0, columnspan=10)
frame = LabelFrame(root, bd=0)
frame.grid(row=1, column=0, columnspan=5, sticky=W)



input_e = Entry(frame,  width=6, font=(None, 15))
input_e.grid(row=0, column=0, padx=4, sticky=W)

reg = root.register(correct_first)
input_e.config(validate='key', validatecommand=(reg, '%d', '%i', '%S'))

first_degrees = Label(frame, text = 'CM', font=(None, 15), anchor=W, justify=LEFT)
first_degrees.grid(row=0, column=1, sticky=W)
equal_label = Label(frame, text = '=', font=(None, 15), anchor=W, justify=LEFT)
equal_label.grid(row=0, column=2, sticky=W)

output_e = Entry(frame,  width=6, font=(None, 15))
output_e.grid(row=0, column=3, padx=4, sticky=W)

reg2= root.register(correct_second)
output_e.config(validate='key', validatecommand=(reg2, '%d'))

second_degress = Label(frame, text = 'IN', font=(None, 15), anchor=W, justify=LEFT)
second_degress.grid(row=0, column=4, sticky=W)
button_go = Button(root, text='GO!', command= lambda: go('ctof'))
button_go.grid(row=2, column=3, columnspan=5, sticky=W+E+N+S, rowspan=2)
button_CtoF = Button(root, text='CM>>IN!', state=DISABLED, command=C_to_F)
button_CtoF.grid(row=2, column=0, columnspan=3, sticky=W+E+N+S)
button_FtoC = Button(root, text='IN>>CM!', command=F_to_C)
button_FtoC.grid(row=3, column=0, columnspan=3, sticky=W+E+N+S)



root.mainloop()