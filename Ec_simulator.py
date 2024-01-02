##############################################################الحمد لله##########################################################################

import tkinter as tk
from tkinter import simpledialog
import PySpice.Logging.Logging as Logging
import numpy as np
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_Ohm, u_V, u_A, u_nF, u_mH, u_W, u_kHz, u_us
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.pyplot import semilogx
from matplotlib import pyplot
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from engineering_notation import EngNumber
from matplotlib.ticker import EngFormatter

#################################################################################################################################################

class Resistor_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        x = 90
        y = 120
        self.points = [x, y, x+15, y, x+20, y+10, x+30, y-10, x+40, y+10, x+50, y-10, x+60, y+10, x+70,y-10 , x+75, y, x+90, y]
        self.body = None
        self.value = "10"
        self.color = None
        self.index = index_list[0]
        index_list[0]+=1
        self.left=None
        self.right=None

        self.draw_resistor()
        self.coords()
        
        # press and drag
        self.canvas.tag_bind(self.body, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,A,b,B,c,C,d,D,e,E,f,F,g,G,h,H,i,I,j,J = self.canvas.coords(self.body)
        self.left = (a,A)
        self.right= (j,J)

    def draw_resistor(self):
        self.body = self.canvas.create_line(self.points, smooth="false", width=3, fill=self.color, tags="resistor")

    def on_press(self, event):
        # store the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        # the chang of rhe position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="value", command=self.change_value)
        menu.add_command(label="rotate", command=self.rotate_resistor_right)
        menu.add_command(label="delete", command=self.delete_combo)
        menu.add_command(label="view current", command=lambda event=event: self.view_current(event))
        menu.add_command(label="view power", command=lambda event=event: self.view_power(event))

        menu.post(event.x_root, event.y_root)

    def view_current(self,event):
        self.label1 = None
        lable_list.append(self.label1)
        #print((self.x, self.y))

        a=v_l[f_d[(self.right)]]
        b=v_l[f_d[(self.left)]]
        c=abs(a-b)
        d=c/int(self.value)
        self.label1=tk.Label(canvas,text=f"{d} A",bg="blue",fg="cyan",font=("araial",14))
        w,v=self.right
        self.label1.place(x=w-45,y=v-30)

        if self.label1 is not None:
                self.label1.bind("<Button-3>", lambda event=event: self.del_label())

    def del_label(self):
        #self.canvas.delete(self.label)
        self.label1.destroy()
        #lable_list.remove(self.label1)


    def view_power(self, event):
        self.label1 = None
        lable_list.append(self.label1)
        #print((self.x, self.y))

        a=v_l[f_d[(self.right)]]
        b=v_l[f_d[(self.left)]]
        c=abs(a-b)
        i=c/int(self.value)
        p = i*i*int(self.value)
        self.label1=tk.Label(canvas,text=f"{p} W",bg="blue",fg="cyan",font=("araial",14))
        w,v=self.right
        self.label1.place(x=w-45,y=v-30)

        if self.label1 is not None:
                self.label1.bind("<Button-3>", lambda event=event: self.del_label())

    def del_label(self):
        #self.canvas.delete(self.label)
        self.label1.destroy()
        #lable_list.remove(self.label1)


    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body, fill=self.color)

    def change_value(self):
        new_value = simpledialog.askstring("resistor value", "please enter the value", initialvalue=self.value)
        if new_value:
            self.value = new_value

    def rotate_resistor_right(self):
        a,A,b,B,c,C,d,D,e,E,f,F,g,G,h,H,i,I,j,J = self.canvas.coords(self.body)
        new_coords = [j,J-90,j,J-75,j-10,J-70,j+10,J-60,j-10,J-50,j+10,J-40,j-10,J-30,j+10,J-20,j,J-15,j,J]

        self.canvas.coords(self.body, *new_coords)
        

    def delete_combo(self):
        self.canvas.delete(self.body)
        resistor_list[self.index]=0

#################################################################################################################################################

