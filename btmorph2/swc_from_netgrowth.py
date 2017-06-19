"""
File contains:

    - :function:`neuron_from_file`
    - :function:`neurons_from_folder`

Alessio Quaresima added this folder for compatibility with NetGrowwth simulator

Sam Sutton refactored and renamed classes, implemented
    PopulationMorphology and NeuronMorphology
"""
from os import listdir
from os.path import isfile, join
import os, json
import btmorph2

def tuple_from_files(file_list):
    """
    Return a list of tuple ('filename.json','filename.swc')
    from a list of filenames
    """
    file_list = sorted(file_list)
    tuple_list=[]
    for file_ in file_list:
        tuple_list.append((file_+".json",file_+".swc"))
    return tuple_list

## list all neurons from neurons folder:
def neurons_from_swc(input_file):
    """
    To keep compatibility with btmorph write single neurons .swc
    from many neurons .swc file
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
    Import the Neuron Morphology from Swc, if the file contains more than a neuron
    creates a PopulationMorphology object, a NeuronMorphology other way.

    Returns
    -------
    The btmorph2 file relative to swc_path
    """
    print( "importing neuron from {}".format(swc_path))
    swc_file=swc_path+".swc"
    gid = neurons_from_swc(swc_file)
    if gid >1:
        neurons = btmorph2.PopulationMorphology(swc_path)
    else:
        neurons = btmorph2.NeuronMorphology(swc_path+"/neuron_1.swc")
    # else:
        # gid = len(listdir(swc_path))
        # if gid >2:
            # neurons = btmorph2.PopulationMorphology(swc_path)
        # else:
            # neurons = btmorph2.NeuronMorphology(swc_path+"/neuron_1.swc")
    return neurons


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
    neuronfiles = [join(neuron_folder,f.split(".")[0]) for f in listdir(neuron_folder) if isfile(join(neuron_folder, f)) and f.split(".")[1]=="json"]
    neurons=[]
    for neuron in neuronfiles:
        neurons.append({"swc":import_swc(neuron),"json":json.load(open(neuron+".json"))})
    # neuronfiles = tuple_from_files(neuronfiles)
    return neurons

def neurons_from_file(file_path):
    """
    Return the btmorph2 neuron morphology from a single neuron .swc file, a .json file is expected
    """
    neuron =os.getcwd()+"/"+file_path
    return {"swc":import_swc(neuron),"json":json.load(open(neuron+".json"))}


