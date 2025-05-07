import sys

sys.path.insert(1, "../helperScripts")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import moose
from tqdm import tqdm
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.collections import LineCollection
import scikit_posthocs as sp
# import os
# import subprocess
from scipy import signal
import scipy.stats as scs

import expcells
import features as fts
import json

import pickle
import scipy
import MOOSEModel_forgapjunction as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy

import statsmodels.formula.api as smf

gapmodel_imp_list = []
file_path = 'Models_gapjuncfeatures_par_300pA.json'
with open(file_path, "r") as file:
    for line in tqdm(file):
        gapmodel = json.loads(line)
        gapmodel_imp_list.append(gapmodel)

DBLOlist_arg = np.argsort([a["Features"]["DBLO_1.5e-10"] for a in gapmodel_imp_list])
gapmodel_imp_list = np.array(gapmodel_imp_list)[DBLOlist_arg]

rdes1 = mm.generateModel(
    gapmodel_imp_list[-1], CurrInjection=300e-12, vClamp=None, refreshKin=True, syn=False, synwg=0.0, synfq=5
)
rdes1.buildModel(modelPath='/model1')
moose.element( '/library' ).name = 'library1'

rdes2 = mm.generateModel(
    gapmodel_imp_list[-1], CurrInjection=0, vClamp=None, refreshKin=True, syn=False, synwg=0.0, synfq=5
)
rdes2.buildModel(modelPath='/model2')
moose.element( '/library' ).name = 'library2'

gj = moose.GapJunction('model1/gj')
gj.Gk = 1e-6*0.1
moose.connect(gj, 'channel1', moose.element('model1/elec/soma'), 'channel')
moose.connect(gj, 'channel2', moose.element('model2/elec/soma'), 'channel')

####### Set Hsolve ##############
hsolve = moose.HSolve( rdes1.elecid.path + '/hsolve' ) # only one HSolve is needed. HSolve 'finds' model2 through gap juction messages
hsolve.dt = rdes1.elecDt
hsolve.target = rdes1.soma.path
###################################

def doesitspike(Gk):
    gj.Gk = Gk
    print(Gk)
    moose.reinit()
    moose.start(1.5)
    tvec = moose.element("/Graphs/plott").vector
    Vmvec1 = moose.element("/model1/graphs/plot0").vector
    Ivec1 = moose.element("/model1/graphs/plot1").vector
    Vmvec2 = moose.element("/model2/graphs/plot0").vector
    Ivec2 = moose.element("/model2/graphs/plot1").vector
    return [tvec, Vmvec1, Vmvec2]

tvec_gap, Vmvec1_gap, Vmvec2_gap = doesitspike(np.mean([gapmodel_imp_list[-1]["gapjuncfeatures"]["minGk1"], gapmodel_imp_list[-1]["gapjuncfeatures"]["minGk0"]]))

plt.plot(tvec_gap, Vmvec1_gap, label='Vmvec1')
plt.plot(tvec_gap, Vmvec2_gap, label='Vmvec2')
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Membrane potential (V)')
plt.show()

np.savez('Vmvec_gap.npz', tvec_gap=tvec_gap, Vmvec1_gap=Vmvec1_gap, Vmvec2_gap=Vmvec2_gap)