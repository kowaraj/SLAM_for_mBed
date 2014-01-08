from math import *
from Tkinter import *
from robot import *

#***************************************

class World():
    def __init__(self, w, h):
        self.width = w
        self.height = h
        
class DisplayMap(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.p = []
        self.p.append([0,0])
        
        # Drawing
        self.can = DisplayObjects ()
        self.can.configure(bg ='ivory', bd =2, relief=SUNKEN)
        self.can.pack(side =TOP, padx =5, pady =5)
        self.can.draw_all(self.p, Robot())

    def update(self, r):
        print "dm's update called"
        obs_coords = self.get_obstacle(r)
        self.p.append(obs_coords)
        self.can.draw_all(self.p, r)

    def get_obstacle(self, r):
        x0 = r.coords[0]
        y0 = r.coords[1]
        a = r.adir
        m = r.meas
        x1 = x0 + m*cos(a)
        y1 = y0 + m*sin(a)
        obs_coords = [int(x1), int(y1)]
        return obs_coords
        
class DisplayObjects(Canvas):

    def __init__(self):
        Canvas.__init__(self)
        self.world = World(400,400)
        # central cross
        self.xc = self.world.height/2
        self.yc = self.world.width/2
        self.lc = 100
        # obstacles' parameters
        self.obst_radius = 3
        #
        self.configure(width=self.world.width, height=self.world.height)
        
    def yi(self, y):
        return self.world.height - y
        
    def draw_all(self, p, r):
        self.configure(bg ='ivory', bd =2, relief=SUNKEN)
        self.delete(ALL)
        self.p = p
        #plotting
        self.plot_world()
        self.plot_obstacles(p)
        self.plot_robot(r)
        
    def plot_robot(self, r):
        x0 = self.xc + r.coords[0]
        y0 = self.yc + r.coords[1]
        a = r.adir
        l = r.arrow
        rad = r.radius
        x1 = x0 + l*cos(a)
        y1 = y0 + l*sin(a)
        self.create_oval(x0-rad, self.yi(y0-rad), x0+rad, self.yi(y0+rad), fill = "gray")
        self.create_line(x0, self.yi(y0), x1, self.yi(y1), fill = "gray", width = 3)

    def plot_world(self):
        self.create_line(self.xc-self.lc, self.yi(self.yc), self.xc+self.lc, self.yi(self.yc), fill="red")
        self.create_line(self.xc, self.yi(self.yc-self.lc), self.xc, self.yi(self.yc+self.lc), fill="red")

    def plot_obstacles(self, ps):
        print ps
        for p in ps:
            radius = self.obst_radius
            px = p[0]
            py = p[1]
            x0 = self.xc + (px - radius)
            y0 = self.yc + (py - radius)
            x1 = self.xc + (px + radius)
            y1 = self.yc + (py + radius)
            self.create_oval(x0, self.yi(y0), x1, self.yi(y1), fill = "blue")





        
