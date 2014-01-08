import time
import serial
import sys
import microterm
from microterm import Microterm
from microterm import console

from robot import *
import slam_display

class Slam():

    def __init__(self):
        self.buf = ""
        self.robot = Robot()
        self.enabled = False

    def cbf(self, data):
        if data == "":
            pass
        elif data == "\r":
            self.upd_dm(self.buf)
            print "completed!, sent buf = ", self.buf
            self.buf = ""

        else:
            self.buf += data
            #print "\ncbf's buf= ",  self.buf

    def upd_dm(self, buf):
        msg = self.parse_robot_msg(buf)
        if msg[2] == 0:
            print "wrong measurement, skip update"
            return
        self.robot = self.robot.update(msg)
        self.dm.update(self.robot)
        
    def parse_robot_msg(self, buf):
        print "parse_coords_buf = ", buf
        try:
            msg = [int(x) for x in buf.split(",")]
        except ValueError, e:
            print "wrong robot msg detected"
            return [0,0,0]
        print "parse_coords_buf: parsed is= ", msg
        return msg
        
    def run(self):
        #port = "/dev/tty.usbmodem1411"
        port = "/dev/ptyp0" # on macOS it's paired with "screen /dev/ttyp0"
        try:
            microterm = Microterm(self.cbf, port, 9600, "N", False, False)
        except serial.SerialException, e:
            sys.stderr.write("could not open port %r: %s\n" % (port, e))
            sys.exit(1)
            
        console.setup()
        sys.stderr.write("\nStarting terminal on port: "+port+"\n")
        sys.stderr.write("commands:\n")
        sys.stderr.write(" enable reader: 1\n")
        sys.stderr.write(" disable reader: 2\n")
        
        microterm.start()
        sys.stderr.write("\n--main displaying loop--\n")
    
        self.dm = slam_display.DisplayMap()
        self.dm.mainloop()

        sys.stderr.write("\n--join term--\n")
        try:
            microterm.join(True)
        except KeyboardInterrupt:
            pass

        sys.stderr.write("\n--- exit ---\n")
        microterm.join()
        #~ console.cleanup()


def main():
    s = Slam()
    s.run()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
    
        
