### Here we get the phase plot data
import os

os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4

import sys

sys.path.insert(1, "../helperScripts")
sys.path.insert(1, "../Kinetics")

import numpy as np
import matplotlib.pyplot as plt
import features as fts
import MOOSEModel as mm
import MOOSEModel_forKDRNaTcurrents as mm_
import expcells
# import brute_curvefit as bcf
from copy import deepcopy
# from tqdm import tqdm
# import pandas as pd
from pprint import pprint
# from goMultiprocessing import Multiprocessthis_appendsave
# import pickle
import json
import moose
# from scipy import signal
# import warnings

# Load models from the JSON file
basemodels_list = []
file_path = "../helperScripts/1compt.json"
with open(file_path, "r") as file:
    for line in file:
        basemodel = json.loads(line)
        basemodels_list.append(basemodel)


cellidx = 5
Na_T_Gbar = 1.7e-06
K_DR_Gbar = 6.5e-07

# Na_T_Gbarfactor = 0.6
# K_DR_Gbarfactor = 1.8

basemodel_NaMig = {
    "Parameters": {
        "notes2": "",
        "Morphology": {
            "sm_len": 15e-6,
            "sm_diam": 15e-6,
            "dend_len": 500e-6,
            "dend_diam_start": 4e-6,
            "dend_diam_end": 4e-6,
            "num_dend_segments": 0,
        },
        "Passive": {
            "Em": -82e-3,
            "sm_RM": 1.48,
            "sm_CM": 0.015,
            "sm_RA": 1.59,
            "dend_RM": 1.54,
            "dend_CM": 0.021,
            "dend_RA": 0.73,
        },
        "Channels": {
            "Na_Chan": {
                "Gbar": Na_T_Gbar,
                "Erev": 0.06,
                "Kinetics": "../Kinetics/Na_Chan_Migliore2018",
            },
            "K_DR_Chan": {
                "Gbar": K_DR_Gbar,
                "Erev": -0.100,
                "Kinetics": "../Kinetics/K_DR_Chan_Custom3",
            },
            "h_Chan": {
                "Gbar": 1e-8,
                "Erev": -0.040,
                "Kinetics": "../Kinetics/h_Chan_Hay2011_exact",
            },
        },
    }
}


baseModel_NaMig = deepcopy(basemodels_list[cellidx])
baseModel_NaMig["Parameters"]["Channels"]["Na_Chan"] = basemodel_NaMig["Parameters"]["Channels"]["Na_Chan"]
baseModel_NaMig["Parameters"]["Channels"]["K_DR_Chan"] = basemodel_NaMig["Parameters"]["Channels"]["K_DR_Chan"]
baseModel_NaMig["Parameters"]["Channels"]["h_Chan"]["Kinetics"] = basemodel_NaMig["Parameters"]["Channels"]["h_Chan"]["Kinetics"]

######################################################################

############################# NaMiginftaumGoutauh ##########################################################################################3
basemodel_NaMiginftaumGoutauh = {
    "Parameters": {
        "notes2": "",
        "Morphology": {
            "sm_len": 15e-6,
            "sm_diam": 15e-6,
            "dend_len": 500e-6,
            "dend_diam_start": 4e-6,
            "dend_diam_end": 4e-6,
            "num_dend_segments": 0,
        },
        "Passive": {
            "Em": -82e-3,
            "sm_RM": 1.48,
            "sm_CM": 0.015,
            "sm_RA": 1.59,
            "dend_RM": 1.54,
            "dend_CM": 0.021,
            "dend_RA": 0.73,
        },
        "Channels": {
            "Na_Chan": {
                "Gbar": Na_T_Gbar,
                "Erev": 0.06,
                "Kinetics": "../Kinetics/Na_Chan_MiginftaumGoutauh",
            },
            "K_DR_Chan": {
                "Gbar": K_DR_Gbar,
                "Erev": -0.100,
                "Kinetics": "../Kinetics/K_DR_Chan_Custom3",
            },
            "h_Chan": {
                "Gbar": 1e-8,
                "Erev": -0.040,
                "Kinetics": "../Kinetics/h_Chan_Hay2011_exact",
            },
        },
    }
}


baseModel_NaMiginftaumGoutauh = deepcopy(basemodels_list[cellidx])
baseModel_NaMiginftaumGoutauh["Parameters"]["Channels"]["Na_Chan"] = basemodel_NaMiginftaumGoutauh["Parameters"]["Channels"]["Na_Chan"]
baseModel_NaMiginftaumGoutauh["Parameters"]["Channels"]["K_DR_Chan"] = basemodel_NaMiginftaumGoutauh["Parameters"]["Channels"]["K_DR_Chan"]
baseModel_NaMiginftaumGoutauh["Parameters"]["Channels"]["h_Chan"]["Kinetics"] = basemodel_NaMiginftaumGoutauh["Parameters"]["Channels"]["h_Chan"]["Kinetics"]

