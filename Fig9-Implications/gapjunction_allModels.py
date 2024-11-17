import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
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

import json

# import pickle
import scipy
import MOOSEModel_multicompt_24_ as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy
from pprint import pprint
import efel

import statsmodels.formula.api as smf
import moose
import pickle

from goMultiprocessing import Multiprocessthis_appendsave

df_expsummaryactiveF = pd.read_pickle("expsummaryactiveF.pkl")

basemodel_imp_list = []
file_path = "activemodels_imp_Eb2_NaTallen.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        if (basemodel["Features"]["AP1_amp_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_amp_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "90th quantile"]):
            basemodel_imp_list.append(basemodel)
        basemodel["gapjuncfeatures"] = {}

DBLOlist_arg = np.argsort([a["Features"]["DBLO_1.5e-10"] for a in basemodel_imp_list])
basemodel_imp_list = np.array(basemodel_imp_list)[DBLOlist_arg]

##################################################################################################################

##############################################################################
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
##############################################################################

def findmin(func, lower_bound=0, upper_bound=100, tolerance=1e-6, **kwags):

    # Find an upper bound where B(upper_bound) becomes True
    while not func(upper_bound, **kwags):
        lower_bound = upper_bound
        upper_bound *= 2

    # Perform binary search to find the minimum x within tolerance
    while upper_bound - lower_bound > tolerance:
        mid_point = (lower_bound + upper_bound) / 2
        if func(mid_point, **kwags):
            upper_bound = mid_point
        else:
            lower_bound = mid_point

    return upper_bound  # or lower_bound, both will be very close

def Gkfunc(Gk, gj, peakidx=0):
    gj.Gk = Gk
    moose.reinit()
    moose.start(1.5)
    tvec = moose.element("/Graphs/plott").vector
    Vmvec1 = moose.element("/model1/graphs/plot0").vector
    Ivec1 = moose.element("/model1/graphs/plot1").vector
    Vmvec2 = moose.element("/model2/graphs/plot0").vector
    Ivec2 = moose.element("/model2/graphs/plot1").vector
    Vm1peaks, Vm1prop = scipy.signal.find_peaks(Vmvec1[(tvec>=0.5) & (tvec<0.6)], prominence=0.001)
    Vm2peaks, Vm2prop = scipy.signal.find_peaks(Vmvec2[(tvec>=0.5) & (tvec<0.6)], prominence=0.001)

    # print(Gk)
    # print(Vm1peaks, Vm2peaks)
    # print(Vm1prop)
    # print(Vm2prop)
    # print('#############################')

    # plt.plot(tvec, Vmvec1)
    # plt.plot(tvec, Vmvec2)
    # plt.show()

    if len(Vm1peaks)==0 or len(Vm2peaks)==0:
        return False

    if Vm2prop['prominences'][peakidx]>0.020:
        return True
    else:
        return False

# def Gkfunc0(Gk):
#     return Gkfunc(Gk, peakidx=0)

# def Gkfunc1(Gk):
#     return Gkfunc(Gk, peakidx=1)

def ourfunc(model):
# for i,model in enumerate(basemodel_imp_list):
    if moose.exists("/model1"):
        moose.delete("/model1")
    if moose.exists("/model2"):
        moose.delete("/model2")
    if moose.exists('/library1'):
        moose.delete('/library1')
    if moose.exists('/library2'):
        moose.delete('/library2')

    rdes1 = mm.generateModel(
        model, CurrInjection=300e-12, vClamp=None, refreshKin=True, syn=False, synwg=0.0, synfq=5
    )
    rdes1.buildModel(modelPath='/model1')
    moose.element( '/library' ).name = 'library1'

    rdes2 = mm.generateModel(
        model, CurrInjection=0, vClamp=None, refreshKin=True, syn=False, synwg=0.0, synfq=5
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

    minGk0 = findmin(Gkfunc, 0.1e-8, 1.5e-8, tolerance=5e-11, gj=gj, peakidx=0)
    model["gapjuncfeatures"]["minGk0"] = minGk0
    minGk1 = findmin(Gkfunc, 0.1e-8, 1.5e-8, tolerance=5e-11, gj=gj, peakidx=1)
    model["gapjuncfeatures"]["minGk1"] = minGk1
    # print(i,minGk0, minGk1)

    # with open('Models_gapjuncfeatures.json', "a") as file:
    #     json.dump(model, file, cls=NpEncoder)
    #     file.write("\n")
    return [model]

Multiprocessthis_appendsave(ourfunc, basemodel_imp_list, [], ['Models_gapjuncfeatures_par.pkl'], seed=123, npool=100)

with open('Models_gapjuncfeatures_par.pkl', "rb") as f, open('Models_gapjuncfeatures_par_300pA.json', "a") as file:
    while True:
        try:
            model = pickle.load(f)
            if len(model) > 0:
                json.dump(model, file, cls=NpEncoder)
                file.write("\n")
        except Exception:
            break


