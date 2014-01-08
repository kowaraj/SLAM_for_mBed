from math import *

class Robot():
    def __init__(self, ):
        self.adir = 0 # angle [degrees]
        self.meas = 0
        self.move = 0 # lenght [in the dir of 'adir']
        self.moves = [] # logging only (history?)

        self.coords = [0,0] #current coords
        self.radius = 10
        self.arrow = 20
        
    def update(self, msg):
        [move, ddir_dg, meas] = msg
        # robot's message is a triplet of: [move, ddir, meas]
        self.coords = self.calc_pos(move)
        ddir = radians(ddir_dg)
        self.adir = (self.adir + ddir) % 360
        self.meas = meas
        self.moves.append(move)
        return self

    def calc_pos(self, move):
        if move == 0:
            return self.coords
        x = self.coords[0]
        y = self.coords[1]
        self.coords[0] = x + move*cos(self.adir)
        self.coords[1] = y + move*sin(self.adir)
        return self.coords
        
        

        
        