######################################################
def find_crossing_widths(signal, threshold=0.01, dt=1/20000):
    signal = np.asarray(signal)
    above = signal > threshold
    crossings = []
    i = 1
    while i < len(signal):
        # Rising edge: crossing from below to above threshold
        if not above[i-1] and above[i]:
            # Linear interpolation to estimate exact crossing time
            frac = (threshold - signal[i-1]) / (signal[i] - signal[i-1])
            t_rise = (i-1 + frac) * dt
            # Now search for the next falling edge
            for j in range(i+1, len(signal)):
                if above[j-1] and not above[j]:
                    frac = (threshold - signal[j-1]) / (signal[j] - signal[j-1])
                    t_fall = (j-1 + frac) * dt
                    crossings.append(t_fall - t_rise)
                    i = j  # resume search after this falling edge
                    break
            else:
                break  # No falling edge found
        i += 1
    return crossings

########################################################
fig, axA = plt.subplots(3,1, sharex=True, sharey=True)

axA_ = [0]*3
axA_[0] = axA[0].twinx()
axA_[1] = axA[1].twinx()
axA_[2] = axA[2].twinx()

tvec_NaMig, Ivec_NaMig, Vmvec_NaMig,Cavec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig, I_K_DR_Chan_vec_NaMig = mm_.runModel(baseModel_NaMig, 150e-12, Truntime=0.6)
moose.delete('library')
tvec_NaMiginftaumGoutauh, Ivec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh,Cavec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh = mm_.runModel(baseModel_NaMiginftaumGoutauh, 150e-12, Truntime=0.6)
moose.delete('library')

axA[0].plot(tvec_NaMig, Vmvec_NaMig, c="C0", label='Mig')
axA_[0].plot(tvec_NaMig, I_K_DR_Chan_vec_NaMig, c="C0", ls='--', label='Mig')
axA[0].plot(tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, c="C3", label='MiginftaumGoutauh')
axA_[0].plot(tvec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh, c="C3", ls='--', label='MiginftaumGoutauh')
F = fts.modelfeatures(baseModel_NaMig, stim_start=0.5, stim_end=1)
print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
moose.delete('library')
F = fts.modelfeatures(baseModel_NaMiginftaumGoutauh, stim_start=0.5, stim_end=1)
print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
np.save('phaseplotdata_NaMig_same.npy', [tvec_NaMig, Vmvec_NaMig, I_K_DR_Chan_vec_NaMig])
np.save('phaseplotdata_NaMiginftaumGoutauh_same.npy', [tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh])

####

# tvec_NaMig, Ivec_NaMig, Vmvec_NaMig,Cavec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig, I_K_DR_Chan_vec_NaMig = mm_.runModel(baseModel_NaMig, 150e-12, Truntime=0.6)
# moose.delete('library')
# tvec_NaMiginftaumGoutauh, Ivec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh,Cavec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh = mm_.runModel(baseModel_NaMiginftaumGoutauh, 150e-12, Truntime=0.6)
# moose.delete('library')

axA[1].plot(tvec_NaMig, Vmvec_NaMig, c="C0", label='Mig')
axA_[1].plot(tvec_NaMig, Gk_Na_Chan_vec_NaMig/Na_T_Gbar, c="C0", ls='--', label='Mig')
axA[1].plot(tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, c="C3", label='MiginftaumGoutauh')
axA_[1].plot(tvec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh/Na_T_Gbar, c="C3", ls='--', label='MiginftaumGoutauh')

print(find_crossing_widths(Gk_Na_Chan_vec_NaMig/Na_T_Gbar))
print(find_crossing_widths(Gk_Na_Chan_vec_NaMiginftaumGoutauh/Na_T_Gbar))
# F = fts.modelfeatures(baseModel_NaMig, stim_start=0.5, stim_end=1)
# print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# moose.delete('library')
# F = fts.modelfeatures(baseModel_NaMiginftaumGoutauh, stim_start=0.5, stim_end=1)
# print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# np.save('phaseplotdata_NaMig_KDR0.npy', [tvec_NaMig, Vmvec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig])
# np.save('phaseplotdata_NaMiginftaumGoutauh_KDR0.npy', [tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh])

####

