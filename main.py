from tkinter import *
import math

root = Tk()
root.title("pyCalc")
scientific_mode = False
angle_mode = "RAD"

frame_standard = Frame(root)
frame_scientific = Frame(root)

frame_standard.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
frame_scientific.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

frame_scientific.grid_remove()

for i in range(7):
    frame_standard.grid_rowconfigure(i, weight=1, uniform="b")

for i in range(9):
    frame_scientific.grid_rowconfigure(i, weight=1, uniform="b")

def fit_window():
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

def show_scientific():
    frame_standard.grid_remove()
    frame_scientific.grid()
    fit_window()

def hide_scientific():
    frame_scientific.grid_remove()
    frame_standard.grid()
    fit_window()

def toggle_scientific():
    global scientific_mode
    if not scientific_mode:
        show_scientific()
        scientific_mode = True
        button_scientific.config(text="Standard")
    else:
        hide_scientific()
        scientific_mode = False
        button_scientific.config(text="Scientific")

def toggle_angle_mode():
    global angle_mode

    if angle_mode == "RAD":
        angle_mode = "DEG"
        button_angle.config(text="DEG")
    else:
        angle_mode = "RAD"
        button_angle.config(text="RAD")


e = Entry(root, width=35, borderwidth=5, justify="right")
e.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

e.bind("<Key>", lambda event: "break")

button_scientific = Button(root, text="Scientific", padx=20, pady=10, command=toggle_scientific)
button_scientific.grid(row=0, column=4, padx=5, pady=10, sticky="nsew")

f_num = 0.0
operation = None
last_operand = None
new_input = False

def convert_to_float(s):
    try:
        return float(s)
    except:
        return None

def set_display(value):
    global new_input

    if isinstance(value, float):
        value = round(value, 10)

        if value.is_integer():
            value = int(value)
        else:
            value = format(value, ".10f").rstrip("0").rstrip(".")

    e.delete(0, END)
    e.insert(0, str(value))
    new_input = True

def button_click(number):
    global new_input
    current = e.get()
    if current == "Error":
        current = ""
    if new_input:
        e.delete(0, END)
        e.insert(0, str(number))
        new_input = False
    else:
        e.delete(0, END)
        e.insert(0, str(current) + str(number))

def button_C():
    global f_num, operation, last_operand, new_input
    f_num = 0.0
    operation = None
    last_operand = None
    new_input = False
    e.delete(0, END)

def button_CE():
    global new_input
    e.delete(0, END)
    new_input = False

def button_bs():
    global new_input
    current = e.get()
    if current == "Error":
        e.delete(0, END)
        new_input = False
        return
    e.delete(0, END)
    e.insert(0, current[:-1])
    new_input = False

def button_dot():
    global new_input
    current = e.get()
    if current == "Error":
        e.delete(0, END)
        current = ""
    if new_input:
        e.delete(0, END)
        e.insert(0, "0.")
        new_input = False
        return
    if "." not in current:
        e.insert(END, ".")

def button_negate():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return
    set_display(-value)

def calculate(a, op, b):
    if op == "addition":
        return a + b
    if op == "subtraction":
        return a - b
    if op == "multiplication":
        return a * b
    if op == "division":
        return a / b
    if op == "power":
        return a ** b
    if op == "modulus":
        return a % b
    return b

def set_operation(op):
    global f_num, operation, last_operand, new_input

    cur = e.get()
    cur_val = convert_to_float(cur) if cur != "" and cur != "Error" else None

    if cur_val is None:
        if operation is not None:
            operation = op
        else:
            operation = op
        new_input = True
        return

    if operation is not None and not new_input:
        try:
            f_num = calculate(f_num, operation, cur_val)
            set_display(f_num)
        except:
            set_display("Error")
            operation = None
            last_operand = None
            return

    else:
        f_num = cur_val

    operation = op
    last_operand = None
    e.delete(0, END)
    new_input = False

def button_add():
    set_operation("addition")

def button_subtract():
    set_operation("subtraction")

