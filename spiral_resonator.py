import os
directory = os.path.dirname(os.path.abspath(__file__))
ebl = os.path.join(directory,'EBL/')
os.chdir(ebl)
import res_shapes as rs
import gdspy
import subprocess

w_caps = [5,10]       #width of capacitor
w_ins = [5,10]        #width of inductor
l_ins = [100,150]   #length of inductors
gaps = [5,10]      #size of gaps

def spiral_resonator_gds(w_caps, w_ins, l_ins, gaps):
    j = 0
    folder = os.path.join(ebl,'gavin_spiral/')
    #resonator - 3 element list [coarse res elements, fine res elements, stuff to remove from ground plane]
    for w_cap,w_in,l_in,gap in [(w_cap,w_in,l_in,gap) for w_cap in w_caps \
        for w_in in w_ins for l_in in l_ins for gap in gaps]:
        spiral_resonator_gds_helper(w_cap, w_in, l_in, gap,j,folder)
        j = j + 1

def spiral_resonator_gds_helper(w_cap, w_in, l_in, gap,j,folder):
    resonator = rs.TRII(w_cap, w_in, l_in, gap)
    poly_cell = gdspy.Cell('POLYGONS')

    for i in resonator[0]:
        poly_cell.add(gdspy.Polygon(i, 2))
        
    grnd = rs.rect(resonator[2], resonator[3], 0, 0)
    grnd_poly = gdspy.Polygon(grnd, 0)
    
    ps = []
    for i in resonator[1]:
        ps.append(gdspy.Polygon(i, 1))
    for i in ps:
        grnd_poly = gdspy.fast_boolean(grnd_poly, i, 'not', precision=1e-9, max_points=1000, layer=0)
    
        
        
    #Add the ground polygons
    poly_cell.add(grnd_poly)
    
    #Write the pattern as a gds file
    os.chdir(folder)
    gdspy.write_gds('spiral_resonator_{}.gds'.format(j), unit=1.0e-6, precision=1.0e-9)
    gdspy.current_library = gdspy.GdsLibrary()#reset the library to not overlap designs

if __name__ == "__main__":
    spiral_resonator_gds(w_caps,w_ins,l_ins,gaps)
    subprocess.run("klayout ~/Documents/group-project--morton/EBL/gavin_spiral/spiral_resonator_0.gds",
        shell=True, check=True,
        executable='/bin/bash')