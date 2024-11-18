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
from pprint import pprint

import pickle
import scipy
import MOOSEModel as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy
from pprint import pprint
import efel
from goMultiprocessing import Multiprocessthis_appendsave

import statsmodels.formula.api as smf

sns.set(style="ticks")
sns.set_context("paper")

# fig = plt.figure(figsize=(8, 10))
fig, axA = plt.subplots(1,1, figsize=(4,4))


# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA]):
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

df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")
df_expactiveF = pd.read_pickle("../helperScripts/expactiveF.pkl")

basemodel_imp_list = []
file_path = "../Fig9-Implications/activemodels_imp_Eb2_NaTallen.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        if (basemodel["Features"]["AP1_amp_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_amp_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "90th quantile"]):
            basemodel_imp_list.append(basemodel)

DBLO_list = np.array([a["Features"]["DBLO_1.5e-10"] for a in basemodel_imp_list])
AP1thresh_list = np.array([a["Features"]["AP1_thresh_1.5e-10"] for a in basemodel_imp_list])

axA.scatter(DBLO_list*1e3, AP1thresh_list*1e3, s=3, c='C7', label='unified models')
# axA.scatter(df_expactiveF["DBLO_1.5e-10"]*1e3, df_expactiveF["AP1_thresh_1.5e-10"]*1e3, s=3, c='C0', label='experimental data')
axA.set_title('DBLO vs AP1 threshold')
axA.set_ylabel('AP1 Threshold (mV)')
axA.set_xlabel('DBLO at 150 pA (mV)')
# axA.legend(frameon=False, loc='lower left')
axA.text(7, -54, s=f'r = {np.corrcoef(DBLO_list*1e3, AP1thresh_list*1e3)[0][1]:.2f}')

#####################
sns.despine(fig=fig)
plt.tight_layout()
plt.savefig('SuppFigS1.png', dpi=300)
# # plt.savefig('Fig8.pdf', dpi=300)
plt.show()




