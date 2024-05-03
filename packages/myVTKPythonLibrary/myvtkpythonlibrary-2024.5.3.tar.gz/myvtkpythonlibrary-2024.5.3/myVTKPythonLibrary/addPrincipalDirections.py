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

import numpy

import myPythonLibrary    as mypy
import myVTKPythonLibrary as myvtk

########################################################################

def getPrincipalDirections(
        field,
        field_storage="vec",
        remove_Z_component=False,
        verbose=0):

    mypy.my_print(verbose, "*** getPrincipalDirections ***")

    if   (field_storage == "vec"):
        assert (field.GetNumberOfComponents() == 6), "Wrong numpber of components ("+str(field.GetNumberOfComponents())+"). Aborting."
    elif (field_storage == "Cmat"):
        assert (field.GetNumberOfComponents() == 9), "Wrong numpber of components ("+str(field.GetNumberOfComponents())+"). Aborting."
    elif (field_storage == "Fmat"):
        assert (field.GetNumberOfComponents() == 9), "Wrong numpber of components ("+str(field.GetNumberOfComponents())+"). Aborting."
    else:
        assert (0), "Wrong storage (field_storage= "+str(field_storage)+"). Aborting."

    n_tuples = field.GetNumberOfTuples()

    farray_Lmin = myvtk.createFloatArray("Lmin", 1, n_tuples)
    farray_Lmid = myvtk.createFloatArray("Lmid", 1, n_tuples)
    farray_Lmax = myvtk.createFloatArray("Lmax", 1, n_tuples)

    farray_Vmin = myvtk.createFloatArray("Vmin", 3, n_tuples)
    farray_Vmid = myvtk.createFloatArray("Vmid", 3, n_tuples)
    farray_Vmax = myvtk.createFloatArray("Vmax", 3, n_tuples)

    mat = numpy.empty((3,3))
    if (field_storage == "vec"):
        vec = numpy.empty(6)
    elif (field_storage == "Cmat"):
        vec = numpy.empty(9)
    elif (field_storage == "Fmat"):
        vec = numpy.empty(9)
    for k_tuple in range(n_tuples):
        #print("k_tuple: "+str(k_tuple))
        field.GetTuple(k_tuple, vec)
        if (field_storage == "vec"):
            mypy.vec_col6_to_mat_sym33(vec, mat)
        elif (field_storage == "Cmat"):
            mypy.cvec9_to_mat33(vec, mat)
        elif (field_storage == "Fmat"):
            mypy.fvec9_to_mat33(vec, mat)

        if (remove_Z_component):
            mat[2,:] = 0.
            mat[:,2] = 0.

        if (numpy.linalg.norm(mat) > 1e-6):
            #mypy.my_print(verbose-1, "k_tuple = "+str(k_tuple))

            vals, vecs = numpy.linalg.eig(mat)
            #mypy.my_print(verbose-1, "vals = "+str(vals))
            #mypy.my_print(verbose-1, "vecs = "+str(vecs))
            #mypy.my_print(verbose-1, "det = "+str(numpy.linalg.det(vecs)))
            idx = vals.argsort()
            vals = vals[idx]
            vecs = vecs[:,idx]
            #mypy.my_print(verbose-1, "vals = "+str(vals))
            #mypy.my_print(verbose-1, "vecs = "+str(vecs))
            #mypy.my_print(verbose-1, "det = "+str(numpy.linalg.det(vecs)))

            mat_Lmin = vals[0]
            mat_Lmid = vals[1]
            mat_Lmax = vals[2]

            mat_Vmax = vecs[:,2]
            mat_Vmid = vecs[:,1]
            mat_Vmin = numpy.cross(mat_Vmax, mat_Vmid)
        else:
            mat_Lmin = 0.
            mat_Lmid = 0.
            mat_Lmax = 0.
            mat_Vmin = [0.]*3
            mat_Vmid = [0.]*3
            mat_Vmax = [0.]*3

        farray_Lmin.SetTuple1(k_tuple, mat_Lmin)
        farray_Lmid.SetTuple1(k_tuple, mat_Lmid)
        farray_Lmax.SetTuple1(k_tuple, mat_Lmax)
        farray_Vmin.SetTuple(k_tuple, mat_Vmin)
        farray_Vmid.SetTuple(k_tuple, mat_Vmid)
        farray_Vmax.SetTuple(k_tuple, mat_Vmax)

    return (farray_Lmin,
            farray_Lmid,
            farray_Lmax,
            farray_Vmin,
            farray_Vmid,
            farray_Vmax)

########################################################################

def addPrincipalDirections(
        mesh,
        field_name,
        field_support="cell",
        field_storage="vec",
        verbose=1):

    mypy.my_print(verbose, "*** addPrincipalDirections ***")

    assert (field_support in ["point", "cell"]), "\"field_support\" must be \"point\" or \"cell\". Aborting."
    assert (field_storage in ["vec", "Cmat", "Fmat"]), "\"field_storage\" must be \"vec\", \"Cmat\" or \"Fmat\". Aborting."

    if   (field_support == "cell" ): mesh_data = mesh.GetCellData()
    elif (field_support == "point"): mesh_data = mesh.GetPointData()

    field = mesh_data.GetArray(field_name)

    (farray_Lmin,
    farray_Lmid,
    farray_Lmax,
    farray_Vmin,
    farray_Vmid,
    farray_Vmax) = myvtk.getPrincipalDirections(
        field=field,
        field_storage=field_storage,
        verbose=verbose-1)

    farray_Lmin.SetName(field_name+"_Lmin")
    farray_Lmid.SetName(field_name+"_Lmid")
    farray_Lmax.SetName(field_name+"_Lmax")
    farray_Vmin.SetName(field_name+"_Vmin")
    farray_Vmid.SetName(field_name+"_Vmid")
    farray_Vmax.SetName(field_name+"_Vmax")

    mesh_data.AddArray(farray_Lmin)
    mesh_data.AddArray(farray_Lmid)
    mesh_data.AddArray(farray_Lmax)
    mesh_data.AddArray(farray_Vmin)
    mesh_data.AddArray(farray_Vmid)
    mesh_data.AddArray(farray_Vmax)

    return (farray_Lmin,
            farray_Lmid,
            farray_Lmax,
            farray_Vmin,
            farray_Vmid,
            farray_Vmax)
