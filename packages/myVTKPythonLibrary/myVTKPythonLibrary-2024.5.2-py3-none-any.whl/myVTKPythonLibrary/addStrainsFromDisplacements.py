#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2023                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
########################################################################

import myPythonLibrary    as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def addStrainsFromDisplacements(
        mesh,
        disp_array_name="Displacement",
        defo_grad_array_name="DeformationGradient",
        strain_array_name="Strain",
        mesh_w_local_basis=None,
        compute_principal_directions=False,
        verbose=0):

    mypy.my_print(verbose, "*** addStrainsFromDisplacements ***")

    myvtk.addDeformationGradients(
        mesh=mesh,
        disp_array_name=disp_array_name,
        verbose=verbose-1)
    myvtk.addStrainsFromDeformationGradients(
        mesh=mesh,
        defo_grad_array_name=defo_grad_array_name,
        strain_array_name=strain_array_name,
        mesh_w_local_basis=mesh_w_local_basis,
        compute_principal_directions=compute_principal_directions,
        verbose=verbose-1)
