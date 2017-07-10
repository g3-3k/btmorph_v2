"""
File contains:

    - :function:`neuron_from_file`
    - :function:`neurons_from_folder`
    - :function:'get_neuron_path'

Alessio Quaresima added this folder for compatibility with NetGrowwth simulator

Sam Sutton refactored and renamed classes, implemented
    PopulationMorphology and NeuronMorphology
"""
from os import listdir
from os.path import isfile, join
import os, json
import btmorph2
import numpy as np


def get_neuron_path(neuron):
    """
    Return the neurite as an np.array.
    This function works with non branching neuron with one only neurite, elseway
    you got an error

    Returns
    -------
    np.array
    """
    if neuron.no_bifurcations()>0:
        raise Exception("Only non branching neuron can return their path as array!")
    else:
        pathx=[]
        pathy=[]
        for node in neuron.get_tree().get_nodes():
            pathx.append(node.content['p3d'].xyz[0])
            pathy.append(node.content['p3d'].xyz[1])
        return np.array([pathx,pathy])



def tuple_from_files(file_list):
    """
    Return a list of tuple ('filename.json','filename.swc')
    from a list of filenames

    DEPRECATED
    """
    file_list = sorted(file_list)
    tuple_list=[]
    for file_ in file_list:
        tuple_list.append((file_+".json",file_+".swc"))
    return tuple_list

## list all neurons from neurons folder:
def neurons_from_swc(input_file):
    """
    COmpatibility function:
    Btmorph read single neuron .swc files
    Netgrowth write many neurons swc file.

    --> write single neurons .swc from many neurons .swc file
    """

    f = open(input_file, 'r')
    filename = input_file.split(".")[0]

    if not os.path.exists(filename):
        os.makedirs(filename)

    def lines_to_file(neuron, _file):
        w = open(_file,'w')
        for z in neuron:
            w.write(z)

    neuron=[]
    gid = 0
    for line in f:
        if not line.startswith('#') and line.strip():
            # print (line)
            neuron.append(line)
        if not line.strip():
            # print( "write", neuron)
            gid+=1
            lines_to_file(neuron,filename+"/neuron_"+str(gid)+".swc")
            neuron =[]
    if neuron:
        gid+=1
        lines_to_file(neuron,filename+"/neuron_"+str(gid)+".swc")
    return gid

def import_swc(swc_path):
    """
    Import the Neuron Morphology from swc.
    If the file contains more than a neuron and population_to_singles set to
    False creates a PopulationMorphology object,

    Returns
    -------
    a list of bitmorph objects.
    """
    swc_file=swc_path+".swc"
    gids = neurons_from_swc(swc_file)
    neurons=[]
    for gid in range(1,gids+1):
        neurons.append(btmorph2.NeuronMorphology(swc_path+"/neuron_"+str(gid)+".swc"))

    # else:
        # gid = len(listdir(swc_path))
        # if gid >2:
            # neurons = btmorph2.PopulationMorphology(swc_path)
        # else:
            #     return neurons


def neurons_from_folder(folder_path):
    """
    Return a list of btmorph2 neurons for all the neurons in the folder.
    The folder is expected to be a set of .swc and .json files with same name.
    The .json file will contain information on the neurons.
    In case the swc file contain more than a neuron, let'say N,
    it will be splitted in N .swc files inside a folder with same name and path.
    This is done for compatibility with btmorph2.

    Returns
    -------
    [...,btmorph2.NeuronMorphology objects,...]
    """
    neuron_folder =os.getcwd()+"/"+folder_path+"/"
    neuronfiles = [join(neuron_folder,f.split(".")[0]) for f in listdir(neuron_folder) if isfile(join(neuron_folder, f)) and f.endswith(".json")]
    neurons=[]
    for neuron in neuronfiles:
        imported_file, gids = import_swc(neuron)
        netgrowth_format = {"gids":gids,"swc":imported_file,"json":json.load(open(neuron+".json"))}
        print( "importing population from {}".format(neuron))
        print( "This population has {} neurons".format(gids))
        neurons.append(netgrowth_format)
    # neuronfiles = tuple_from_files(neuronfiles)
    return neurons

def neuron_from_file(file_path):
    """
    Get btmorph_v2 object from Netgrowth saved simulation
    Return the btmorph2 NeuronMorphology .swc file, a .json file is expected
    """
    neuron =os.getcwd()+"/"+file_path
    return {"swc":import_swc(neuron),"json":json.load(open(neuron+".json"))}


