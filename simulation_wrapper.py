import qsd.tests.remote_interface as remote_interface
import postprocess.postprocess as postprocess

def simulation_wrapper(host, COMSOL_model, paramfile):
    #Generate GDS file

    #Calculate impedance

    #Preprocessing - calculate current distribution

    #COMSOL simulation
    remote_interface(host, COMSOL_model, paramfile, current_density_file)
    #Postprocess - generate g_ens and pi_fidelity
    g_ens, FWHM = postprocess(file_gens2_number)
    
    return (g_ens, FWHM)

if __name__ == "__main__":
    host = 'monaco'
    COMSOL_model = 'cpw_vacuum_calcs.mph'
    paramfile = 'paramlist.txt'
    current_density_file = "current_density.csv"
    file_gens2 = os.getcwd() + '/qsd/downloads/exports/g_ens2.csv'
    file_gens2_number = os.getcwd() + '/qsd/downloads/exports/g_ens2_number.csv'
    file_N = os.getcwd() + '/qsd/downloads/exports/N.csv'
    simulation_wrapper(host, COMSOL_model, paramfile)