def button_multiply():
    set_operation("multiplication")

def button_divide():
    set_operation("division")

def button_power():
    set_operation("power")

def button_mod():
    set_operation("modulus")

def button_equal():
    global f_num, operation, last_operand, new_input

    if operation is None:
        return

    cur = e.get()

    if cur == "" or cur == "Error":
        if last_operand is None:
            b = f_num
            last_operand = b
        else:
            b = last_operand
    else:
        if new_input and last_operand is not None:
            b = last_operand
        else:
            b = convert_to_float(cur)
            if b is None:
                set_display("Error")
                operation = None
                last_operand = None
                return
            last_operand = b

    try:
        f_num = calculate(f_num, operation, b)
        set_display(f_num)
    except:
        set_display("Error")
        operation = None
        last_operand = None
        new_input = True

def button_square():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return
    set_display(value ** 2)

def button_square_root():
    value = convert_to_float(e.get())
    if value is None or value < 0:
        set_display("Error")
        return
    set_display(math.sqrt(value))

def button_reciprocal():
    value = convert_to_float(e.get())
    if value is None or value == 0:
        set_display("Error")
        return
    set_display(1 / value)

def button_log():
    value = convert_to_float(e.get())
    if value is None or value <= 0:
        set_display("Error")
        return
    set_display(math.log10(value))

def button_ln():
    value = convert_to_float(e.get())
    if value is None or value <= 0:
        set_display("Error")
        return
    set_display(math.log(value))

def button_sin():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return

    if angle_mode == "DEG":
        value = math.radians(value)

    set_display(math.sin(value))


def button_cos():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return

    if angle_mode == "DEG":
        value = math.radians(value)

    set_display(math.cos(value))


def button_tan():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return

    if angle_mode == "DEG":
        value = math.radians(value)

    set_display(math.tan(value))


def button_ctg():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return

    if angle_mode == "DEG":
        value = math.radians(value)

    t = math.tan(value)
    if t == 0:
        set_display("Error")
        return

    set_display(1 / t)

def button_fact():
    try:
        n = int(float(e.get()))
        if n < 0:
            raise ValueError
        set_display(math.factorial(n))
    except:
        set_display("Error")

def button_percent():
    global f_num, operation
    value = convert_to_float(e.get())
    if value is None:
        return

    if operation is None:
        set_display(value / 100)
    else:
        if operation in ("addition", "subtraction"):
            set_display(f_num * (value / 100))
        else:
            set_display(value / 100)

def button_abs():
    value = convert_to_float(e.get())
    if value is None:
        set_display("Error")
        return
    set_display(abs(value))

def button_pi():
    set_display(math.pi)

def button_e():
    set_display(math.e)

