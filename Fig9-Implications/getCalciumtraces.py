#### Here we store the result of Calcium traces to calculate median ca conc during 300 pA AP train

import os

os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4

import sys

sys.path.insert(1, "../helperScripts")

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
import MOOSEModel_multicompt_24_Ca as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy
from pprint import pprint
import efel

import statsmodels.formula.api as smf
import moose
import pickle

from goMultiprocessing import Multiprocessthis_appendsave

df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

basemodel_imp_list = []
file_path = "activemodels_imp_Eb2_NaTallen.json"
modelid=0 #Our parallelization is asynchronous. This helps with the ordering
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodel["Parameters"]["Channels"]["K_DR_Chan"]["Kinetics"] = basemodel["Parameters"]["Channels"]["K_DR_Chan"]["Kinetics"]
        basemodel["Parameters"]["Channels"]["Na_T_Chan"]["Kinetics"] = basemodel["Parameters"]["Channels"]["Na_T_Chan"]["Kinetics"]
        basemodel["Parameters"]["Channels"]["h_Chan"]["Kinetics"] = basemodel["Parameters"]["Channels"]["h_Chan"]["Kinetics"]
        if (basemodel["Features"]["AP1_amp_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_amp_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "90th quantile"]):
            basemodel['modelid'] = modelid
            modelid += 1
            basemodel_imp_list.append(basemodel)

##################################################################################################################

# for i,model in enumerate(basemodel_imp_list):
def ourfunc_helper(model, refreshKin, Gbarfactor_CaL=1, Gbarfactor_CaN=1e-5, Gbarfactor_CaR=1e-5, Gbarfactor_CaT=1e-5):
    # i=i_model[0]
    # model=i_model[1]
    # # print(i)
    sm_area = 2*np.pi*model["Parameters"]["Morphology"]['sm_len']*model["Parameters"]["Morphology"]['sm_diam']
    model["Parameters"]["Ca_Conc"] = {
                "Ca_B": 0.02591067*100/(sm_area), #3.67e6
                "Ca_tau": 80e-3,
                "Ca_base": 1e-4,
                "Kinetics": "../Kinetics/Ca_Conc_Common1",
            }
    model["Parameters"]["Channels"]["Ca_L_Chan"] = {
                    "Gbar": 8.040874125061715e-11*Gbarfactor_CaL,
                    "Erev": 0.140,
                    "Kinetics": "../Kinetics/Ca_L_Chan_Migliore2018",
                }
    model["Parameters"]["Channels"]["Ca_N_Chan"] = {
                    "Gbar": 3.752801006907419e-11*Gbarfactor_CaN,
                    "Erev": 0.140,
                    "Kinetics": "../Kinetics/Ca_N_Chan_Migliore2018",
                }
    model["Parameters"]["Channels"]["Ca_R_Chan"] = {
                    "Gbar": 3.195687109173425e-10*Gbarfactor_CaR,
                    "Erev": 0.140,
                    "Kinetics": "../Kinetics/Ca_R_Chan_Upchurch2022",
                }
    model["Parameters"]["Channels"]["Ca_T_Chan"] = {
                    "Gbar": 8.105502056278108e-12*Gbarfactor_CaT,
                    "Erev": 0.140,
                    "Kinetics": "../Kinetics/Ca_T_Chan_Migliore2018",
                }

    tvec, Vmvec, Cavec, I_Ca_L_Chan_vec, I_Ca_N_Chan_vec, I_Ca_R_Chan_vec, I_Ca_T_Chan_vec = mm.runModel(model, refreshKin=refreshKin)
    # np.save(f'modeloutput/{i}.pkl', [tvec, Vmvec, Cavec, I_Ca_L_Chan_vec, I_Ca_N_Chan_vec, I_Ca_R_Chan_vec, I_Ca_T_Chan_vec])
    return [model['modelid'], tvec, Vmvec, Cavec, I_Ca_L_Chan_vec, I_Ca_N_Chan_vec, I_Ca_R_Chan_vec, I_Ca_T_Chan_vec]

# for Cachan in ['CaL', 'CaN', 'CaR', 'CaT']:
#     if Cachan=='CaL':
#         def ourfunc(model):
#             return ourfunc_helper(model, refreshKin=False, Gbarfactor_CaL=1, Gbarfactor_CaN=1e-5, Gbarfactor_CaR=1e-5, Gbarfactor_CaT=1e-5)
#     elif Cachan=='CaN':
#         def ourfunc(model):
#             return ourfunc_helper(model, refreshKin=False, Gbarfactor_CaL=1e-5, Gbarfactor_CaN=1, Gbarfactor_CaR=1e-5, Gbarfactor_CaT=1e-5)
#     elif Cachan=='CaR':
#         def ourfunc(model):
#             return ourfunc_helper(model, refreshKin=False, Gbarfactor_CaL=1e-5, Gbarfactor_CaN=1e-5, Gbarfactor_CaR=1, Gbarfactor_CaT=1e-5)
#     elif Cachan=='CaT':
#         def ourfunc(model):
#             return ourfunc_helper(model, refreshKin=False, Gbarfactor_CaL=1e-5, Gbarfactor_CaN=1e-5, Gbarfactor_CaR=1e-5, Gbarfactor_CaT=1)

#     i, tvec, Vmvec, Cavec, I_Ca_L_Chan_vec, I_Ca_N_Chan_vec, I_Ca_R_Chan_vec, I_Ca_T_Chan_vec = ourfunc_helper(basemodel_imp_list[0], refreshKin=True)

#     Multiprocessthis_appendsave(ourfunc, basemodel_imp_list, [], [f'{Cachan}/i.pkl', f'{Cachan}/tvec.pkl', f'{Cachan}/Vmvec.pkl', f'{Cachan}/Cavec.pkl', f'{Cachan}/I_Ca_L_Chan_vec.pkl', f'{Cachan}/I_Ca_N_Chan_vec.pkl', f'{Cachan}/I_Ca_R_Chan_vec.pkl', f'{Cachan}/I_Ca_T_Chan_vec.pkl'], seed=123, npool=100)


for ii,Cachan in enumerate(['CaL', 'CaN', 'CaR', 'CaT']):
    i_list = []
    with open(f'{Cachan}/i.pkl', "rb") as f:
        while True:
            try:
                i_list.append(pickle.load(f))
            except Exception:
                break
    i_list_argsort = np.argsort(i_list)

    tvec_list = []
    with open(f'{Cachan}/tvec.pkl', "rb") as f:
        while True:
            try:
                tvec_list.append(pickle.load(f))
            except Exception:
                break
    tvec_list = np.array(tvec_list)[i_list_argsort]

    # Vmvec_list = []
    # with open(f'{Cachan}/Vmvec.pkl', "rb") as f:
    #     while True:
    #         try:
    #             Vmvec_list.append(pickle.load(f))
    #         except Exception:
    #             break
    # Vmvec_list = np.array(Vmvec_list)[i_list_argsort]

    Cavec_list = []
    with open(f'{Cachan}/Cavec.pkl', "rb") as f:
        while True:
            try:
                Cavec_list.append(pickle.load(f))
            except Exception:
                break
    Cavec_list = np.array(Cavec_list)[i_list_argsort]

    medianCa_list = np.array([np.median(Cavec_list[i][(tvec_list[i]>0.5) & (tvec_list[i]<=1)]) for i in range(len(Cavec_list))])
    with open(f'{Cachan}/medianCa.pkl', "wb") as output_file:
        pickle.dump(medianCa_list, output_file)