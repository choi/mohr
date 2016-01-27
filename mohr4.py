from ttk import Frame, Button, Style
from Tkinter import *
from math import *
import cmath

class Example(Frame):  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title("Mohr Circle Construction")        
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        self.canvas = canvas
        
        ## Input area
        
        self.show_stress = IntVar()
        show_stress_check = Checkbutton(self, text = "Show stress", variable = self.show_stress, command = self.showStress)
        show_stress_check_window = canvas.create_window(100, 420, window=show_stress_check)
        
        reset_rotation = Button(self, text = "Reset rotation", command = self.resetRotation)
        reset_rotation.configure(width = 15, background = "#c0c0c0")
        reset_rotation_window = canvas.create_window(325, 420, window=reset_rotation)
        
        self.sigma_x_val = StringVar()
        self.sigma_y_val = StringVar()
        self.tau_xy_val = StringVar()
        self.theta_val = StringVar()
        sigma_x = Entry(textvariable=self.sigma_x_val)
        sigma_y = Entry(textvariable=self.sigma_y_val)
        tau_xy = Entry(textvariable=self.tau_xy_val)
        theta = Entry(textvariable=self.theta_val)
        sigma_x_window = canvas.create_window(125, 480, window=sigma_x)
        sigma_y_window = canvas.create_window(125, 510, window=sigma_y)
        tau_xy_window = canvas.create_window(125, 540, window=tau_xy)
        theta_window = canvas.create_window(125, 570, window=theta)
        canvas.create_text(30, 480, anchor=W, text=u"\u03c3")
        canvas.create_text(37, 485, anchor=W, text="x")
        canvas.create_text(30, 510, anchor=W, text=u"\u03c3")
        canvas.create_text(37, 515, anchor=W, text="y")
        canvas.create_text(30, 540, anchor=W, text=u"\u03c4")
        canvas.create_text(37, 545, anchor=W, text="xy")
        canvas.create_text(30, 570, anchor=W, text=u"\u03b8")
        
        calculate = Button(self, text = "Calculate", command = self.calculate)
        calculate.configure(width = 15, background = "#c0c0c0")
        calculate_window = canvas.create_window(325, 480, window=calculate)
        
        self.sigma_x_prime_val = StringVar()
        sigma_x_prime = Entry(textvariable=self.sigma_x_prime_val)
        sigma_x_prime_window = canvas.create_window(325, 510, window=sigma_x_prime)
        canvas.create_text(230, 510, anchor=W, text=u"\u03c3")
        canvas.create_text(237, 515, anchor=W, text="x'")
        
        self.sigma_y_prime_val = StringVar()
        sigma_y_prime = Entry(textvariable=self.sigma_y_prime_val)
        sigma_y_prime_window = canvas.create_window(325, 540, window=sigma_y_prime)
        canvas.create_text(230, 540, anchor=W, text=u"\u03c3")
        canvas.create_text(237, 545, anchor=W, text="y'")
        
        self.tau_xy_prime_val = StringVar()
        tau_xy_prime = Entry(textvariable=self.tau_xy_prime_val)
        tau_xy_prime_window = canvas.create_window(325, 570, window=tau_xy_prime)
        canvas.create_text(230, 570, anchor=W, text=u"\u03c4")
        canvas.create_text(237, 575, anchor=W, text="x'y'")
        
        canvas.create_text(75, 450, anchor=W, text="Definition of stress")               
        
        
        ## Stress square graph
        
        self.square = canvas.create_rectangle(120,100,320,300)
        self.rotated = False
        self.lines = [None, None, None, None, None, None, None, None]
        
        ## Mohr Circle graph

        self.graph = Canvas(self)
        self.graph.config(width = 418, height = 418, bg = "#fff", highlightbackground = "#fff", relief = GROOVE, bd = 3)
        self.graph.yaxis = self.graph.create_line(210, 420, 210, 0)
        self.graph.xaxis = self.graph.create_line(-1000, 210, 1010, 210)
        self.mohr = None
        self.pline = None
        self.pointtext = None
        graph_window = canvas.create_window(448, 23, window = self.graph, anchor = NW)
        self.graph.scale = 1
        
        ## Operation of Mohr's circle
        
        self.show_principal_stress = IntVar()
        show_principal_stress_check = Checkbutton(self, text = "Show principal stress", variable = self.show_principal_stress, command = self.showPrincipalStress)
        show_principal_stress_check_window = canvas.create_window(550, 510, window=show_principal_stress_check)
        
        left = Button(self, text = "Left", command = self.left)
        left.configure(width = 10, background = "#c0c0c0")
        left_window = canvas.create_window(490, 480, window=left)
        zoomin = Button(self, text = "Zoom in", command = self.zoomin)
        zoomin.configure(width = 10, background = "#c0c0c0")
        zoomin_window = canvas.create_window(575, 480, window=zoomin)
        zoomout = Button(self, text = "Zoom out", command = self.zoomout)
        zoomout.configure(width = 10, background = "#c0c0c0")
        zoomout_window = canvas.create_window(660, 480, window=zoomout)
        right = Button(self, text = "Right", command = self.right)
        right.configure(width = 10, background = "#c0c0c0")
        right_window = canvas.create_window(745, 480, window=right)
        reset = Button(self, text = "Reset", command = self.original)
        reset.configure(width = 10, background = "#c0c0c0")
        reset_window = canvas.create_window(830, 480, window=reset)

        self.radio_val = IntVar()
        self.radio_val.set(1)
        theta_input = Radiobutton(self, text = "", variable = self.radio_val, value = 1, command = self.calculate)
        theta_p = Radiobutton(self, text = "", variable = self.radio_val, value = 2, command = self.calculate)
        theta_s = Radiobutton(self, text = "", variable = self.radio_val, value = 3, command = self.calculate)
        theta_input_window = canvas.create_window(710, 510, window=theta_input, anchor = W)
        theta_p_window = canvas.create_window(710, 540, window=theta_p, anchor = W)
        canvas.create_text(738, 510, anchor=W, text="User Input")        
        canvas.create_text(738, 540, anchor=W, text=u"\u03b8")        
        canvas.create_text(745, 545, anchor=W, text="p")
        theta_s_window = canvas.create_window(710, 570, window=theta_s, anchor = W)
        canvas.create_text(738, 570, anchor=W, text=u"\u03b8")        
        canvas.create_text(745, 575, anchor=W, text="s")
        
        
        canvas.pack(fill=BOTH, expand=1)

    def resetRotation(self):        
        self.theta_val.set("0")
        self.canvas.delete(self.square)
        self.square = self.canvas.create_rectangle(120,100,320,300)
        self.rotated = False
        if self.show_stress.get() == 1:
            for i in self.lines:
                self.canvas.delete(i)
        self.showStress()
        
    def calculate(self):
        s_x = float(self.sigma_x_val.get())
        s_y = float(self.sigma_y_val.get())
        t_xy = float(self.tau_xy_val.get())
        
        self.sigma_avg = ((s_x + s_y) / 2)
        self.tau_max = ((s_x - s_y) ** 2 / 4 + t_xy ** 2) ** .5
        if s_x != s_y:
            self.theta_p = degrees(atan(2 * t_xy / (s_x - s_y)) / 2)
        else:
            self.theta_p = 45
        if t_xy != 0:
            self.theta_s = -degrees(atan((s_x - s_y) / 2 / t_xy) / 2)
        else:
            self.theta_s = -45
        
        if self.theta_val.get() == "":
            self.theta_val.set(str(self.theta_p))
            self.radio_val.set(2)
        elif self.radio_val.get() == 2:
            self.theta_val.set(str(self.theta_p))
        elif self.radio_val.get() == 3:
            self.theta_val.set(str(self.theta_s))
        
        self.sigma_x_prime_val.set(self.sigma_avg + (s_x - s_y) * cos(float(self.theta_val.get()) * pi / 90) / 2 + t_xy * sin(float(self.theta_val.get()) * pi / 90))
        self.sigma_y_prime_val.set(self.sigma_avg - (s_x - s_y) * cos(float(self.theta_val.get()) * pi / 90) / 2 - t_xy * sin(float(self.theta_val.get()) * pi / 90))
        self.tau_xy_prime_val.set(-(s_x - s_y) * sin(float(self.theta_val.get()) * pi / 90) / 2 + t_xy * cos(float(self.theta_val.get()) * pi / 90))        
        
        ## Mohr Circle graph
        
        _s_x = s_x * self.graph.scale
        _s_y = s_y * self.graph.scale
        _t_xy = t_xy * self.graph.scale
        self._sigma_avg = self.sigma_avg * self.graph.scale
        self._tau_max = self.tau_max * self.graph.scale
        
        if self.mohr != None:
            self.graph.delete(self.mohr)
        self.mohr = self.graph.create_oval(int(self._sigma_avg - self._tau_max)+210,int(self._tau_max)+210,int(self._sigma_avg + self._tau_max)+210,210-int(self._tau_max))
            
        if self.pline != None:
            self.graph.delete(self.pline)
        self.pline = self.graph.create_line(int(210+_s_x), int(210+_t_xy), int(2*self._sigma_avg+210-_s_x), int(210-_t_xy))
        
        if self.pointtext == None:
            if _s_x < 0:
                if _t_xy < 0:
                    orientation = SE
                else:
                    orientation = NE
            else:
                if _t_xy < 0:
                    orientation = SW
                else:
                    orientation = NW
            self.pointtext = self.graph.create_text(int(_s_x)+210, int(_t_xy)+210, anchor=orientation, text="(%.1f, %.1f)" % (s_x, t_xy))
        else:
            self.graph.delete(self.pointtext)
            if _s_x < 0:
                if _t_xy < 0:
                    orientation = SE
                else:
                    orientation = NE
            else:
                if _t_xy < 0:
                    orientation = SW
                else:
                    orientation = NW
            self.pointtext = self.graph.create_text(int(_s_x)+210, int(_t_xy)+210, anchor=orientation, text="(%.1f, %.1f)" % (s_x, t_xy))
        
        ## Stress square graph
        
        coordinates = [(120, 100), (120, 300), (320, 300), (320, 100)]
        points = []
        
        cangle = cmath.exp(-float(self.theta_val.get())*1j*pi/180) 
        center = complex(220, 200)
        for x, y in coordinates:
            v = cangle * (complex(x, y) - center) + center
            points += [int(v.real), int(v.imag)]
        
        self.canvas.delete(self.square)
        self.rotated = True
        
        self.square = self.canvas.create_polygon(points, fill = "#fff", outline = "#000")
        
        if self.show_principal_stress.get() == 1:
            self.graph.delete(self.spstext1)
            self.graph.delete(self.spstext2)
            self.showPrincipalStress()
        if self.show_stress.get() == 1:
            for i in self.lines:
                self.canvas.delete(i)
            self.showStress()
    
    def showStress(self):
        if self.show_stress.get() == 1:
            if self.rotated:
                xdir, ydir, tdir = None, None, None
                s_x_prime = self.sigma_x_prime_val.get()
                s_y_prime = self.sigma_y_prime_val.get()
                t_xy_prime = self.tau_xy_prime_val.get()
                if s_x_prime == "" or float(s_x_prime) == 0:
                    pass
                elif float(s_x_prime) > 0:
                    xdir = FIRST
                else:
                    xdir = LAST
                    
                if s_y_prime == "" or float(s_y_prime) == 0:
                    pass
                elif float(s_y_prime) > 0:
                    ydir = FIRST
                else:
                    ydir = LAST
                    
                if t_xy_prime == "" or float(t_xy_prime) == 0:
                    pass
                elif float(t_xy_prime) > 0:
                    tdir = FIRST
                else:
                    tdir = LAST
                
                coordinates = [(220, 30), (220, 100), (220, 370), (220, 300), (50, 200), (120, 200), (390, 200), (320, 200), (245, 75), (195, 75), (195, 325), (245, 325), (345, 175), (345, 225), (95, 225), (95, 175)]
                points = []
        
                cangle = cmath.exp(-float(self.theta_val.get())*1j*pi/180) 
                center = complex(220, 200)
                for x, y in coordinates:
                    v = cangle * (complex(x, y) - center) + center
                    points = [int(v.imag), int(v.real)] + points
                
                
                if ydir:
                    self.lines[0] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = ydir)
                    self.lines[1] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = ydir)
                else:
                    points = points[8:]
                if xdir:
                    self.lines[2] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = xdir)
                    self.lines[3] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = xdir)
                else:
                    points = points[8:]
                if tdir:
                    self.lines[4] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = tdir)
                    self.lines[5] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = tdir)
                    self.lines[6] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = tdir)
                    self.lines[7] = self.canvas.create_line(points.pop(), points.pop(), points.pop(), points.pop(), arrow = tdir)
                else:
                    points = points[8:]
            else:
                xdir, ydir, tdir = None, None, None
                s_x = self.sigma_x_val.get()
                s_y = self.sigma_y_val.get()
                t_xy = self.tau_xy_val.get()
                if s_x == "" or float(s_x) == 0:
                    pass
                elif float(s_x) > 0:
                    xdir = FIRST
                else:
                    xdir = LAST
                    
                if s_y == "" or float(s_y) == 0:
                    pass
                elif float(s_y) > 0:
                    ydir = FIRST
                else:
                    ydir = LAST
                    
                if t_xy == "" or float(t_xy) == 0:
                    pass
                elif float(t_xy) > 0:
                    tdir = FIRST
                else:
                    tdir = LAST
                    
                if ydir:
                    self.lines[0] = self.canvas.create_line(220, 30, 220, 100, arrow = ydir)
                    self.lines[1] = self.canvas.create_line(220, 370, 220, 300, arrow = ydir)
                if xdir:
                    self.lines[2] = self.canvas.create_line(50, 200, 120, 200, arrow = xdir)
                    self.lines[3] = self.canvas.create_line(390, 200, 320, 200, arrow = xdir)
                if tdir:
                    self.lines[4] = self.canvas.create_line(245, 75, 195, 75, arrow = tdir)
                    self.lines[5] = self.canvas.create_line(195, 325, 245, 325, arrow = tdir)
                    self.lines[6] = self.canvas.create_line(345, 175, 345, 225, arrow = tdir)
                    self.lines[7] = self.canvas.create_line(95, 225, 95, 175, arrow = tdir)
        else:
            for i in self.lines:
                if i != None:
                    self.canvas.delete(i)
                    i = None
            
    def zoomin(self):
        self.graph.scale *= 1.5
        self.calculate()
        if self.show_principal_stress.get() == 1:
            self.graph.delete(self.spstext1)
            self.graph.delete(self.spstext2)
            self.showPrincipalStress()
    
    def zoomout(self):
        self.graph.scale /= 1.5
        self.calculate()
    
    def left(self):
        self.graph.xview_scroll(-1, UNITS)

    def right(self):
        self.graph.xview_scroll(1, UNITS)
    
    def original(self):
        self.graph.xview_moveto(0)
        self.graph.scale = 1
        self.calculate()
    
    def showPrincipalStress(self):
        if self.show_principal_stress.get() == 1 :
            self.spstext1 = self.graph.create_text(int(self._sigma_avg - self._tau_max)+200, 220, anchor=E, text="(%.1f, %.1f)" % (self.sigma_avg - self.tau_max,0))
            self.spstext2 = self.graph.create_text(int(self._sigma_avg + self._tau_max)+220, 220, anchor=W, text="(%.1f, %.1f)" % (self.sigma_avg + self.tau_max,0))
        else:
            self.graph.delete(self.spstext1)
            self.graph.delete(self.spstext2)
    
def main():
    root = Tk()
    ex = Example(root)
    root.geometry("900x600+50+50")
    root.mainloop()  

if __name__ == '__main__':
    main()  