class Capacitor_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        x = 90
        y = 120
        self.points_r = [x, y, x+35, y, x+35, y+20, x+35, y-20]
        self.points_l = [x+55, y+20, x+55, y-20, x+55, y, x+90, y]
        self.body_r = None
        self.body_l = None
        self.value = "10"
        self.color = None
        self.index = index_list[1]
        index_list[1]+=1
        self.left=None
        self.right=None

        self.draw_capacitor()
        self.coords()
        
        # press and drag
        self.canvas.tag_bind(self.body_r, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body_r, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body_r, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body_l, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body_l, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body_l, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,A,b,B,c,C,d,D = self.canvas.coords(self.body_r)
        e,E,f,F,g,G,h,H = self.canvas.coords(self.body_l) 
        self.left = (a,A)
        self.right= (h,H)

    def draw_capacitor(self):
        self.body_r = self.canvas.create_line(self.points_r, smooth="false", width=3, fill=self.color, tags="capacitor_r")
        self.body_l = self.canvas.create_line(self.points_l, smooth="false", width=3, fill=self.color, tags="capacitor_r")

    def on_press(self, event):
        # store the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        # the change of position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body_r, delta_x, delta_y)
        self.canvas.move(self.body_l, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="value", command=self.change_value)
        menu.add_command(label="rotate", command=self.rotate_capacitor_right)
        menu.add_command(label="delete", command=self.delete_combo)
        menu.post(event.x_root, event.y_root)

    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body_r, fill=self.color)
            self.canvas.itemconfig(self.body_l, fill=self.color)

    def change_value(self):
        new_value = simpledialog.askstring("please ,enter the new value", initialvalue=self.value)
        if new_value:
            self.value = new_value

    def rotate_capacitor_right(self):
        a,A,b,B,c,C,d,D = self.canvas.coords(self.body_r)
        e,E,f,F,g,G,h,H = self.canvas.coords(self.body_l) 
        new_coords_r = [h,H-90,h,H-55,h+20,H-55,h-20,H-55]
        new_coords_l = [h+20,H-35,h-20,H-35,h,H-35,h,H]
        self.canvas.coords(self.body_r, *new_coords_r)
        self.canvas.coords(self.body_l, *new_coords_l)
        

    def delete_combo(self):
        self.canvas.delete(self.body_r)
        self.canvas.delete(self.body_l)
        capacitor_list[self.index]=0

#################################################################################################################################################

class Inductance_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 90
        self.y = 120
        self.body1 = None
        self.body2 = None
        self.body3 = None
        self.body4 = None
        self.body5 = None
        self.body6 = None
        self.left=None
        self.right=None
        self.points1 = [self.x,self.y, self.x+15, self.y]
        self.points2 = [self.x+75, self.y, self.x+90, self.y]
        self.value = "10"
        self.color = None
        self.index = index_list[2]
        index_list[2]+=1

        self.draw_Inductance()
        self.coords()
        
        # press and drag
        self.canvas.tag_bind(self.body1, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body1, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body1, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body2, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body2, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body2, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body3, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body3, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body3, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body4, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body4, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body4, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body5, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body5, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body5, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,b,c,d = self.canvas.coords(self.body1)
        e,f,g,h = self.canvas.coords(self.body5)
        self.left = (a,b)
        self.right= (g,h)
    
    def draw_Inductance(self):
        self.body1 = self.canvas.create_line(self.points1, smooth="false", width=3, fill=self.color, tags="inductance1")
        self.body2 = self.canvas.create_oval(self.x+15, self.y-12, self.x+39, self.y+12, outline=self.color, width=3, tags="inductance2")
        self.body3 = self.canvas.create_oval(self.x+33, self.y-12, self.x+57, self.y+12, outline=self.color, width=3, tags="inductance3")
        self.body4 = self.canvas.create_oval(self.x+51, self.y-12, self.x+75, self.y+12, outline=self.color, width=3, tags="inductance4")
        self.body5 = self.canvas.create_line(self.points2, smooth="false", width=3, fill=self.color, tags="inductance5")

    def on_press(self, event):
        # strore the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        #the chang of position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body1, delta_x, delta_y)
        self.canvas.move(self.body2, delta_x, delta_y)
        self.canvas.move(self.body3, delta_x, delta_y)
        self.canvas.move(self.body4, delta_x, delta_y)
        self.canvas.move(self.body5, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="value", command=self.change_value)
        menu.add_command(label="rotate", command=self.rotate_inductance_right)
        menu.add_command(label="delete", command=self.delete_combo)
        menu.post(event.x_root, event.y_root)

    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body1, fill=self.color)
            self.canvas.itemconfig(self.body2, outline=self.color)
            self.canvas.itemconfig(self.body3, outline=self.color)
            self.canvas.itemconfig(self.body4, outline=self.color)
            self.canvas.itemconfig(self.body5, fill=self.color)

    def change_value(self):
        new_value = simpledialog.askstring("please enter the new value", initialvalue=self.value)
        if new_value:
            self.value = new_value

    def rotate_inductance_right(self):
        a, b, c, d= self.canvas.coords(self.body5)
        n1=[c,d-90,c,d-75]
        n2=[c-12,d-75,c+12,d-51]
        n3=[c-12,d-57,c+12,d-33]
        n4=[c-12,d-39,c+12,d-15]
        n5=[c,d-15,c,d]

        self.canvas.coords(self.body1, n1)
        self.canvas.coords(self.body2, n2)
        self.canvas.coords(self.body3, n3)
        self.canvas.coords(self.body4, n4)
        self.canvas.coords(self.body5, n5)
        

    def delete_combo(self):
        self.canvas.delete(self.body1)
        self.canvas.delete(self.body2)
        self.canvas.delete(self.body3)
        self.canvas.delete(self.body4)
        self.canvas.delete(self.body5)
        inductance_list[self.index]=0

