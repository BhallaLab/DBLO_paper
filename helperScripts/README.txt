expcells.py - Utility script to handle experimental data
MOOSEModel.py - Utility script to handle models defined for MOOSE
features.py - Utility script to calculate electrophysiological features

rdesigneur_forgapjunction.py - Utility script. Modification to MOOSE code to allow gap junctions. Needed for Fig9
MOOSEModel_forgapjunction.py - Utility script. Same as MOOSEModel.py but slight modifications necessary for gap junctions

getballnstickpas.py - Generates subthreshold pas models in the following files:
    pas.json
getballnstickimp.py - Generates subthreshold imp models in the following files:
    imp.json
get1compt.py - Generates subthreshold 1compt models in the following files:
    1compt.json
getactivemodels.py - Generates active pas,imp,1compt triplets in the following files:
    activemodels_pas_.json
    activemodels_1compt_.json
    activemodels_imp_.json
filteractivemodels.py - Script to remove pas,imp,1compt triplets with invalid AP height. Generates the following files:
    activemodels_pas.json
    activemodels_1compt.json
    activemodels_imp.json

expfeatures_as_pklcsv.py - Script to calculate and store features of experimental recordings. Generates the following files:
    exppasF.pkl
    expsummaryactiveF.csv
    expsummaryactiveF.pkl
    expactiveF.csv
    expactiveF.pkl
    expchirp.csv
    expchirp.pkl
    exppasF.csv

plots_1compt/ - Contains plots that show how well the 13 subthreshold 1compt models fit to their corresponding neuron's experimental data
plots_pas/ - Contains plots that show how well the 13x10=130 subthreshold pas models fit to their corresponding neuron's experimental data
plots_imp/ - Contains plots that show how well the 13 subthreshold imp models fit to their corresponding neuron's experimental data
