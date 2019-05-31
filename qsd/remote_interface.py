#!/usr/bin/env python
from qsd.ssh_control import sshcommand

def remote_interface(host,COMSOL_model,paramfile_1):
    sshc = sshcommand.SSHCommand(host,model=COMSOL_model,paramfile=paramfile_1)

    # Securely copy the parameter list to remote machine
    #sshc.scp_params() 

    # Ensure that the remote machine has the folder structure
    sshc.check_host_machine()

    # Copy the parameter file to correct directory
    sshc.set_comsol_data()

    sshc.upload_job_script()

    # Run COMSOL on remote machine
    sshc.run_comsol()

    # Download data from remote machine
    sshc.get_comsol_data(host)

if __name__ == "__main__":
    remote_interface('monaco','ART_res.mph','paramlist.txt')