#################################################################################################################################################
        
class DC_Power_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 90
        self.y = 120
        self.points1 = [self.x,self.y,self.x+15,self.y]
        self.points2 = [self.x+24,self.y, self.x+40,self.y]
        self.points3 = [self.x+50,self.y, self.x+66,self.y]
        self.points4 = [self.x+58,self.y+8, self.x+58,self.y-8]
        self.points5 = [self.x+75,self.y,self.x+90,self.y]
        self.body1 = None
        self.body2 = None
        self.body3 = None
        self.body4 = None
        self.body5 = None
        self.body6 = None
        self.left=None
        self.right=None
        self.value = "10"
        self.color = None
        self.index = index_list[3]
        index_list[3]+=1

        self.draw_dc()
        self.coords()
        
        # ربط حدث النقر والسحب
        self.canvas.tag_bind(self.body1, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body1, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body1, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body2, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body2, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body2, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body3, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body3, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body3, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body4, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body4, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body4, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body5, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body5, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body5, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body6, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body6, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body6, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,b,c,d = self.canvas.coords(self.body1)
        e,f,g,h = self.canvas.coords(self.body6)
        self.left = (a,b)
        self.right= (g,h)
    
    def draw_dc(self):
        self.body1 = self.canvas.create_line(self.points1, smooth="false", width=3, fill=self.color, tags="dc1")
        self.body2 = self.canvas.create_oval(self.x+15, self.y-30, self.x+75, self.y+30, outline=self.color, width=3, tags="dc2")
        self.body3 = self.canvas.create_line(self.points2, smooth="false", width=3, fill=self.color, tags="dc3")
        self.body4 = self.canvas.create_line(self.points3, smooth="false", width=3, fill=self.color, tags="dc4")
        self.body5 = self.canvas.create_line(self.points4, smooth="false", width=3, fill=self.color, tags="dc5")
        self.body6 = self.canvas.create_line(self.points5, smooth="false", width=3, fill=self.color, tags="dc6")

    def on_press(self, event):
        # store the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        # the change of position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body1, delta_x, delta_y)
        self.canvas.move(self.body2, delta_x, delta_y)
        self.canvas.move(self.body3, delta_x, delta_y)
        self.canvas.move(self.body4, delta_x, delta_y)
        self.canvas.move(self.body5, delta_x, delta_y)
        self.canvas.move(self.body6, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="value", command=self.change_value)
        menu.add_command(label="rotate", command=self.rotate_dcpower_right)
        menu.add_command(label="delete", command=self.delete_dc)
        menu.add_command(label="view power", command=lambda event=event: self.view_power(event))
        menu.post(event.x_root, event.y_root)

    def view_power(self, event):
        self.label1 = None
        lable_list.append(self.label1)
        #print((self.x, self.y))

        p = mx * int(self.value)
        self.label1=tk.Label(canvas,text=f"{p} W",bg="blue",fg="cyan",font=("araial",14))
        w,v=self.right
        self.label1.place(x=w-45,y=v-30)

        if self.label1 is not None:
                self.label1.bind("<Button-3>", lambda event=event: self.del_label())

    def del_label(self):
        #self.canvas.delete(self.label)
        self.label1.destroy()
        #lable_list.remove(self.label1)

    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body1, fill=self.color)
            self.canvas.itemconfig(self.body2, outline=self.color)
            self.canvas.itemconfig(self.body3, fill=self.color)
            self.canvas.itemconfig(self.body4, fill=self.color)
            self.canvas.itemconfig(self.body5, fill=self.color)
            self.canvas.itemconfig(self.body6, fill=self.color)

    def change_value(self):
        new_value = simpledialog.askstring("please enter the new value", initialvalue=self.value)
        if new_value:
            self.value = new_value

    def rotate_dcpower_right(self):
        a,b,c,d = self.canvas.coords(self.body6)
        n1=[c,d-90,c,d-75]
        n2=[c-30,d-75,c+30,d-15]
        n3=[c,d-66,c,d-50]
        n4=[c,d-40,c,d-24]
        n5=[c+8,d-32,c-8,d-32]
        n6=[c,d-15,c,d]
        self.canvas.coords(self.body1, n1)
        self.canvas.coords(self.body2, n2)
        self.canvas.coords(self.body3, n3)
        self.canvas.coords(self.body4, n4)
        self.canvas.coords(self.body5, n5)
        self.canvas.coords(self.body6, n6)
        

    def delete_dc(self):
        self.canvas.delete(self.body1)
        self.canvas.delete(self.body2)
        self.canvas.delete(self.body3)
        self.canvas.delete(self.body4)
        self.canvas.delete(self.body5)
        self.canvas.delete(self.body6)
        dcpower_list[self.index]=0