baseModel_NaMig["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"] *= 1e-10
baseModel_NaMiginftaumGoutauh["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"] *= 1e-10
tvec_NaMig, Ivec_NaMig, Vmvec_NaMig,Cavec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig, I_K_DR_Chan_vec_NaMig = mm_.runModel(baseModel_NaMig, 150e-12, Truntime=0.6)
moose.delete('library')
tvec_NaMiginftaumGoutauh, Ivec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh,Cavec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh = mm_.runModel(baseModel_NaMiginftaumGoutauh, 150e-12, Truntime=0.6)
moose.delete('library')

axA[2].plot(tvec_NaMig, Vmvec_NaMig, c="C0", label='Mig')
axA_[2].plot(tvec_NaMig, Na_Chan_Y_vec_NaMig, c="C0", ls='--', label='Mig')
axA[2].plot(tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, c="C3", label='MiginftaumGoutauh')
axA_[2].plot(tvec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, c="C3", ls='--', label='MiginftaumGoutauh')
F = fts.modelfeatures(baseModel_NaMig, stim_start=0.5, stim_end=1)
print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
moose.delete('library')
F = fts.modelfeatures(baseModel_NaMiginftaumGoutauh, stim_start=0.5, stim_end=1)
print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
np.save('phaseplotdata_NaMig_KDR0.npy', [tvec_NaMig, Vmvec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig])
np.save('phaseplotdata_NaMiginftaumGoutauh_KDR0.npy', [tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh])


# baseModel_NaMig["Parameters"]["Channels"]["Na_Chan"]["Gbar"] *= Na_T_Gbarfactor
# tvec_NaMig, Ivec_NaMig, Vmvec_NaMig,Cavec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig, I_K_DR_Chan_vec_NaMig = mm_.runModel(baseModel_NaMig, 150e-12, Truntime=0.6)
# moose.delete('library')
# # tvec_NaMiginftaumGoutauh, Ivec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh,Cavec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh = mm_.runModel(baseModel_NaMiginftaumGoutauh, 150e-12, Truntime=0.6)
# # moose.delete('library')

# axA[1].plot(tvec_NaMig, Vmvec_NaMig, c="C0", label='Mig')
# axA[1].plot(tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, c="C3", label='MiginftaumGoutauh')
# F = fts.modelfeatures(baseModel_NaMig, stim_start=0.5, stim_end=1)
# print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# moose.delete('library')
# # F = fts.modelfeatures(baseModel_NaMiginftaumGoutauh, stim_start=0.5, stim_end=1)
# # print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# np.save('phaseplotdata_NaMig_ampcompensated.npy', [tvec_NaMig, Vmvec_NaMig])
# np.save('phaseplotdata_NaMiginftaumGoutauh_ampcompensated.npy', [tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh])


# baseModel_NaMig["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"] *= K_DR_Gbarfactor
# tvec_NaMig, Ivec_NaMig, Vmvec_NaMig,Cavec_NaMig, Gk_Na_Chan_vec_NaMig, Na_Chan_Y_vec_NaMig, I_K_DR_Chan_vec_NaMig = mm_.runModel(baseModel_NaMig, 150e-12, Truntime=0.6)
# moose.delete('library')
# # tvec_NaMiginftaumGoutauh, Ivec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh,Cavec_NaMiginftaumGoutauh, Gk_Na_Chan_vec_NaMiginftaumGoutauh, Na_Chan_Y_vec_NaMiginftaumGoutauh, I_K_DR_Chan_vec_NaMiginftaumGoutauh = mm_.runModel(baseModel_NaMiginftaumGoutauh, 150e-12, Truntime=0.6)
# # moose.delete('library')

# axA[2].plot(tvec_NaMig-0.0033, Vmvec_NaMig, c="C0", label='Mig')
# axA[2].plot(tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh, c="C3", label='MiginftaumGoutauh')
# F = fts.modelfeatures(baseModel_NaMig, stim_start=0.5, stim_end=1)
# print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# moose.delete('library')
# # F = fts.modelfeatures(baseModel_NaMiginftaumGoutauh, stim_start=0.5, stim_end=1)
# # print(F['freq_1.5e-10'], F['AP1_width_1.5e-10'], F['DBLO_1.5e-10'], F['AP1_amp_1.5e-10']+F['AP1_thresh_1.5e-10'])
# np.save('phaseplotdata_NaMig_ampwidthcompensated.npy', [tvec_NaMig, Vmvec_NaMig])
# np.save('phaseplotdata_NaMiginftaumGoutauh_ampwidthcompensated.npy', [tvec_NaMiginftaumGoutauh, Vmvec_NaMiginftaumGoutauh])



plt.show()















