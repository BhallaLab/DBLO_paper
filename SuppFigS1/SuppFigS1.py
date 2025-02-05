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
import scipy.stats as sst
import scipy.signal as ssg

import json
from pprint import pprint

import pickle
import scipy
import MOOSEModel_ as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy
from pprint import pprint
import efel
from goMultiprocessing import Multiprocessthis_appendsave

import statsmodels.formula.api as smf

sns.set(style="ticks")
sns.set_context("paper")

fig = plt.figure(figsize=(8, 3), constrained_layout=False)
# fig = plt.figure(constrained_layout=True)
gs = GridSpec(1, 2, figure=fig)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
# axC = fig.add_subplot(gs[1, 0])
# axD = fig.add_subplot(gs[1, 1])


# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA, axB]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig - 20
    y_infig = y_infig + 20
    x_ax, y_ax = ax.transAxes.inverted().transform([x_infig,y_infig])
    ax.text(
        x_ax,
        y_ax,
        f"{chr(65+i)}",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        va="top",
        ha="right",
    )

# Load models from the JSON file
basemodels_list = []
file_path = "activemodels_activesoma.json"
with open(file_path, "r") as file:
    for line in file:
        basemodel = json.loads(line)
        basemodels_list.append(basemodel)

DBLO_150pA_list = []
AP1amp_150pA_list = []
RA_list = []
for model in basemodels_list:
    DBLO_150pA_list.append(model["Features"]["DBLO_1.5e-10"])
    AP1amp_150pA_list.append(model["Features"]["AP1_amp_1.5e-10"])
    RA_list.append(model["Parameters"]["Passive"]["sm_RA"])


#### Panel A ###################
# axA.scatter(RA_list, np.array(DBLO_150pA_list)*1e3, c='C7', s=4)
# axA.set_xlabel(r'RA ($\Omega$m)')
# axA.set_ylabel('DBLO (mV)')
# axA.set_xscale('log')
# m_RAvsDBLO, b_RAvsDBLO, r_RAvsDBLO, pvalue_RAvsDBLO, _ = sst.linregress(RA_list, np.array(DBLO_150pA_list)*1e3)

# axB.scatter(RA_list, np.array(AP1amp_150pA_list)*1e3, c='C7', s=4)
# axB.set_ylabel(r'Spike height (mV)')
# axB.set_xlabel(r'RA ($\Omega$m)')
# axB.set_xscale('log')
# m_RAvsAP1amp, b_RAvsAP1amp, r_RAvsAP1amp, pvalue_RAvsAP1amp, _ = sst.linregress(RA_list, np.array(AP1amp_150pA_list)*1e3)

df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

axA.axvspan(14.3, 23.6, color='C2', alpha=0.3)
# axA.text(20, 100, "High DBLO", fontsize=12, color="black",
#         horizontalalignment='center', verticalalignment='center', rotation=90)
axA.axvspan(10, 14.3, color='C8', alpha=0.3)
# axA.text(14, 100, "Moderate DBLO", fontsize=12, color="black",
#         horizontalalignment='center', verticalalignment='center', rotation=90)
axA.axhspan(df_expsummaryactiveF['10th quantile']["AP1_amp_1.5e-10"]*1e3, df_expsummaryactiveF['90th quantile']["AP1_amp_1.5e-10"]*1e3, color='C9', alpha=0.3)
# axA.text(-10, 120, "Physiological AP1 amplitude", fontsize=12, color="black",
#         horizontalalignment='center', verticalalignment='center', rotation=0)
axA.scatter(np.array(DBLO_150pA_list)*1e3, np.array(AP1amp_150pA_list)*1e3, c='C7', s=4)
axA.set_ylabel(r'Spike height (mV)')
axA.set_xlabel('DBLO (mV)')
# axB.set_xscale('log')



m_DBLOvsAP1amp, b_DBLOvsAP1amp, r_DBLOvsAP1amp, pvalue_DBLOvsAP1amp, _ = sst.linregress(np.array(DBLO_150pA_list)*1e3, np.array(AP1amp_150pA_list)*1e3)


#### Panel B #########################
highRAmodelidx = np.argsort(RA_list)[-1]
lowRAmodelidx = np.argsort(RA_list)[0]
highRAmodel = basemodels_list[highRAmodelidx]
lowRAmodel = basemodels_list[lowRAmodelidx]

t150, Itrace150, Vtrace150, Ca = mm.runModel(highRAmodel, 150e-12, refreshKin=True)
axB.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='high RA', c='C2')
t150, Itrace150, Vtrace150, Ca = mm.runModel(lowRAmodel, 150e-12, refreshKin=True)
axB.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='low RA', c='C3')
axB.set_xlabel("Time (ms)")
axB.set_ylabel("Voltage (mV)")
axB.set_title("Representative models")
axB.legend(frameon=False)
axB.set_xlim(400, 1300)

# axA.scatter(RA_list[highRAmodelidx], np.array(DBLO_150pA_list)[highRAmodelidx]*1e3, c='C2', s=100, marker='X')
# axA.scatter(RA_list[lowRAmodelidx], np.array(DBLO_150pA_list)[lowRAmodelidx]*1e3, c='C3', s=100, marker='X')
# axB.scatter(RA_list[highRAmodelidx], np.array(AP1amp_150pA_list)[highRAmodelidx]*1e3, c='C2', s=100, marker='X')
# axB.scatter(RA_list[lowRAmodelidx], np.array(AP1amp_150pA_list)[lowRAmodelidx]*1e3, c='C3', s=100, marker='X')
axA.scatter(np.array(DBLO_150pA_list)[highRAmodelidx]*1e3, np.array(AP1amp_150pA_list)[highRAmodelidx]*1e3, c='C2', s=100, marker='X')
axA.scatter(np.array(DBLO_150pA_list)[lowRAmodelidx]*1e3, np.array(AP1amp_150pA_list)[lowRAmodelidx]*1e3, c='C3', s=100, marker='X')


#####################
sns.despine(fig=fig)
plt.tight_layout()
plt.savefig('SuppFigS2.png', dpi=300)
# # plt.savefig('Fig8.pdf', dpi=300)
plt.show()


#####################
############ Write to NOTES.txt ###############
with open('NOTES.txt', 'w') as f:
    # f.write(f'RA vs DBLO linear regressin - {r_RAvsDBLO:1.2f}, pvalue {pvalue_RAvsDBLO:1.2e}\n')
    # f.write(f'RA vs AP1 amp linear regressin - {r_RAvsAP1amp:1.2f}, pvalue {pvalue_RAvsAP1amp:1.2e}\n')
    f.write(f'DBLO vs AP1 amp linear regressin - {r_DBLOvsAP1amp:1.2f}, pvalue {pvalue_DBLOvsAP1amp:1.2e}\n')
    f.write(f"Highest RA model's DBLO - {np.array(DBLO_150pA_list)[highRAmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[highRAmodelidx]*1e3} mV and RA - {RA_list[highRAmodelidx]}\n")
    f.write(f"Lowest RA model's DBLO - {np.array(DBLO_150pA_list)[lowRAmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[lowRAmodelidx]*1e3} mV and RA - {RA_list[lowRAmodelidx]}\n")
    f.write(f'Highest DBLO - {np.max(DBLO_150pA_list)*1e3} mV\n')