#################################################################################################################################################
        
class AC_Power_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 90
        self.y = 120
        self.points1 = [self.x,self.y,self.x+15,self.y]
        self.points2 = [self.x+25, self.y, self.x+35, self.y-20,self.x+45,self.y, self.x+55, self.y+20, self.x+65, self.y]
        self.points3 = [self.x+75,self.y,self.x+90,self.y]
        self.body1 = None
        self.body2 = None
        self.body3 = None
        self.body4 = None
        self.value = "10"
        self.hz = 0.06
        self.color = None
        self.left=None
        self.right=None
        self.index = index_list[4]
        index_list[4]+=1

        self.draw_ac()
        self.coords()
        
        # pree and drag
        self.canvas.tag_bind(self.body1, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body1, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body1, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body2, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body2, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body2, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body3, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body3, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body3, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body4, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body4, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body4, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,b,c,d = self.canvas.coords(self.body1)
        e,f,g,h = self.canvas.coords(self.body4)
        self.left = (a,b)
        self.right= (g,h)
    
    def draw_ac(self):
        self.body1 = self.canvas.create_line(self.points1, smooth="false", width=3, fill=self.color, tags="ac1")
        self.body2 = self.canvas.create_oval(self.x+15, self.y-30, self.x+75, self.y+30, outline=self.color, width=3, tags="ac2")
        self.body3 = self.canvas.create_line(self.points2, smooth="true", width=3, fill=self.color, tags="ac3")
        self.body4 = self.canvas.create_line(self.points3, smooth="false", width=3, fill=self.color, tags="ac4")

    def on_press(self, event):
        # store the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        # the chanf=g of position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body1, delta_x, delta_y)
        self.canvas.move(self.body2, delta_x, delta_y)
        self.canvas.move(self.body3, delta_x, delta_y)
        self.canvas.move(self.body4, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="value", command=self.change_value)
        menu.add_command(label="frequency", command=self.change_hz)
        menu.add_command(label="rotate", command=self.rotate_acpower_right)
        menu.add_command(label="delete", command=self.delete_ac)
        menu.post(event.x_root, event.y_root)

    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body1, fill=self.color)
            self.canvas.itemconfig(self.body2, outline=self.color)
            self.canvas.itemconfig(self.body3, fill=self.color)
            self.canvas.itemconfig(self.body4, fill=self.color)

    def change_value(self):
        new_value = simpledialog.askstring("enter the new value", initialvalue=self.value)
        if new_value:
            self.value = new_value

    def change_hz(self):
        new_value = simpledialog.askfloat("enter the new value", initialvalue=self.hz)
        if new_value:
            self.hz = new_value

    def rotate_acpower_right(self):
        a,b,c,d = self.canvas.coords(self.body4)
        n1=[c,d-90,c,d-75]
        n2=[c-30,d-75,c+30,d-15]
        n3=[c,d-65,c+20,d-55,c,d-45,c-20,d-35,c,d-25]
        n4=[c,d-15,c,d]
        self.canvas.coords(self.body1, n1)
        self.canvas.coords(self.body2, n2)
        self.canvas.coords(self.body3, n3)
        self.canvas.coords(self.body4, n4)
        

    def delete_ac(self):
        self.canvas.delete(self.body1)
        self.canvas.delete(self.body2)
        self.canvas.delete(self.body3)
        self.canvas.delete(self.body4)
        acpower_list[self.index]=0

#################################################################################################################################################

