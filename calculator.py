from tkinter import *


root = Tk()
root.title('Simple Calculator')
root.iconbitmap(r'calc.ico')


operation = Entry(root, width=35, borderwidth=5)
operation.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
e = Entry(root, width=35, borderwidth=5)
e.grid(row=1, column=0, columnspan=3, padx=10, pady=10)



current_state = None
previous_state = None
cached_num = None
f_num = None
ready_to_math = False
ready_to_equal = False
history = ""


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
            history+= str(second_number)
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


button_1 = Button(root, text='1', padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text='2', padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text='3', padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text='4', padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text='5', padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text='6', padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text='7', padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text='8', padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text='9', padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text='0', padx=40, pady=20, command=lambda: button_click(0))
button_add = Button(root, text='+', padx=39, pady=20, command=button_add, state=DISABLED)
button_equal = Button(root, text='=', padx=40, pady=20, command=button_equal, state=DISABLED)
button_clear = Button(root, text='Clear', padx=79, pady=20, command=button_clear, state=DISABLED)

button_subtract = Button(root, text='-', padx=41, pady=20, command=button_subtract, state=DISABLED)
button_multiply = Button(root, text='x', padx=40, pady=20, command=button_multiply, state=DISABLED)
button_divide = Button(root, text='/', padx=41, pady=20, command=button_divide, state=DISABLED)

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
button_float = Button(root, text='.', padx=40, pady=20, command=button_float)

button_clear.grid(row=5, column=1, columnspan=2)
button_add.grid(row=6, column=0)
button_equal.grid(row=6, column=1)
button_float.grid(row=6, column=2)

button_subtract.grid(row=7, column=0)
button_multiply.grid(row=7, column=1)
button_divide.grid(row=7, column=2)

root.mainloop()