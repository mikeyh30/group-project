from qsd_gpm.remote_interface import remote_interface
from postprocess import postprocess
from preprocess import preprocess
import os

def changeparamsfile(paramfile, w, t, l, pen, omega, Z, w_mesa, h_mesa, gap_ind):
    f = open(paramfile,'w')
    f.write('w = ' + str(w) + '\n'
        't = ' + str(t) + '\n'
        'l = ' + str(l) + '\n'
        'pen = ' + str(pen) + '\n'
        'omega = ' + str(omega) + '\n'
        'Z = ' + str(Z) + '\n'
        'w_mesa = ' + str(w_mesa) + '\n'
        'h_mesa = ' + str(h_mesa) + '\n'
        'gap_ind = ' + str(gap_ind)
        )
    f.close()

def simulation_wrapper_noparams(host, COMSOL_model, paramfile):
    #Generate GDS file

    #Calculate impedance

    #Preprocessing - calculate current distribution
    current_density_file, paramfile = preprocess(paramfile)
    #COMSOL simulation
    remote_interface(host, COMSOL_model, paramfile, current_density_file)
    #Postprocess - generate g_ens and pi_fidelity
    file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
    g_ens, FWHM = postprocess(file_gens2_number)
    
    return (g_ens, FWHM)

def simulation_wrapper(host, COMSOL_model, paramfile, w, t, l, pen, omega, Z, w_mesa, h_mesa, gap_ind):
    changeparamsfile(paramfile ,w,t,l,pen,omega,Z,w_mesa,h_mesa,gap_ind)
    g_ens, FWHM = simulation_wrapper_noparams(host, COMSOL_model, paramfile)
    return (g_ens, FWHM)

if __name__ == "__main__":
    host = 'monaco'
    COMSOL_model = 'ART_res.mph'
    # paramfile = 'paramlist.txt'
    # current_density_file = "current_density.csv"
    file_gens2 = os.getcwd() + '/downloads/exports/g_ens2.csv'
    file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
    file_N = os.getcwd() + '/downloads/exports/N.csv'
    gens, FWHM = simulation_wrapper_noparams(host, COMSOL_model, "cpw_parameters.txt")
    print(gens)