class Ground_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 150
        self.y = 120
        self.points1 = [self.x,self.y-30,self.x,self.y]
        self.points2 = [self.x-30,self.y,self.x+30,self.y]
        self.points3 = [self.x-20,self.y+7.5,self.x+20,self.y+7.5]
        self.points4 = [self.x-10,self.y+15,self.x+10,self.y+15]
        self.body1 = None
        self.body2 = None
        self.body3 = None
        self.body4 = None
        self.point = None
        self.value = "0"
        self.color = None
        self.index = index_list[5]
        index_list[5]+=1

        self.draw_ground()
        self.coords()

        
        # press and drag
        self.canvas.tag_bind(self.body1, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body1, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body1, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body2, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body2, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body2, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body3, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body3, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body3, "<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.body4, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.body4, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.body4, "<Button-3>", self.show_context_menu)

    def coords(self):
        a,b,c,d = self.canvas.coords(self.body1)
        self.point = (a,b)
    
    def draw_ground(self):
        self.body1 = self.canvas.create_line(self.points1, smooth="false", width=3, fill=self.color, tags="g1")
        self.body2 = self.canvas.create_line(self.points2, smooth="false", width=3, fill=self.color, tags="g2")
        self.body3 = self.canvas.create_line(self.points3, smooth="false", width=3, fill=self.color, tags="g3")
        self.body4 = self.canvas.create_line(self.points4, smooth="false", width=3, fill=self.color, tags="g4")

    def on_press(self, event):
        # store the start position
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event):
        # the change of position and moving
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        self.canvas.move(self.body1, delta_x, delta_y)
        self.canvas.move(self.body2, delta_x, delta_y)
        self.canvas.move(self.body3, delta_x, delta_y)
        self.canvas.move(self.body4, delta_x, delta_y)
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="rotate", command=self.rotate_ground_right)
        menu.add_command(label="delete", command=self.delete_ground)
        menu.post(event.x_root, event.y_root)

    def change_color(self, new_color):
            self.color = new_color
            self.canvas.itemconfig(self.body1, fill=self.color)
            self.canvas.itemconfig(self.body2, fill=self.color)
            self.canvas.itemconfig(self.body3, fill=self.color)
            self.canvas.itemconfig(self.body4, fill=self.color)

    def rotate_ground_right(self):
        a,b,c,d = self.canvas.coords(self.body4)
        e = a + 10
        f = b
        n1 = [e+15,f,e+45,f]
        n2 = [e+15,f-30,e+15,f+30]
        n3 = [e+7.5,f-20,e+7.5,f+20]
        n4 = [e,f-10,e,f+10]
        self.canvas.coords(self.body1, n1)
        self.canvas.coords(self.body2, n2)
        self.canvas.coords(self.body3, n3)
        self.canvas.coords(self.body4, n4)
        

    def delete_ground(self):
        self.canvas.delete(self.body1)
        self.canvas.delete(self.body2)
        self.canvas.delete(self.body3)
        self.canvas.delete(self.body4)
        ground_list[self.index]=0