button_1 = Button(frame_standard, text="1", padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(frame_standard, text="2", padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(frame_standard, text="3", padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(frame_standard, text="4", padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(frame_standard, text="5", padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(frame_standard, text="6", padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(frame_standard, text="7", padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(frame_standard, text="8", padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(frame_standard, text="9", padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(frame_standard, text="0", padx=40, pady=20, command=lambda: button_click(0))

button_add_btn = Button(frame_standard, text="+", padx=40, pady=20, command=button_add)
button_sub_btn = Button(frame_standard, text="-", padx=40, pady=20, command=button_subtract)
button_mul_btn = Button(frame_standard, text="*", padx=40, pady=20, command=button_multiply)
button_div_btn = Button(frame_standard, text="/", padx=40, pady=20, command=button_divide)
button_equal_btn = Button(frame_standard, text="=", padx=40, pady=20, command=button_equal)

button_C_btn = Button(frame_standard, text="C", padx=40, pady=20, command=button_C)
button_CE_btn = Button(frame_standard, text="CE", padx=40, pady=20, command=button_CE)
button_bsci_btn = Button(frame_standard, text="bs", padx=40, pady=20, command=button_bs)
button_percent_btn = Button(frame_standard, text="%", padx=40, pady=20, command=button_percent)

button_recip_btn = Button(frame_standard, text="1/x", padx=40, pady=20, command=button_reciprocal)
button_square_btn = Button(frame_standard, text="x²", padx=40, pady=20, command=button_square)
button_sqrt_btn = Button(frame_standard, text="√", padx=40, pady=20, command=button_square_root)

button_neg_btn = Button(frame_standard, text="+/-", padx=40, pady=20, command=button_negate)
button_dot_btn = Button(frame_standard, text=".", padx=40, pady=20, command=button_dot)

button_pi_const = Button(frame_scientific, text="π", padx=40, pady=20, command=button_pi)
button_e_const = Button(frame_scientific, text="e", padx=40, pady=20, command=button_e)

button_percent_btn.grid(row=1, column=0, sticky="nsew")
button_CE_btn.grid(row=1, column=1, sticky="nsew")
button_C_btn.grid(row=1, column=2, sticky="nsew")
button_bsci_btn.grid(row=1, column=3, sticky="nsew")

button_recip_btn.grid(row=2, column=0, sticky="nsew")
button_square_btn.grid(row=2, column=1, sticky="nsew")
button_sqrt_btn.grid(row=2, column=2, sticky="nsew")
button_div_btn.grid(row=2, column=3, sticky="nsew")

button_7.grid(row=3, column=0, sticky="nsew")
button_8.grid(row=3, column=1, sticky="nsew")
button_9.grid(row=3, column=2, sticky="nsew")
button_mul_btn.grid(row=3, column=3, sticky="nsew")

button_4.grid(row=4, column=0, sticky="nsew")
button_5.grid(row=4, column=1, sticky="nsew")
button_6.grid(row=4, column=2, sticky="nsew")
button_sub_btn.grid(row=4, column=3, sticky="nsew")

button_1.grid(row=5, column=0, sticky="nsew")
button_2.grid(row=5, column=1, sticky="nsew")
button_3.grid(row=5, column=2, sticky="nsew")
button_add_btn.grid(row=5, column=3, sticky="nsew")

button_neg_btn.grid(row=6, column=0, sticky="nsew")
button_0.grid(row=6, column=1, sticky="nsew")
button_dot_btn.grid(row=6, column=2, sticky="nsew")
button_equal_btn.grid(row=6, column=3, sticky="nsew")

sci_percent = Button(frame_scientific, text="%", padx=40, pady=20, command=button_percent)
sci_CE = Button(frame_scientific, text="CE", padx=40, pady=20, command=button_CE)
sci_C = Button(frame_scientific, text="C", padx=40, pady=20, command=button_C)
sci_bs = Button(frame_scientific, text="bs", padx=40, pady=20, command=button_bs)

sci_sin = Button(frame_scientific, text="sin", padx=40, pady=20, command=button_sin)
sci_cos = Button(frame_scientific, text="cos", padx=40, pady=20, command=button_cos)
sci_tan = Button(frame_scientific, text="tan", padx=40, pady=20, command=button_tan)
sci_ctg = Button(frame_scientific, text="ctg", padx=40, pady=20, command=button_ctg)

sci_log = Button(frame_scientific, text="log", padx=40, pady=20, command=button_log)
sci_ln  = Button(frame_scientific, text="ln",  padx=40, pady=20, command=button_ln)
sci_pow = Button(frame_scientific, text="xʸ", padx=40, pady=20, command=button_power)
sci_mod = Button(frame_scientific, text="mod", padx=40, pady=20, command=button_mod)

sci_abs = Button(frame_scientific, text="abs", padx=40, pady=20, command=button_abs)
sci_fact = Button(frame_scientific, text="fact", padx=40, pady=20, command=button_fact)
sci_recip = Button(frame_scientific, text="1/x", padx=40, pady=20, command=button_reciprocal)
sci_div = Button(frame_scientific, text="/", padx=40, pady=20, command=button_divide)

sci_7 = Button(frame_scientific, text="7", padx=40, pady=20, command=lambda: button_click(7))
sci_8 = Button(frame_scientific, text="8", padx=40, pady=20, command=lambda: button_click(8))
sci_9 = Button(frame_scientific, text="9", padx=40, pady=20, command=lambda: button_click(9))
sci_mul = Button(frame_scientific, text="*", padx=40, pady=20, command=button_multiply)

sci_4 = Button(frame_scientific, text="4", padx=40, pady=20, command=lambda: button_click(4))
sci_5 = Button(frame_scientific, text="5", padx=40, pady=20, command=lambda: button_click(5))
sci_6 = Button(frame_scientific, text="6", padx=40, pady=20, command=lambda: button_click(6))
sci_sub = Button(frame_scientific, text="-", padx=40, pady=20, command=button_subtract)

sci_1 = Button(frame_scientific, text="1", padx=40, pady=20, command=lambda: button_click(1))
sci_2 = Button(frame_scientific, text="2", padx=40, pady=20, command=lambda: button_click(2))
sci_3 = Button(frame_scientific, text="3", padx=40, pady=20, command=lambda: button_click(3))
sci_add = Button(frame_scientific, text="+", padx=40, pady=20, command=button_add)

sci_neg = Button(frame_scientific, text="+/-", padx=40, pady=20, command=button_negate)
sci_0 = Button(frame_scientific, text="0", padx=40, pady=20, command=lambda: button_click(0))
sci_dot = Button(frame_scientific, text=".", padx=40, pady=20, command=button_dot)
sci_eq = Button(frame_scientific, text="=", padx=40, pady=20, command=button_equal)
button_angle = Button(frame_scientific, text="RAD", padx=40, pady=20, command=toggle_angle_mode)
sci_percent.grid(row=1, column=0, sticky="nsew")
sci_CE.grid(row=1, column=1, sticky="nsew")
sci_C.grid(row=1, column=2, sticky="nsew")
sci_bs.grid(row=1, column=3, sticky="nsew")
button_angle.grid(row=1, column=4, sticky="nsew")
sci_sin.grid(row=2, column=0, sticky="nsew")
sci_cos.grid(row=2, column=1, sticky="nsew")
sci_tan.grid(row=2, column=2, sticky="nsew")
sci_ctg.grid(row=2, column=3, sticky="nsew")

sci_log.grid(row=3, column=0, sticky="nsew")
sci_ln.grid(row=3, column=1, sticky="nsew")
sci_pow.grid(row=3, column=2, sticky="nsew")
sci_mod.grid(row=3, column=3, sticky="nsew")

sci_abs.grid(row=4, column=0, sticky="nsew")
sci_fact.grid(row=4, column=1, sticky="nsew")
sci_recip.grid(row=4, column=2, sticky="nsew")
sci_div.grid(row=4, column=3, sticky="nsew")

sci_7.grid(row=5, column=0, sticky="nsew")
sci_8.grid(row=5, column=1, sticky="nsew")
sci_9.grid(row=5, column=2, sticky="nsew")
sci_mul.grid(row=5, column=3, sticky="nsew")

sci_4.grid(row=6, column=0, sticky="nsew")
sci_5.grid(row=6, column=1, sticky="nsew")
sci_6.grid(row=6, column=2, sticky="nsew")
sci_sub.grid(row=6, column=3, sticky="nsew")

sci_1.grid(row=7, column=0, sticky="nsew")
sci_2.grid(row=7, column=1, sticky="nsew")
sci_3.grid(row=7, column=2, sticky="nsew")
sci_add.grid(row=7, column=3, sticky="nsew")

sci_neg.grid(row=8, column=0, sticky="nsew")
sci_0.grid(row=8, column=1, sticky="nsew")
sci_dot.grid(row=8, column=2, sticky="nsew")
sci_eq.grid(row=8, column=3, sticky="nsew")

button_pi_const.grid(row=2, column=4, sticky="nsew")
button_e_const.grid(row=3, column=4, sticky="nsew")

fit_window()
root.resizable(False, False)
root.mainloop()