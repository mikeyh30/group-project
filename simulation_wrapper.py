import qsd.tests.remote_interface as remote_interface

def simulation_wrapper(host, COMSOL_model, paramfile):
    #Generate GDS file

    #Calculate impedance

    #Preprocessing - calculate current distribution

    #COMSOL simulation
    remote_interface(host, COMSOL_model, paramfile)
    #Postprocess - generate g_ens and pi_fidelity
    g_ens, pi_fidelity = postprocess()
    
    return (g_ens, pi_fidelity)

if __name__ == "__main__":
    host = 'cork'
    COMSOL_model = 'cpw_vacuum_calcs.mph'
    paramfile = 'paramlist.txt'
    simulation_wrapper(host, COMSOL_model, paramfile)