#################################################################################################################################################
########################################################--------the wire------------
class Wire_Class:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = []
        self.body = []
        self.m=[]
        self.z=[]
        self.color = None
        self.pin = 0
        self.bin = 0
        self.index = index_list[6]
        index_list[6]+=1
        self.name = str(self.index)
        global z
        
        canvas.bind("<Double-Button-1>", self.get_index)
        canvas.bind("<Button-3>", self.stop)

        #pree and drag
        self.ev()

    def ev(self):
        global z
        for i in range(0, len(self.body)):
            self.canvas.tag_bind(f"wire{self.z[i]}", "<ButtonPress-1>", lambda event, i=i: self.on_press(event, i))
            self.canvas.tag_bind(f"wire{self.z[i]}", "<B1-Motion>", lambda event, i=i: self.on_drag(event, i))
            self.canvas.tag_bind(f"wire{self.z[i]}", "<Button-3>", lambda event, i=i: self.show_context_menu(event, i))

    def get_index(self, event):
        global z
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        a = cx*15
        b = cy*15
        if(self.pin>=2):
            if(abs(a-self.points[self.pin-2])<abs(b-self.points[self.pin-1])):
                a=self.points[self.pin-2]
            else:
                b=self.points[self.pin-1]
        self.points.append(a)
        self.points.append(b)
        self.pin +=2
        self.draw_wire()
    
    def draw_wire(self):
        global z
        m = None
        if(self.pin>=4):
            if((self.points[self.pin-4]==self.points[self.pin-2])and(self.points[self.pin-3]==self.points[self.pin-1])):
                self.bin += 0
            elif(self.points[self.pin-4]==self.points[self.pin-2]):
                m = 1 #رأسي
            elif(self.points[self.pin-3]==self.points[self.pin-1]):
                m = 0 #أفقي
            if(len(self.body)>=1):
                if(m==self.m[self.bin-1]):
                    a,b,c,d=self.canvas.coords(self.body[self.bin-1])
                    self.canvas.coords(self.body[self.bin-1], a,b,self.points[self.pin-2],self.points[self.pin-1])
                else:
                    self.body.append(self.canvas.create_line(self.points[self.pin-4],self.points[self.pin-3],self.points[self.pin-2],self.points[self.pin-1], smooth="false", width=3, fill=self.color, tags=f"wire{z}"))
                    self.m.append(m)
                    self.z.append(z)
                    self.bin += 1
                    z+=1
            else:
                self.body.append(self.canvas.create_line(self.points[self.pin-4],self.points[self.pin-3],self.points[self.pin-2],self.points[self.pin-1], smooth="false", width=3, fill=self.color, tags=f"wire{z}"))
                self.m.append(m)
                self.z.append(z)
                self.bin += 1
                z+=1


    def stop(self, event):
        canvas.unbind("<Double-Button-1>")
        self.ev()

    def on_press(self, event, i):
        global z
        # store the start position 
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.start_x = cx*15
        self.start_y = cy*15

    def on_drag(self, event, i):
        global z
        # the change of position and moving
        y = x = None
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        evx = cx*15
        evy = cy*15
        delta_x = evx - self.start_x
        delta_y = evy - self.start_y
        x = delta_x
        y = delta_y
        if(self.m[i]==0):
            delta_x=0
            self.canvas.move(f"wire{self.z[i]}", delta_x, delta_y)
            a,b,c,d=self.canvas.coords(self.body[i])
            if(i==0):
                if(len(self.body)==1):
                    self.canvas.coords(self.body[i], a+x,b,c-x,d)
                else:
                    e,f,g,h=self.canvas.coords(self.body[i+1])
                    self.canvas.coords(self.body[i+1], c,d,g,h)
                    self.canvas.coords(self.body[i], a+x,b,c,d)

            elif(i==len(self.body)-1):
                e,f,g,h=self.canvas.coords(self.body[i-1])
                self.canvas.coords(self.body[i-1], e,f,a,b)
                self.canvas.coords(self.body[i], a,b,c+x,d)
            elif((i>0)and(i<(len(self.body)-1))):
                e,f,g,h=self.canvas.coords(self.body[i+1])
                self.canvas.coords(self.body[i+1], c,d,g,h)
                j,k,l,m=self.canvas.coords(self.body[i-1])
                self.canvas.coords(self.body[i-1], j,k,a,b)
        else:
            delta_y=0
            self.canvas.move(f"wire{self.z[i]}", delta_x, delta_y)
            a,b,c,d=self.canvas.coords(self.body[i])
            if(i==0):
                if(len(self.body)==1):
                    self.canvas.coords(self.body[i], a,b+y,c,d-y)
                else:
                    e,f,g,h=self.canvas.coords(self.body[i+1])
                    self.canvas.coords(self.body[i+1], c,d,g,h)
                    self.canvas.coords(self.body[i], a,b+y,c,d)
            elif(i==len(self.body)-1):
                e,f,g,h=self.canvas.coords(self.body[i-1])
                self.canvas.coords(self.body[i-1], e,f,a,b)
                self.canvas.coords(self.body[i], a,b,c,d+y)
            elif((i>0)and(i<(len(self.body)-1))):
                e,f,g,h=self.canvas.coords(self.body[i+1])
                self.canvas.coords(self.body[i+1], c,d,g,h)
                j,k,l,m=self.canvas.coords(self.body[i-1])
                self.canvas.coords(self.body[i-1], j,k,a,b)

        # redefine the start position
        self.start_x = evx
        self.start_y = evy

    def show_context_menu(self, event, i):
        global z
        menu = tk.Menu(self.canvas, tearoff=0)
        color_menu = tk.Menu(menu, tearoff=0)
        color_menu.add_command(label="blue", command=lambda: self.change_color("blue"))
        color_menu.add_command(label="red", command=lambda: self.change_color("red"))
        color_menu.add_command(label="yellow", command=lambda: self.change_color("yellow"))
        menu.add_cascade(label="color", menu=color_menu)
        menu.add_command(label="delete", command=self.delete_combo)
        menu.post(event.x_root, event.y_root)

    def change_color(self, new_color):
            global z
            self.color = new_color
            for a in range(0, len(self.body)):
                self.canvas.itemconfig(f"wire{self.z[a]}", fill=self.color)

    def delete_combo(self):
        global z
        for a in range(0, len(self.body)):
            self.canvas.delete(f"wire{self.z[a]}")
        wire_list[self.index]=0
#################################################################################################################################################

def draw_grid(canvas, width, height, spacing):
    # the vertical lines
    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill="lightgray", width=1)

    # the horizontal lines
    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill="lightgray", width=1)

#################################################################################################################################################

def add_resistor(resistor_list):
    resistor_list.append(Resistor_Class(canvas))

def add_capacitor(capacitor_list):
    capacitor_list.append(Capacitor_Class(canvas))

def add_inductance(inductance_list):
    inductance_list.append(Inductance_Class(canvas))

def add_wire(wire_list):
    wire_list.append(Wire_Class(canvas))

def add_acpower(acpower_list):
    acpower_list.append(AC_Power_Class(canvas))

def add_dcpower(dcpower_list):
    dcpower_list.append(DC_Power_Class(canvas))

def add_ground(ground_list):
    ground_list.append(Ground_Class(canvas))
#################################################################################################################################################
    
