### Here, we make active models with all the channels

import os

os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4

import sys

sys.path.insert(1, "../helperScripts")

import numpy as np
import matplotlib.pyplot as plt
import features as fts
import MOOSEModel as mm
import expcells
import brute_curvefit as bcf
from copy import deepcopy
from tqdm import tqdm
import pandas as pd
from pprint import pprint
from goMultiprocessing import Multiprocessthis_appendsave
import pickle
import json
from scipy import signal
import warnings

# warnings.simplefilter(action="ignore", category=FutureWarning)
# warnings.simplefilter(action="ignore", category=RuntimeWarning)
# warnings.simplefilter(action="ignore", category=RuntimeError)

Featurelist = [
    "CellID",
    # "E_rest_0",
    # "Input resistance",
    # "Cell capacitance",
    # "Time constant",
    # "sagV_m50",
    # "sagrat_m50",
    "freq_0",
    "AP1_amp_1.5e-10",
    # "APp_amp_1.5e-10",
    # "AP1_time_1.5e-10",
    # "APp_time_1.5e-10",
    # "APavgpratio_amp_1.5e-10",
    # "AP1_width_1.5e-10",
    # "APp_width_1.5e-10",
    # "AP1_thresh_1.5e-10",
    # "APp_thresh_1.5e-10",
    # "AP1_lat_1.5e-10",
    # "ISI1_1.5e-10",
    # "ISIl_1.5e-10",
    "ISIavg_1.5e-10",
    # "ISImedian_1.5e-10",
    "freq_1.5e-10",
    # "Adptn_id_1.5e-10",
    # "fAHP_AP1_amp_1.5e-10",
    # "DBLO_1.5e-10",
    # "AbsDBL_1.5e-10",
    # "AP1_amp_3e-10",
    # "APp_amp_3e-10",
    # "AP1_time_3e-10",
    # "APp_time_3e-10",
    # "APavgpratio_amp_3e-10",
    # "AP1_width_3e-10",
    # "APp_width_3e-10",
    # "AP1_thresh_3e-10",
    # "APp_thresh_3e-10",
    # "AP1_lat_3e-10",
    # "ISI1_3e-10",
    # "ISIl_3e-10",
    # "ISIavg_3e-10",
    # "ISImedian_3e-10",
    # "freq_3e-10",
    # "Adptn_id_3e-10",
    # "fAHP_AP1_amp_3e-10",
    # "DBLO_3e-10",
    # "AbsDBL_3e-10",
    # "freq300to150ratio",
]
# pasmodelFlist = ['E_rest_0', 'Input resistance', 'Cell capacitance', 'Time constant', 'sagV_m50', 'sagrat_m50', "ISImedian_1.5e-10"]

### get exp cell features ###
LJP = 15e-3
samplingrate = 20000
df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

######################################################
stimamp = 30e-12
stim_start_chirp = 0.3
stim_end_chirp = 13.3
stim_start = 0.5
stim_end = 1
tstop = 14.5
stimlist_chirp = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start_chirp} & t<{stim_end_chirp}) * sin(2*3.14159265359*(t-{stim_start_chirp})^3) * {stimamp}",
]
stimlist_chirp2 = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start_chirp} & t<{stim_start_chirp+501}) * sin(2*3.14159265359*(t-{stim_start_chirp})^2) * {stimamp}",
]
stimlist_CC = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start} & t<{stim_start+0.5}) * {-25e-12}",
]
stimlist_epsp = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start} & t<{stim_start+0.5}) * {0e-12}",
]
stimlist_150pA = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start} & t<{stim_start+0.5}) * {150e-12}",
]
stimlist_bis = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start} & t<{stim_start+0.2}) * {150e-12} + (t>{stim_start+0.5} & t<{stim_start+0.7}) * {-50e-12}",
]

baseModel = {
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
            "sm_RM": 0.1,
            "sm_CM": 0.17,
            "sm_RA": 1.59,
            "dend_RM": 1.54,
            "dend_CM": 0.021,
            "dend_RA": 0.73,
        },
        "Channels": {
            "Na_T_Chan": {
                "Gbar": 1e-4,
                "Erev": 0.06,
                "Kinetics": "../Kinetics/Na_T_Chan_Royeck_wslow",
            },
            "K_DR_Chan": {
                "Gbar": 1e-3,
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

# Load models from the JSON file
basemodels_list = []
file_path = "../helperScripts/1compt.json"
with open(file_path, "r") as file:
    for line in file:
        basemodel = json.loads(line)
        basemodels_list.append(basemodel)
####################################################

def ourfunc(i):
    model = deepcopy(baseModel)
    pasmodel = basemodels_list[np.random.randint(0, len(basemodels_list))]
    model["Parameters"]["notes"] = pasmodel["Parameters"]["notes"]
    model["Parameters"]["Morphology"] = pasmodel["Parameters"]["Morphology"]
    model["Parameters"]["Passive"] = pasmodel["Parameters"]["Passive"]
    if "Gbar" in pasmodel["Parameters"]["Channels"]["h_Chan"].keys():
        model["Parameters"]["Channels"]["h_Chan"]["Gbar"] = pasmodel["Parameters"][
            "Channels"
        ]["h_Chan"]["Gbar"]
        model["Parameters"]["Channels"]["h_Chan"].pop("gbar", None)
    else:
        model["Parameters"]["Channels"]["h_Chan"]["Gbar"] = pasmodel["Parameters"][
            "Channels"
        ]["h_Chan"]["gbar"]*np.pi*model["Parameters"]["Morphology"]["sm_len"]*model["Parameters"]["Morphology"]["sm_diam"]
        model["Parameters"]["Channels"]["h_Chan"].pop("gbar", None)

    model["Parameters"]["Channels"]["Na_T_Chan"]["Gbar"] = 10 ** np.random.uniform(
        -7, -5
        # -8, -4
    )
    model["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"] = 10 ** np.random.uniform(
        # -7, -2
        -6, -3
    )
    model["Parameters"]["Channels"]["K_DR_Chan"]["Erev"] = np.random.uniform(-100e-3, -50e-3)

    Featurelist_ = Featurelist[1:]  ## To remove CellID

    modelF = fts.modelfeatures(
        model, stim_start=0.5, stim_end=1, refreshKin=True
    )

    for f in Featurelist_:
        if modelF[f] is None:
            return [{}]


    model["Features"] = modelF

    if model["Features"]["freq_1.5e-10"]*model["Features"]["ISIavg_1.5e-10"] < 0.9: ## So that Depolarization blocks are taken care of
        return [{}]

    for rrow in Featurelist_:
        if model["Features"][rrow] < df_expsummaryactiveF.loc[rrow, "10th quantile"]:
            return [{}]
        if model["Features"][rrow] > df_expsummaryactiveF.loc[rrow, "90th quantile"]:
            return [{}]
    
    print('yoooohooooo', model["Features"]["DBLO_1.5e-10"])
    return [model]


Multiprocessthis_appendsave(
   ourfunc, range(50000), [], ["tempactivemodels.pkl"], seed=np.random.randint(0, 2**32 - 1), npool=0.8
)

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


with open("tempactivemodels.pkl", "rb") as f, open(
    'activemodels.json', "a"
) as file:
    while True:
        model = pickle.load(f)
        # pprint(model)
        if len(model) > 0:
            json.dump(model, file, cls=NpEncoder)
            file.write("\n")