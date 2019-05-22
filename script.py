import os
os.chdir(r'C:\Users\ok_78\Dropbox\UCLQ Fellowship\Devices\EBL\scripting')
import res_shapes as rs
import gdspy
import numpy as np

#determine parameters
a, c = -1.22074819e-02,   1.51061191e+01
fs = np.linspace(7.15, 7.55, 9)
xs = 1/a*fs - c/a


#setup the folder and gds 'cell'
poly_cell = gdspy.Cell('POLYGONS')
folder = r'C:\Users\ok_78\Dropbox\UCLQ Fellowship\Devices\gavin_spiral_test'


#layer 0 - rectangle showing chip size. Not to be exposed.
chip_w = 5000
chip_h = 5000
poly = gdspy.Polygon(rs.rect(chip_w, chip_h, -2500 , -2500 ), 0)
poly_cell.add(poly)

q = 0
lens = np.append(np.append(np.linspace(6000, 7000, 5), np.linspace(5500, 6000, 2)), np.linspace(7000, 7500, 2))
for i in xs:
    res = rs.gavin_spiral(10, 20, 300, lens[q])
    res = [rs.move(i, -1000  + 1000*(q%3), -1000 + 1000*(q/3)) for i in res]
    for i in res:
        poly_cell.add(gdspy.Polygon(i, 1))
    q+=1


#Write the pattern as a gds file
os.chdir(folder)
gdspy.write_gds('chip_test.gds', unit=1.0e-6, precision=1.0e-9)
# gdspy.LayoutViewer()