def run():
    global resistor_list
    global capacitor_list
    global inductance_list
    global wire_list
    global dcpower_list
    global acpower_list
    global ground_list
    global p_l
    global allp
    global p_w
    global points_list
    global index_list
    global pp
    global ccc
    global neg
    global lastl
    global f_d
    global v_l
    global final_list
    global circuit
    global flag
    global dc
    global mx
    global ac
    v_l = {}
    dc = False
    ac = False
    flag = False
    circuit= Circuit('Circuit with CCVS')
    points_list=[]
    final_list = []
    f_d = {}
    for i in range (0, len(wire_list)):
        points = []
        if (wire_list[i]!=0)and(len(wire_list[i].body)==0):
            wire_list[i]==0
        if (wire_list[i] is not None) and (wire_list[i] != 0):
            for a in range (0, len(wire_list[i].body)):
                w,x,y,z=wire_list[i].canvas.coords(wire_list[i].body[a])
                if wire_list[i].m[a] == 0:  # horizontal
                    for b in range (int(min(w,y)), int(max(w,y)+1), 15):
                        v = (b, int(x))
                        if points.count(v) == 0:
                            points.append(v)
                            p_w[v] = []
                        if allp.count(v) == 0:
                            allp.append(v)
                else:  # vertical
                    for b in range (int(min(x,z)), int(max(x,z)+1), 15):
                        v = (int(w), b)
                        if points.count(v) == 0:
                            points.append(v)
                            p_w[v] = []
                        if allp.count(v) == 0:
                            allp.append(v)
        if points != []:
            if(p_l.count(points)==0):
                p_l.append(points)

    
    for i in range (0, len(p_l)):
        for a in range (0, len(p_l[i])):
            if p_w[p_l[i][a]] == []:
                p_w[p_l[i][a]].append(i)
            else:
                if p_w[p_l[i][a]].count(i) == 0:
                    p_w[p_l[i][a]].append(i)
    pp=[]
    neg=[]
    ccc = 0
    lastl=0
    for i in range(0, len(p_l)):
        if(pp.count(i)==0):
            if(len(pp)==0):
                pp.append(i)
            else:
                points_list.append(pp)
                pp=[]
                pp.append(i)
        def goto():
            global resistor_list
            global capacitor_list
            global inductance_list
            global wire_list
            global dcpower_list
            global acpower_list
            global ground_list
            global p_l
            global allp
            global p_w
            global points_list
            global index_list
            global pp
            global ccc
            global neg
            global lastl
            global z
            global flag
            flag = False
            for a in range (0,len(allp)):
                for b in range (0, len(p_w[allp[a]])):
                    if(pp.count(p_w[allp[a]][b])!=0):
                        for c in range (0, len(p_w[allp[a]])):
                            if(pp.count(p_w[allp[a]][c])==0):
                                pp.append(p_w[allp[a]][c])
                    else:
                        ccc += 1
                        if(ccc==len(p_w[allp[a]])):
                            neg.append(a)
        goto()
        while (len(neg)>0):
            lastl=len(neg)
            neg=[]
            goto()
            if(lastl==len(neg)):
                break

    points_list.append(pp)
    for i in range(0, len(points_list)):
        rr=[]
        for a in range (0, len(points_list[i])):
            for b in range (0, len(p_l[points_list[i][a]])):
                if(rr.count(p_l[points_list[i][a]][b])==0):
                    rr.append(p_l[points_list[i][a]][b])
        final_list.append(rr)
    
    for i in range (0,len(final_list)):
        for a in range (0, len(final_list[i])):
            f_d[final_list[i][a]]=i
    #print(final_list)
    #print(f_d)
#############################################################---------------------second_part
    #print(f_d)
            
    for i in range(0, len(dcpower_list)):
        if(dcpower_list[i]!=0):
            dcpower_list[i].coords()
            a=dcpower_list[i].left
            b=dcpower_list[i].right
            #print(a, b)
            if(f_d[b]!=f_d[a]):
                circuit.V(i,f_d[b] , f_d[a], int(dcpower_list[i].value)@u_V)
                flag = True
                dc = True
            else:
                print("Error: voltage source has the same two point")

    for i in range(0, len(acpower_list)):
        if(acpower_list[i]!=0):
            acpower_list[i].coords()
            a=acpower_list[i].left
            b=acpower_list[i].right
            if(f_d[b]!=f_d[a]):
                circuit.SinusoidalVoltageSource(1, b, a,amplitude=int(acpower_list[i].value)@u_V, frequency = 5@u_kHz, offset= 0, delay = 0, damping_factor =0)
                flag = True
                ac = True
            else:
                print("Error: voltage source has the same two point")

    if(flag):
        for i in range(0, len(resistor_list)):
            if(resistor_list[i]!=0):
                resistor_list[i].coords()
                a=resistor_list[i].left
                b=resistor_list[i].right
                #print(a, b)
                circuit.R(i, f_d[b] , f_d[a], int(resistor_list[i].value)@u_Ohm)

        for i in range(0, len(capacitor_list)):
            if(capacitor_list[i]!=0):
                capacitor_list[i].coords()
                a=capacitor_list[i].left
                b=capacitor_list[i].right
                #print(a, b)
                circuit.C(i, f_d[b] , f_d[a], int(capacitor_list[i].value)@u_nF)

        for i in range(0, len(inductance_list)):
            if(inductance_list[i]!=0):
                inductance_list[i].coords()
                a=inductance_list[i].left
                b=inductance_list[i].right
                #print(a, b)
                circuit.L(i, f_d[b] , f_d[a], int(inductance_list[i].value)@u_mH)

        for i in range(0, len(ground_list)):
            if(ground_list[i]!=0):
                ground_list[i].coords()
                a=ground_list[i].point
                #print(a)
                

        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        if (dc):
            analysis = simulator.operating_point()
        elif (ac):
            analysis = simulator.transient(step_time=0.1@u_us, end_time=5*(1/(5@u_kHz)))
            time=np.array(analysis.time)

        v_l[0]=float(0)
        for node in analysis.nodes.values():
            print('Node {}: {:4.1f} V'.format(str(node), float(np.squeeze(node))))
            s =str(node)
            v_l[int(s)]=(float(np.squeeze(node)))

        #print(v_l[f_d[(15,15)]])
            
        #print(v_l)

        for branch in analysis.branches.values():
            print('Branch {}: {:5.2f} A'.format(str(branch), float(np.squeeze(branch))))
            mx=max(mx,abs(float(np.squeeze(branch))))

#################################################################################################################################################
            
class voltage_value:
    def __init__(self,event,canvas):
        dex=event.x
        cx=dex//15
        dey=event.y
        cy=dey//15
        if(dex%15>7):
            cx=cx+1
        if(dey%15>7):
            cy=cy+1
        self.x = cx*15
        self.y = cy*15
        self.canvas = canvas
        self.label = None
        lable_list.append(self)
        #print((self.x, self.y))

        if (self.x, self.y) in f_d :
            a=v_l[f_d[(self.x, self.y)]]
            self.label=tk.Label(canvas,text=f"{a} V",bg="blue",fg="cyan",font=("araial",14))
            self.label.place(x=event.x,y=event.y)

        if self.label is not None:
                self.label.bind("<Button-3>", lambda event: self.del_label())

    def del_label(self):
        #self.canvas.delete(self.label)
        self.label.destroy()
        lable_list.remove(self)

#################################################################################################################################################

root = tk.Tk()
root.title("ECSIM")
root.geometry("{0}x{1}+450+200".format(600, 400))
# root.iconbitmap("project.ico")

canvas = tk.Canvas(root, width=1530, height=780, bg="#FFFAFA")#the color is snow
canvas.pack()

draw_grid(canvas, 1530, 780, 15)

global resistor_list
global lable_list
global capacitor_list
global inductance_list
global wire_list
global dcpower_list
global acpower_list
global ground_list
global p_l
global allp
global p_w
global points_list
global final_list
global f_d
global index_list
global pp
global ccc
global dc
global ac
global neg
global lastl
global mx
global z
global circuit
global flag
global v_l



resistor_list = []
lable_list=[]
capacitor_list= []
inductance_list= []
wire_list = []
dcpower_list = []
acpower_list = []
ground_list = []
final_list = []
f_d = {}
p_l = []
allp = []
p_w = {}
points_list = []
index_list = [0,0,0,0,0,0,0]
z = 0
mx = float(0)

def cc():
    canvas.bind("<Double-Button-1>", lambda event, canvas=canvas: voltage_value(event,canvas))

menu_bar = tk.Menu(root)

# إعداد قائمة الملف
tools_menu = tk.Menu(menu_bar, tearoff=0)
run_menu = tk.Menu(menu_bar, tearoff=0)

tools_menu.add_command(label="Resistor", command=lambda: add_resistor(resistor_list))
tools_menu.add_command(label="Capacitor", command=lambda: add_capacitor(capacitor_list))
tools_menu.add_command(label="Inductance", command=lambda: add_inductance(inductance_list))
tools_menu.add_separator()
tools_menu.add_command(label="DC_power", command=lambda: add_dcpower(dcpower_list))
#tools_menu.add_command(label="AC_power", command=lambda: add_acpower(acpower_list))
tools_menu.add_separator()
tools_menu.add_command(label="Ground", command=lambda: add_ground(ground_list))
tools_menu.add_separator()
tools_menu.add_command(label="Wire", command=lambda: add_wire(wire_list))

run_menu.add_command(label="Run", command=lambda: run())
run_menu.add_separator()
run_menu.add_command(label="Voltage", command=lambda: cc())
#run_menu.add_command(label="Current", command=lambda: run())
#run_menu.add_command(label="Power", command=lambda: run())

# add menu to menu_bar
menu_bar.add_cascade(label="tools", menu=tools_menu)
menu_bar.add_cascade(label="Operations", menu=run_menu)

# setting up the window
root.config(menu=menu_bar)

root.state('zoomed')
root.mainloop()
