# import pylustrator

# pylustrator.start()

import sys

sys.path.insert(1, "../helperScripts")
from DBLOutilities import PrintLogger as PrintLogger

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.collections import LineCollection
import scikit_posthocs as sp
import os
# import subprocess
from scipy import signal
import scipy.stats as scs

import expcells
import features as fts
import json

from goMultiprocessing import Multiprocessthis_appendsave
# import pickle
import scipy
import MOOSEModel as mm
import MOOSEModel_forKDRNaTcurrents as mm_
from matplotlib.cm import viridis
from matplotlib.colors import to_rgba
from copy import deepcopy
import moose
import matplotlib.patches as mpatches

pd.options.display.float_format = '{:.2e}'.format

sns.set(style="ticks")
sns.set_context("paper")

fig = plt.figure(figsize=(8, 10))
gs = fig.add_gridspec(4,2, hspace=0.4, wspace=0.3)

gs_inner = gs[0:2, 0].subgridspec(
    2, 1, hspace=0.1
)
axA = [0]*2
axA[0] = fig.add_subplot(gs_inner[0, 0])
axA[1] = fig.add_subplot(gs_inner[1, 0])

axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, 1])
axD = fig.add_subplot(gs[2, 0])
axE = fig.add_subplot(gs[2, 1])
axF = fig.add_subplot(gs[3, 0])
axG = fig.add_subplot(gs[3, 1])


# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA[0], axB, axC, axD, axE, axF, axG]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig - 20
    y_infig = y_infig + 20
    x_ax, y_ax = ax.transAxes.inverted().transform([x_infig,y_infig])
    ax.text(
        x_ax,
        y_ax,
        f'{chr(65+i)}',
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        va="top",
        ha="right",
    )

def int_to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_numeral = ""
    for i, v in enumerate(val):
        while n >= v:
            roman_numeral += syms[i]
            n -= v
    return roman_numeral

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA[0], axA[1]]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig
    y_infig = y_infig + 15
    x_ax, y_ax = ax.transAxes.inverted().transform([x_infig,y_infig])
    ax.text(
        x_ax,
        y_ax,
        f'({int_to_roman(i+1)})',
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        va="top",
        ha="right",
    )

# f = open('NOTES.txt', 'w')
sys.stdout = PrintLogger('NOTES.txt', 'w')
##############################
df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

# Load models from the JSON file
basemodels_NaTGou_list = []
basemodels_NaTGou_nowidth_list = []
file_path = "activemodels_NaTGou_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaTGou_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaTGou_list.append(basemodel)

print(f'Number of valid NaTGou models: {len(basemodels_NaTGou_list)}')
DBLO_NaTGou_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaTGou_list])
AP1_height_NaTGou_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaTGou_list])
DBLO_nowidth_NaTGou_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaTGou_nowidth_list])
AP1_width_NaTGou_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaTGou_list])
AP1_width_nowidth_NaTGou_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaTGou_nowidth_list])
KDRGbar_NaTGou_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaTGou_list])
KDRGbar_nowidth_NaTGou_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaTGou_nowidth_list])
highDBLOmodel_NaTGou = np.array(basemodels_NaTGou_list)[np.argsort(DBLO_NaTGou_list)[-1]]


# Load models from the JSON file
basemodels_NaTRoy_list = []
basemodels_NaTRoy_nowidth_list = []
file_path = "activemodels_NaTRoy_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaTRoy_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaTRoy_list.append(basemodel)

print(f'Number of valid NaTRoy models: {len(basemodels_NaTRoy_list)}')
DBLO_NaTRoy_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaTRoy_list])
AP1_height_NaTRoy_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaTRoy_list])
DBLO_nowidth_NaTRoy_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaTRoy_nowidth_list])
AP1_width_NaTRoy_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaTRoy_list])
AP1_width_nowidth_NaTRoy_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaTRoy_nowidth_list])
KDRGbar_NaTRoy_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaTRoy_list])
KDRGbar_nowidth_NaTRoy_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaTRoy_nowidth_list])
highDBLOmodel_NaTRoy = np.array(basemodels_NaTRoy_list)[np.argsort(DBLO_NaTRoy_list)[-1]]


# Load models from the JSON file
basemodels_NaMig_list = []
basemodels_NaMig_nowidth_list = []
file_path = "activemodels_NaMig_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaMig_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaMig_list.append(basemodel)

print(f'Number of valid NaMig models: {len(basemodels_NaMig_list)}')
DBLO_NaMig_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMig_list])
AP1_height_NaMig_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaMig_list])
DBLO_nowidth_NaMig_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMig_nowidth_list])
AP1_width_NaMig_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMig_list])
AP1_width_nowidth_NaMig_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMig_nowidth_list])
KDRGbar_NaMig_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMig_list])
KDRGbar_nowidth_NaMig_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMig_nowidth_list])
highDBLOmodel_NaMig = np.array(basemodels_NaMig_list)[np.argsort(DBLO_NaMig_list)[-1]]


# Load models from the JSON file
basemodels_NaMiginfGoutau_list = []
basemodels_NaMiginfGoutau_nowidth_list = []
file_path = "activemodels_NaMiginfGoutau_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaMiginfGoutau_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaMiginfGoutau_list.append(basemodel)

print(f'Number of valid NaMiginfGoutau models: {len(basemodels_NaMiginfGoutau_list)}')
DBLO_NaMiginfGoutau_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginfGoutau_list])
AP1_height_NaMiginfGoutau_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaMiginfGoutau_list])
DBLO_nowidth_NaMiginfGoutau_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginfGoutau_nowidth_list])
AP1_width_NaMiginfGoutau_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginfGoutau_list])
AP1_width_nowidth_NaMiginfGoutau_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginfGoutau_nowidth_list])
KDRGbar_NaMiginfGoutau_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginfGoutau_list])
KDRGbar_nowidth_NaMiginfGoutau_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginfGoutau_nowidth_list])
highDBLOmodel_NaMiginfGoutau = np.array(basemodels_NaMiginfGoutau_list)[np.argsort(DBLO_NaMiginfGoutau_list)[-1]]


# Load models from the JSON file
basemodels_NaMigtauGouinf_list = []
basemodels_NaMigtauGouinf_nowidth_list = []
file_path = "activemodels_NaMigtauGouinf_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaMigtauGouinf_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaMigtauGouinf_list.append(basemodel)

print(f'Number of valid NaMigtauGouinf models: {len(basemodels_NaMigtauGouinf_list)}')
DBLO_NaMigtauGouinf_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMigtauGouinf_list])
AP1_height_NaMigtauGouinf_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaMigtauGouinf_list])
DBLO_nowidth_NaMigtauGouinf_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMigtauGouinf_nowidth_list])
AP1_width_NaMigtauGouinf_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMigtauGouinf_list])
AP1_width_nowidth_NaMigtauGouinf_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMigtauGouinf_nowidth_list])
KDRGbar_NaMigtauGouinf_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMigtauGouinf_list])
KDRGbar_nowidth_NaMigtauGouinf_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMigtauGouinf_nowidth_list])
highDBLOmodel_NaMigtauGouinf = np.array(basemodels_NaMigtauGouinf_list)[np.argsort(DBLO_NaMigtauGouinf_list)[-1]]


# Load models from the JSON file
basemodels_NaMiginftauhGoutaum_list = []
basemodels_NaMiginftauhGoutaum_nowidth_list = []
file_path = "activemodels_NaMiginftauhGoutaum_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaMiginftauhGoutaum_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaMiginftauhGoutaum_list.append(basemodel)

print(f'Number of valid NaMiginftauhGoutaum models: {len(basemodels_NaMiginftauhGoutaum_list)}')
DBLO_NaMiginftauhGoutaum_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginftauhGoutaum_list])
AP1_height_NaMiginftauhGoutaum_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaMiginftauhGoutaum_list])
DBLO_nowidth_NaMiginftauhGoutaum_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginftauhGoutaum_nowidth_list])
AP1_width_NaMiginftauhGoutaum_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginftauhGoutaum_list])
AP1_width_nowidth_NaMiginftauhGoutaum_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginftauhGoutaum_nowidth_list])
KDRGbar_NaMiginftauhGoutaum_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginftauhGoutaum_list])
KDRGbar_nowidth_NaMiginftauhGoutaum_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginftauhGoutaum_nowidth_list])
highDBLOmodel_NaMiginftauhGoutaum = np.array(basemodels_NaMiginftauhGoutaum_list)[np.argsort(DBLO_NaMiginftauhGoutaum_list)[-1]]


# Load models from the JSON file
basemodels_NaMiginftaumGoutauh_list = []
basemodels_NaMiginftaumGoutauh_nowidth_list = []
file_path = "activemodels_NaMiginftaumGoutauh_.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        basemodels_NaMiginftaumGoutauh_nowidth_list.append(basemodel)
        if (basemodel["Features"]["AP1_width_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_width_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_width_1.5e-10", "90th quantile"]):
            basemodels_NaMiginftaumGoutauh_list.append(basemodel)

print(f'Number of valid NaMiginftaumGoutauh models: {len(basemodels_NaMiginftaumGoutauh_list)}')
DBLO_NaMiginftaumGoutauh_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginftaumGoutauh_list])
AP1_height_NaMiginftaumGoutauh_list = np.array([a["Features"]["AP1_thresh_1.5e-10"]*1e3+a["Features"]["AP1_amp_1.5e-10"]*1e3 for a in basemodels_NaMiginftaumGoutauh_list])
AP1_width_NaMiginftaumGoutauh_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginftaumGoutauh_list])
AP1_width_nowidth_NaMiginftaumGoutauh_list = np.array([a["Features"]["AP1_width_1.5e-10"]*1e3 for a in basemodels_NaMiginftaumGoutauh_nowidth_list])
DBLO_nowidth_NaMiginftaumGoutauh_list = np.array([a["Features"]["DBLO_1.5e-10"]*1e3 for a in basemodels_NaMiginftaumGoutauh_nowidth_list])
KDRGbar_NaMiginftaumGoutauh_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginftaumGoutauh_list])
KDRGbar_nowidth_NaMiginftaumGoutauh_list = np.array([a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodels_NaMiginftaumGoutauh_nowidth_list])
highDBLOmodel_NaMiginftaumGoutauh = np.array(basemodels_NaMiginftaumGoutauh_list)[np.argsort(DBLO_NaMiginftaumGoutauh_list)[-1]]


###########################################################################################################################################3
tvec,Ivec,Vmvec,Ca = mm.runModel(highDBLOmodel_NaTGou, refreshKin=True)
xgate = moose.element('library/Na_T_Chan/gateX')
v = np.linspace(xgate.min, xgate.max, xgate.divs+1)
m3_Gou, = axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB)**moose.element('library/Na_T_Chan').Xpower, label='$m_{inf}^3$ Gou', color='C2')
# m_Gou, = axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB), label='$m_{inf}$ Gou', color='C2')
mt_Gou, = axA[1].plot(v*1e3, 1/xgate.tableB*1e3, label='$tau_m$ Gou', color='C2')
ygate = moose.element('library/Na_T_Chan/gateY')
h_Gou, = axA[0].plot(v*1e3, (ygate.tableA/ygate.tableB)**moose.element('library/Na_T_Chan').Ypower, label='$h_{inf}$ \nGou', color='C2', linestyle='--')
ht_Gou, = axA[1].plot(v*1e3, 1/ygate.tableB*1e3, label='$tau_h$ Gou', color='C2', linestyle='--')
moose.delete('library')


tvec,Ivec,Vmvec,Ca = mm.runModel(highDBLOmodel_NaTRoy, refreshKin=True)
xgate = moose.element('library/Na_T_Chan/gateX')
v = np.linspace(xgate.min, xgate.max, xgate.divs+1)
m3_Roy, =axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB)**moose.element('library/Na_T_Chan').Xpower, label='$m_{inf}^3$ Roy', color='C8')
# m_Roy, = axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB), label='$m_{inf}$ Roy', color='C8')
mt_Roy, =axA[1].plot(v*1e3, 1/xgate.tableB*1e3, label='$tau_m$ Roy', color='C8')
ygate = moose.element('library/Na_T_Chan/gateY')
h_Roy, = axA[0].plot(v*1e3, (ygate.tableA/ygate.tableB)**moose.element('library/Na_T_Chan').Ypower, label='$h_{inf}$ \nRoy', color='C8', linestyle='--')
ht_Roy, =axA[1].plot(v*1e3, 1/ygate.tableB*1e3, label='$tau_h$ Roy', color='C8', linestyle='--')
moose.delete('library')


tvec,Ivec,Vmvec,Ca = mm.runModel(highDBLOmodel_NaMig, refreshKin=True)
xgate = moose.element('library/Na_Chan/gateX')
v = np.linspace(xgate.min, xgate.max, xgate.divs+1)
m3_Mig, =axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB)**moose.element('library/Na_Chan').Xpower, label='$m_{inf}^3$ Mig', color='C3')
# m_Mig, = axA[0].plot(v*1e3, (xgate.tableA/xgate.tableB), label='$m_{inf}$ Mig', color='C3')
mt_Mig, =axA[1].plot(v*1e3, 1/xgate.tableB*1e3, label='$tau_m$ Mig', color='C3')
ygate = moose.element('library/Na_Chan/gateY')
h_Mig, = axA[0].plot(v*1e3, (ygate.tableA/ygate.tableB)**moose.element('library/Na_Chan').Ypower, label='$h_{inf}$ \nMig', color='C3', linestyle='--')
ht_Mig, =axA[1].plot(v*1e3, 1/ygate.tableB*1e3, label='$tau_h$ Mig', color='C3', linestyle='--')
moose.delete('library')


# axA[0].set_xlabel('Voltage (mV)')
axA[0].set_ylabel('Steady state (1)')
# axA[0].legend(frameon=False)
legendh = axA[0].legend(handles = [h_Gou, h_Mig, h_Roy], loc='center left', frameon=False, bbox_to_anchor=(-0.02, 0.5))
axA[0].add_artist(legendh)
legendm = axA[0].legend(handles = [m3_Gou, m3_Mig, m3_Roy], loc='center right', frameon=False, bbox_to_anchor=(1.1, 0.3))
axA[0].set_xlim(-100, 0)
axA[0].tick_params(bottom=True, labelbottom=False)

axA[1].set_xlabel('Voltage (mV)')
axA[1].set_ylabel('Tau (ms)')
# axA[1].legend(frameon=False)
legendh = axA[1].legend(handles = [ht_Gou, ht_Mig, ht_Roy], loc='upper left', frameon=False)
axA[1].add_artist(legendh)
legendm = axA[1].legend(handles = [mt_Gou, mt_Mig, mt_Roy],  loc='upper right', frameon=False, bbox_to_anchor=(1, 1))
axA[1].set_xlim(-100, 0)


##########################################

######### Panel B ########################
# s_NaMiginfGoutau = "\n" + "\n" + r"$Mig\_m_{\infty}\_h_{\infty}$" + "\n" + r"$Gou\_m_{\tau}\_h_{\tau}$"
# s_NaMigtauGouinf = r"$Mig\_m_{\tau}\_h_{\tau}$" + "\n" + r"$Gou\_m_{\infty}\_h_{\infty}$"
# s_NaMiginftauhGoutaum = "\n" + "\n" + r"$Mig\_m_{\infty}\_h_{\infty}\_h_{\tau}$" + "\n" + r"$Gou\_m_{\tau}$"
# s_NaMiginftaumGoutauh = r"$Mig\_m_{\infty}\_h_{\infty}\_m_{\tau}$" + "\n" + r"$Gou\_h_{\tau}$"
s_NaMiginfGoutau = r"Mig$_{G\tau}$"
s_NaMigtauGouinf = r"Mig$_{G\infty}$"
s_NaMiginftauhGoutaum = r"Mig$_{G\tau m}$"
s_NaMiginftaumGoutauh = r"Mig$_{G\tau h}$"


df = pd.DataFrame(columns=["type", "DBLO150 (mV)"])
modeltype = (
    ["Gou"] * len(basemodels_NaTGou_list)
    + ["Roy"] * len(basemodels_NaTRoy_list)  
    + ["Mig"] * len(basemodels_NaMig_list)
    + [s_NaMiginfGoutau] * len(basemodels_NaMiginfGoutau_list)
    + [s_NaMigtauGouinf] * len(basemodels_NaMigtauGouinf_list)
    + [s_NaMiginftauhGoutaum] * len(basemodels_NaMiginftauhGoutaum_list)
    + [s_NaMiginftaumGoutauh] * len(basemodels_NaMiginftaumGoutauh_list)
)
DBLO150 = np.concatenate((DBLO_NaTGou_list,DBLO_NaTRoy_list,DBLO_NaMig_list, DBLO_NaMiginfGoutau_list, DBLO_NaMigtauGouinf_list, DBLO_NaMiginftauhGoutaum_list, DBLO_NaMiginftaumGoutauh_list))
df.loc[:, "type"] = modeltype
df.loc[:, "DBLO150 (mV)"] = DBLO150
df = df.convert_dtypes()

GouvsMigvsRoy_kruskal = scipy.stats.kruskal(
    list(df[df["type"] == "Gou"].loc[:, "DBLO150 (mV)"]),
    list(df[df["type"] == "Roy"].loc[:, "DBLO150 (mV)"]),
    list(df[df["type"] == "Mig"].loc[:, "DBLO150 (mV)"]),
    # list(df[df["type"] == s_NaMiginfGoutau].loc[:, "DBLO150 (mV)"]),
    # list(df[df["type"] == s_NaMigtauGouinf].loc[:, "DBLO150 (mV)"]),
    # list(df[df["type"] == s_NaMiginftauhGoutaum].loc[:, "DBLO150 (mV)"]),
    # list(df[df["type"] == s_NaMiginftaumGoutauh].loc[:, "DBLO150 (mV)"]),
)
print('Kruskal-Wallis H-test ', GouvsMigvsRoy_kruskal)

GouvsMigvsRoy_dunn = sp.posthoc_dunn(df, val_col="DBLO150 (mV)", group_col="type", p_adjust='bonferroni')

print('Dunn’s test\n', GouvsMigvsRoy_dunn)
print('Mean DBLO at 150pA\n', df.groupby('type').mean()['DBLO150 (mV)'], df.groupby('type').std()['DBLO150 (mV)'])

print('Max DBLO at 150pA\n', df.groupby('type').max()['DBLO150 (mV)'])

# def statannotator(ax, xpair_list, y, d, pvalues_list):
#     d_ = 0
#     for xpair, pvalue in zip(xpair_list, pvalues_list):
#         ax.plot(xpair, [y + d_, y + d_], c="black")
#         ax.text(np.mean(xpair), y + d_, pvalue, ha="center", va="bottom", c="black")
#         d_ = d_ + d

def statannotator(ax, x_list, y, pvalues_list):
    for x, pvalue in zip(x_list, pvalues_list):
        ax.text(x, y, pvalue, ha="center", va="bottom", c="black")

def convert_pvalue_to_asterisks(pvalue, nfactor=1):
    if pvalue <= 0.0001/nfactor:
        return "****"
    elif pvalue <= 0.001/nfactor:
        return "***"
    elif pvalue <= 0.01/nfactor:
        return "**"
    elif pvalue <= 0.05/nfactor:
        return "*"
    return "ns"


order = ["Gou", "Roy", "Mig", s_NaMiginfGoutau, s_NaMigtauGouinf, s_NaMiginftauhGoutaum, s_NaMiginftaumGoutauh]
palette = ["C2", "C8", "C3", "C4", "C5", "C1", "C9"]
ax = sns.boxplot(
    ax=axB,
    data=df,
    x="type",
    y="DBLO150 (mV)",
    order=order,
    palette=palette,
    showfliers=False,
    zorder=2
)
# ax = sns.violinplot(ax=axD, data=df, x='type', y='DBLO150 (mV)', order=order, palette=palette)
sns.stripplot(
    ax=ax,
    data=df,
    x="type",
    y="DBLO150 (mV)",
    order=order,
    palette=palette,
    size=2,
    zorder=3
)
ax.set_xlabel("")  # Remove x-axis label
ax.set_xticklabels([])  # Remove x-tick labels
statannotator(
    axB,
    [0,1,3,4,5,6],
    df["DBLO150 (mV)"].max()+0.5,
    [
        convert_pvalue_to_asterisks(a)
        for a in [GouvsMigvsRoy_dunn.loc["Mig", "Gou",], GouvsMigvsRoy_dunn.loc["Mig", "Roy"], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginfGoutau], GouvsMigvsRoy_dunn.loc["Mig", s_NaMigtauGouinf], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginftauhGoutaum], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginftaumGoutauh]]
    ],
)


######### Panel C ######################################
if not os.path.exists('max_I_K_DR_NaTGou_list.npy'):
    def find_crossing_widths(signal, threshold=0.5, dt=1/20000):
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

    def ourfunc(model):
        tvec, Ivec, Vmvec,Cavec, Gk_Na_Chan_vec, Na_Chan_Y_vec, I_K_DR_Chan_vec = mm_.runModel(model, refreshKin=True)
        if "Na_Chan" in model["Parameters"]["Channels"].keys():
            normalizedGk = Gk_Na_Chan_vec[tvec>0.5]/max(Gk_Na_Chan_vec[tvec>0.5])
            crossings = find_crossing_widths(normalizedGk)
        else:
            normalizedGk = Gk_Na_Chan_vec[tvec>0.5]/max(Gk_Na_Chan_vec[tvec>0.5])            
            crossings = find_crossing_widths(normalizedGk)
        # print(model["Parameters"]["Channels"]["Na_T_Chan"]["Gbar"])
        # print(f'{max(normalizedGk) = }')
        # plt.figure()
        # # plt.plot(tvec[tvec>0.5], normalizedGk)
        # plt.plot(tvec, Gk_Na_Chan_vec)
        # plt.show()
        return [max(np.abs(I_K_DR_Chan_vec)), crossings[0]]

    max_I_K_DR_NaTGou_list = []
    max_I_K_DR_NaTRoy_list = []
    max_I_K_DR_NaMig_list = []
    max_I_K_DR_NaMiginfGoutau_list = []
    max_I_K_DR_NaMigtauGouinf_list = []
    max_I_K_DR_NaMiginftauhGoutaum_list = []
    max_I_K_DR_NaMiginftaumGoutauh_list = []

    Gkwidth_NaTGou_list = []
    Gkwidth_NaTRoy_list = []
    Gkwidth_NaMig_list = []
    Gkwidth_NaMiginfGoutau_list = []
    Gkwidth_NaMigtauGouinf_list = []
    Gkwidth_NaMiginftauhGoutaum_list = []
    Gkwidth_NaMiginftaumGoutauh_list = []

    # for model in basemodels_NaTGou_list:
    #     ourfunc(model)
    max_I_K_DR_NaTGou_list, Gkwidth_NaTGou_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaTGou_list, [max_I_K_DR_NaTGou_list, Gkwidth_NaTGou_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaTRoy_list, Gkwidth_NaTRoy_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaTRoy_list, [max_I_K_DR_NaTRoy_list, Gkwidth_NaTRoy_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaMig_list, Gkwidth_NaMig_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaMig_list, [max_I_K_DR_NaMig_list, Gkwidth_NaMig_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaMiginfGoutau_list, Gkwidth_NaMiginfGoutau_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaMiginfGoutau_list, [max_I_K_DR_NaMiginfGoutau_list, Gkwidth_NaMiginfGoutau_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaMigtauGouinf_list, Gkwidth_NaMigtauGouinf_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaMigtauGouinf_list, [max_I_K_DR_NaMigtauGouinf_list, Gkwidth_NaMigtauGouinf_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaMiginftauhGoutaum_list, Gkwidth_NaMiginftauhGoutaum_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaMiginftauhGoutaum_list, [max_I_K_DR_NaMiginftauhGoutaum_list, Gkwidth_NaMiginftauhGoutaum_list], [], seed=123412, npool=0.8
        )
    max_I_K_DR_NaMiginftaumGoutauh_list, Gkwidth_NaMiginftaumGoutauh_list = Multiprocessthis_appendsave(
           ourfunc, basemodels_NaMiginftaumGoutauh_list, [max_I_K_DR_NaMiginftaumGoutauh_list, Gkwidth_NaMiginftaumGoutauh_list], [], seed=123412, npool=0.8
        )

    np.save('max_I_K_DR_NaTGou_list.npy', max_I_K_DR_NaTGou_list)
    np.save('max_I_K_DR_NaTRoy_list.npy', max_I_K_DR_NaTRoy_list)
    np.save('max_I_K_DR_NaMig_list.npy', max_I_K_DR_NaMig_list)
    np.save('max_I_K_DR_NaMiginfGoutau_list.npy', max_I_K_DR_NaMiginfGoutau_list)
    np.save('max_I_K_DR_NaMigtauGouinf_list.npy', max_I_K_DR_NaMigtauGouinf_list)
    np.save('max_I_K_DR_NaMiginftauhGoutaum_list.npy', max_I_K_DR_NaMiginftauhGoutaum_list)
    np.save('max_I_K_DR_NaMiginftaumGoutauh_list.npy', max_I_K_DR_NaMiginftaumGoutauh_list)

    np.save('Gkwidth_NaTGou_list.npy', Gkwidth_NaTGou_list)
    np.save('Gkwidth_NaTRoy_list.npy', Gkwidth_NaTRoy_list)
    np.save('Gkwidth_NaMig_list.npy', Gkwidth_NaMig_list)
    np.save('Gkwidth_NaMiginfGoutau_list.npy', Gkwidth_NaMiginfGoutau_list)
    np.save('Gkwidth_NaMigtauGouinf_list.npy', Gkwidth_NaMigtauGouinf_list)
    np.save('Gkwidth_NaMiginftauhGoutaum_list.npy', Gkwidth_NaMiginftauhGoutaum_list)
    np.save('Gkwidth_NaMiginftaumGoutauh_list.npy', Gkwidth_NaMiginftaumGoutauh_list)

max_I_K_DR_NaTGou_list = np.load('max_I_K_DR_NaTGou_list.npy')*1e9
max_I_K_DR_NaTRoy_list = np.load('max_I_K_DR_NaTRoy_list.npy')*1e9
max_I_K_DR_NaMig_list = np.load('max_I_K_DR_NaMig_list.npy')*1e9
max_I_K_DR_NaMiginfGoutau_list = np.load('max_I_K_DR_NaMiginfGoutau_list.npy')*1e9
max_I_K_DR_NaMigtauGouinf_list = np.load('max_I_K_DR_NaMigtauGouinf_list.npy')*1e9
max_I_K_DR_NaMiginftauhGoutaum_list = np.load('max_I_K_DR_NaMiginftauhGoutaum_list.npy')*1e9
max_I_K_DR_NaMiginftaumGoutauh_list = np.load('max_I_K_DR_NaMiginftaumGoutauh_list.npy')*1e9

Gkwidth_NaTGou_list = np.load('Gkwidth_NaTGou_list.npy')*1e3
Gkwidth_NaTRoy_list = np.load('Gkwidth_NaTRoy_list.npy')*1e3
Gkwidth_NaMig_list = np.load('Gkwidth_NaMig_list.npy')*1e3
Gkwidth_NaMiginfGoutau_list = np.load('Gkwidth_NaMiginfGoutau_list.npy')*1e3
Gkwidth_NaMigtauGouinf_list = np.load('Gkwidth_NaMigtauGouinf_list.npy')*1e3
Gkwidth_NaMiginftauhGoutaum_list = np.load('Gkwidth_NaMiginftauhGoutaum_list.npy')*1e3
Gkwidth_NaMiginftaumGoutauh_list = np.load('Gkwidth_NaMiginftaumGoutauh_list.npy')*1e3

######### Panel C ########################
df = pd.DataFrame(columns=["type", "max I_K_DR (nA)"])
modeltype = (
    ["Gou"] * len(basemodels_NaTGou_list)
    + ["Roy"] * len(basemodels_NaTRoy_list)  
    + ["Mig"] * len(basemodels_NaMig_list)
    + [s_NaMiginfGoutau] * len(basemodels_NaMiginfGoutau_list)
    + [s_NaMigtauGouinf] * len(basemodels_NaMigtauGouinf_list)
    + [s_NaMiginftauhGoutaum] * len(basemodels_NaMiginftauhGoutaum_list)
    + [s_NaMiginftaumGoutauh] * len(basemodels_NaMiginftaumGoutauh_list)
)
max_I_K_DR = np.concatenate((max_I_K_DR_NaTGou_list,max_I_K_DR_NaTRoy_list,max_I_K_DR_NaMig_list, max_I_K_DR_NaMiginfGoutau_list, max_I_K_DR_NaMigtauGouinf_list, max_I_K_DR_NaMiginftauhGoutaum_list, max_I_K_DR_NaMiginftaumGoutauh_list))
df.loc[:, "type"] = modeltype
df.loc[:, "max I_K_DR (nA)"] = max_I_K_DR
df = df.convert_dtypes()

GouvsMigvsRoy_kruskal = scipy.stats.kruskal(
    list(df[df["type"] == "Gou"].loc[:, "max I_K_DR (nA)"]),
    list(df[df["type"] == "Roy"].loc[:, "max I_K_DR (nA)"]),
    list(df[df["type"] == "Mig"].loc[:, "max I_K_DR (nA)"]),
    # list(df[df["type"] == s_NaMiginfGoutau].loc[:, "max I_K_DR (nA)"]),
    # list(df[df["type"] == s_NaMigtauGouinf].loc[:, "max I_K_DR (nA)"]),
    # list(df[df["type"] == s_NaMiginftauhGoutaum].loc[:, "max I_K_DR (nA)"]),
    # list(df[df["type"] == s_NaMiginftaumGoutauh].loc[:, "max I_K_DR (nA)"]),
)
print('Kruskal-Wallis H-test ', GouvsMigvsRoy_kruskal)

GouvsMigvsRoy_dunn = sp.posthoc_dunn(df, val_col="max I_K_DR (nA)", group_col="type", p_adjust='bonferroni')

print('Dunn’s test\n', GouvsMigvsRoy_dunn)
print('Mean DBLO at 150pA\n', df.groupby('type').mean()["max I_K_DR (nA)"], df.groupby('type').std()["max I_K_DR (nA)"])

order = ["Gou", "Roy", "Mig", s_NaMiginfGoutau, s_NaMigtauGouinf, s_NaMiginftauhGoutaum, s_NaMiginftaumGoutauh]
palette = ["C2", "C8", "C3", "C4", "C5", "C1", "C9"]
ax = sns.boxplot(
    ax=axC,
    data=df,
    x="type",
    y="max I_K_DR (nA)",
    order=order,
    palette=palette,
    showfliers=False,
    zorder=2
)

# ax = sns.violinplot(ax=axD, data=df, x='type', y="max I_K_DR (nA)", order=order, palette=palette)
sns.stripplot(
    ax=ax,
    data=df,
    x="type",
    y="max I_K_DR (nA)",
    order=order,
    palette=palette,
    size=2,
    zorder=3
)
# plt.setp(ax.get_xticklabels(), rotation=90)
# ax.tick_params(axis='x', labelsize=8)
# Rotate only the last two tick labels
for label in ax.get_xticklabels()[-4:]:
    label.set_rotation(30)
    # label.set_ha('right')  # optional: align right
ax.set_xlabel("")  # Remove x-axis label
statannotator(
    axC,
    [0,1,3,4,5,6],
    df["max I_K_DR (nA)"].max()+1,
    [
        convert_pvalue_to_asterisks(a)
        for a in [GouvsMigvsRoy_dunn.loc["Mig", "Gou",], GouvsMigvsRoy_dunn.loc["Mig", "Roy"], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginfGoutau], GouvsMigvsRoy_dunn.loc["Mig", s_NaMigtauGouinf], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginftauhGoutaum], GouvsMigvsRoy_dunn.loc["Mig", s_NaMiginftaumGoutauh]]
    ],
)

axC.set_yscale('log')


############ Panel D #######################################################################
print('######## D ####################')

l1 = axD.scatter(max_I_K_DR_NaTGou_list, DBLO_NaTGou_list, label='Gou', c="C2", s=3)
print('Gou', scipy.stats.spearmanr(max_I_K_DR_NaTGou_list, DBLO_NaTGou_list))
l2 = axD.scatter(max_I_K_DR_NaTRoy_list, DBLO_NaTRoy_list, label='Roy', c="C8", s=3)
print('NaTRoy', scipy.stats.spearmanr(max_I_K_DR_NaTRoy_list, DBLO_NaTRoy_list))
l3 = axD.scatter(max_I_K_DR_NaMig_list, DBLO_NaMig_list, label='Mig', c="C3", s=3)
print('NaMig', scipy.stats.spearmanr(max_I_K_DR_NaMig_list, DBLO_NaMig_list))
l4 = axD.scatter(max_I_K_DR_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list, label=s_NaMiginfGoutau, c="C4", s=3)
print('NaMiginfGoutau', scipy.stats.spearmanr(max_I_K_DR_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list))
l5 = axD.scatter(max_I_K_DR_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list, label=s_NaMigtauGouinf, c="C5", s=3)
print('NaMigtauGouinf', scipy.stats.spearmanr(max_I_K_DR_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list))
l6 = axD.scatter(max_I_K_DR_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list, label=s_NaMiginftauhGoutaum, c="C1", s=3)
print('NaMiginftauhGoutaum', scipy.stats.spearmanr(max_I_K_DR_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list))
l7 = axD.scatter(max_I_K_DR_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list, label=s_NaMiginftaumGoutauh, c="C9", s=3)
print('NaMiginftaumGoutauh', scipy.stats.spearmanr(max_I_K_DR_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list))

print('All', scipy.stats.spearmanr(np.concatenate([max_I_K_DR_NaTGou_list,max_I_K_DR_NaTRoy_list,max_I_K_DR_NaMig_list,max_I_K_DR_NaMiginfGoutau_list,max_I_K_DR_NaMigtauGouinf_list,max_I_K_DR_NaMiginftauhGoutaum_list,max_I_K_DR_NaMiginftaumGoutauh_list]), 
    np.concatenate([DBLO_NaTGou_list,DBLO_NaTRoy_list,DBLO_NaMig_list,DBLO_NaMiginfGoutau_list,DBLO_NaMigtauGouinf_list,DBLO_NaMiginftauhGoutaum_list,DBLO_NaMiginftaumGoutauh_list])))

handles = [l1, l2, l3, l4, l5, l6, l7]
labels = ['Gou', 'Roy','Mig',s_NaMiginfGoutau,s_NaMigtauGouinf,s_NaMiginftauhGoutaum,s_NaMiginftaumGoutauh]
leg1 = axD.legend(handles[:3], labels[:3], loc='upper right', bbox_to_anchor=(0.7, 1.0), frameon=False)
leg2 = axD.legend(handles[3:], labels[3:], loc='upper right', bbox_to_anchor=(1.0, 1.0), frameon=False)
axD.add_artist(leg1)

axD.set_xlabel('Maximum K_DR current (nA)')
axD.set_ylabel('DBLO (mV)')
# axD.legend(frameon=False)
# axD.set_xscale('log')
# plt.setp(axD.get_xticklabels(), rotation=25)
# axD.tick_params(axis='x', labelrotation=25)


############ Panel E #######################################################################
print('######## E ####################')
l1 = axE.scatter(Gkwidth_NaTGou_list, DBLO_NaTGou_list, label='Gou', c="C2", s=3)
print('Gou', scipy.stats.spearmanr(Gkwidth_NaTGou_list, DBLO_NaTGou_list))
l2 = axE.scatter(Gkwidth_NaTRoy_list, DBLO_NaTRoy_list, label='Roy', c="C8", s=3)
print('NaTRoy', scipy.stats.spearmanr(Gkwidth_NaTRoy_list, DBLO_NaTRoy_list))
l3 = axE.scatter(Gkwidth_NaMig_list, DBLO_NaMig_list, label='Mig', c="C3", s=3)
print('NaMig', scipy.stats.spearmanr(Gkwidth_NaMig_list, DBLO_NaMig_list))
l4 = axE.scatter(Gkwidth_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list, label=s_NaMiginfGoutau, c="C4", s=3)
print('NaMiginfGoutau', scipy.stats.spearmanr(Gkwidth_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list))
l5 = axE.scatter(Gkwidth_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list, label=s_NaMigtauGouinf, c="C5", s=3)
print('NaMigtauGouinf', scipy.stats.spearmanr(Gkwidth_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list))
l6 = axE.scatter(Gkwidth_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list, label=s_NaMiginftauhGoutaum, c="C1", s=3)
print('NaMiginftauhGoutaum', scipy.stats.spearmanr(Gkwidth_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list))
l7 = axE.scatter(Gkwidth_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list, label=s_NaMiginftaumGoutauh, c="C9", s=3)
print('NaMiginftaumGoutauh', scipy.stats.spearmanr(Gkwidth_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list))

print('All', scipy.stats.spearmanr(np.concatenate([Gkwidth_NaTGou_list,Gkwidth_NaTRoy_list,Gkwidth_NaMig_list,Gkwidth_NaMiginfGoutau_list,Gkwidth_NaMigtauGouinf_list,Gkwidth_NaMiginftauhGoutaum_list,Gkwidth_NaMiginftaumGoutauh_list]), 
    np.concatenate([DBLO_NaTGou_list,DBLO_NaTRoy_list,DBLO_NaMig_list,DBLO_NaMiginfGoutau_list,DBLO_NaMigtauGouinf_list,DBLO_NaMiginftauhGoutaum_list,DBLO_NaMiginftaumGoutauh_list])))


# handles = [l1, l2, l3, l4, l5, l6, l7]
# labels = ['Gou', 'Roy','Mig',s_NaMiginfGoutau,s_NaMigtauGouinf,s_NaMiginftauhGoutaum,s_NaMiginftaumGoutauh]
# leg1 = axE.legend(handles[:3], labels[:3], loc='upper right', bbox_to_anchor=(0.7, 1.0), frameon=False)
# leg2 = axE.legend(handles[3:], labels[3:], loc='upper right', bbox_to_anchor=(1.0, 1.0), frameon=False)
# axE.add_artist(leg1)

axE.set_xlabel('Na_T open duration (ms)')
axE.set_ylabel('DBLO (mV)')
# axE.legend(frameon=False)
# axD.set_xscale('log')
# plt.setp(axD.get_xticklabels(), rotation=25)
# axD.tick_params(axis='x', labelrotation=25)

############ Panel F #######################################################################
print('######## F ####################')
l1 = axF.scatter(KDRGbar_NaTGou_list, DBLO_NaTGou_list, label='Gou', c="C2", s=3)
print('Gou', scipy.stats.spearmanr(KDRGbar_NaTGou_list, DBLO_NaTGou_list))
l2 = axF.scatter(KDRGbar_NaTRoy_list, DBLO_NaTRoy_list, label='Roy', c="C8", s=3)
print('NaTRoy', scipy.stats.spearmanr(KDRGbar_NaTRoy_list, DBLO_NaTRoy_list))
l3 = axF.scatter(KDRGbar_NaMig_list, DBLO_NaMig_list, label='Mig', c="C3", s=3)
print('NaMig', scipy.stats.spearmanr(KDRGbar_NaMig_list, DBLO_NaMig_list))
l4 = axF.scatter(KDRGbar_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list, label=s_NaMiginfGoutau, c="C4", s=3)
print('NaMiginfGoutau', scipy.stats.spearmanr(KDRGbar_NaMiginfGoutau_list, DBLO_NaMiginfGoutau_list))
l5 = axF.scatter(KDRGbar_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list, label=s_NaMigtauGouinf, c="C5", s=3)
print('NaMigtauGouinf', scipy.stats.spearmanr(KDRGbar_NaMigtauGouinf_list, DBLO_NaMigtauGouinf_list))
l6 = axF.scatter(KDRGbar_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list, label=s_NaMiginftauhGoutaum, c="C1", s=3)
print('NaMiginftauhGoutaum', scipy.stats.spearmanr(KDRGbar_NaMiginftauhGoutaum_list, DBLO_NaMiginftauhGoutaum_list))
l7 = axF.scatter(KDRGbar_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list, label=s_NaMiginftaumGoutauh, c="C9", s=3)
print('NaMiginftaumGoutauh', scipy.stats.spearmanr(KDRGbar_NaMiginftaumGoutauh_list, DBLO_NaMiginftaumGoutauh_list))

print('All', scipy.stats.spearmanr(np.concatenate([KDRGbar_NaTGou_list,KDRGbar_NaTRoy_list,KDRGbar_NaMig_list,KDRGbar_NaMiginfGoutau_list,KDRGbar_NaMigtauGouinf_list,KDRGbar_NaMiginftauhGoutaum_list,KDRGbar_NaMiginftaumGoutauh_list]), 
    np.concatenate([DBLO_NaTGou_list,DBLO_NaTRoy_list,DBLO_NaMig_list,DBLO_NaMiginfGoutau_list,DBLO_NaMigtauGouinf_list,DBLO_NaMiginftauhGoutaum_list,DBLO_NaMiginftaumGoutauh_list])))


# handles = [l1, l2, l3, l4, l5, l6, l7]
# labels = ['Gou', 'Roy','Mig',s_NaMiginfGoutau,s_NaMigtauGouinf,s_NaMiginftauhGoutaum,s_NaMiginftaumGoutauh]
# leg1 = axF.legend(handles[:3], labels[:3], loc='upper right', bbox_to_anchor=(0.7, 1.0), frameon=False)
# leg2 = axF.legend(handles[3:], labels[3:], loc='upper right', bbox_to_anchor=(1.0, 1.0), frameon=False)
# axF.add_artist(leg1)

axF.set_xlabel('K_DR Gbar (µS)')
axF.set_ylabel('DBLO (mV)')
# axF.legend(frameon=False)
# axD.set_xscale('log')
# plt.setp(axD.get_xticklabels(), rotation=25)
# axD.tick_params(axis='x', labelrotation=25)

############ Panel G #######################################################################
print('######## G ####################')
l1 = axG.scatter(AP1_width_nowidth_NaTGou_list, DBLO_nowidth_NaTGou_list, label='Gou', c="C2", s=3)
print('Gou', scipy.stats.spearmanr(AP1_width_nowidth_NaTGou_list, DBLO_nowidth_NaTGou_list))
l2 = axG.scatter(AP1_width_nowidth_NaTRoy_list, DBLO_nowidth_NaTRoy_list, label='Roy', c="C8", s=3)
print('NaTRoy', scipy.stats.spearmanr(AP1_width_nowidth_NaTRoy_list, DBLO_nowidth_NaTRoy_list))
l3 = axG.scatter(AP1_width_nowidth_NaMig_list, DBLO_nowidth_NaMig_list, label='Mig', c="C3", s=3)
print('NaMig', scipy.stats.spearmanr(AP1_width_nowidth_NaMig_list, DBLO_nowidth_NaMig_list))
l4 = axG.scatter(AP1_width_nowidth_NaMiginfGoutau_list, DBLO_nowidth_NaMiginfGoutau_list, label=s_NaMiginfGoutau, c="C4", s=3)
print('NaMiginfGoutau', scipy.stats.spearmanr(AP1_width_nowidth_NaMiginfGoutau_list, DBLO_nowidth_NaMiginfGoutau_list))
l5 = axG.scatter(AP1_width_nowidth_NaMigtauGouinf_list, DBLO_nowidth_NaMigtauGouinf_list, label=s_NaMigtauGouinf, c="C5", s=3)
print('NaMigtauGouinf', scipy.stats.spearmanr(AP1_width_nowidth_NaMigtauGouinf_list, DBLO_nowidth_NaMigtauGouinf_list))
l6 = axG.scatter(AP1_width_nowidth_NaMiginftauhGoutaum_list, DBLO_nowidth_NaMiginftauhGoutaum_list, label=s_NaMiginftauhGoutaum, c="C1", s=3)
print('NaMiginftauhGoutaum', scipy.stats.spearmanr(AP1_width_nowidth_NaMiginftauhGoutaum_list, DBLO_nowidth_NaMiginftauhGoutaum_list))
l7 = axG.scatter(AP1_width_nowidth_NaMiginftaumGoutauh_list, DBLO_nowidth_NaMiginftaumGoutauh_list, label=s_NaMiginftaumGoutauh, c="C9", s=3)
print('NaMiginftaumGoutauh', scipy.stats.spearmanr(AP1_width_nowidth_NaMiginftaumGoutauh_list, DBLO_nowidth_NaMiginftaumGoutauh_list))

print('All', scipy.stats.spearmanr(np.concatenate([AP1_width_nowidth_NaTGou_list,AP1_width_nowidth_NaTRoy_list,AP1_width_nowidth_NaMig_list,AP1_width_nowidth_NaMiginfGoutau_list,AP1_width_nowidth_NaMigtauGouinf_list,AP1_width_nowidth_NaMiginftauhGoutaum_list,AP1_width_nowidth_NaMiginftaumGoutauh_list]), 
    np.concatenate([DBLO_nowidth_NaTGou_list,DBLO_nowidth_NaTRoy_list,DBLO_nowidth_NaMig_list,DBLO_nowidth_NaMiginfGoutau_list,DBLO_nowidth_NaMigtauGouinf_list,DBLO_nowidth_NaMiginftauhGoutaum_list,DBLO_nowidth_NaMiginftaumGoutauh_list])))

# handles = [l1, l2, l3, l4, l5, l6, l7]
# labels = ['Gou', 'Roy','Mig',s_NaMiginfGoutau,s_NaMigtauGouinf,s_NaMiginftauhGoutaum,s_NaMiginftaumGoutauh]
# leg1 = axG.legend(handles[:3], labels[:3], loc='upper right', bbox_to_anchor=(0.7, 1.0), frameon=False)
# leg2 = axG.legend(handles[3:], labels[3:], loc='upper right', bbox_to_anchor=(1.0, 1.0), frameon=False)
# axG.add_artist(leg1)

axG.axvspan(df_expsummaryactiveF['10th quantile']["AP1_width_1.5e-10"]*1e3, df_expsummaryactiveF['90th quantile']["AP1_width_1.5e-10"]*1e3, color='C9', alpha=0.3)

axG.set_xlabel('AP1 width (ms)')
axG.set_ylabel('DBLO (mV)')
# axG.legend(frameon=False)
# axD.set_xscale('log')
# plt.setp(axD.get_xticklabels(), rotation=25)
# axD.tick_params(axis='x', labelrotation=25)


######################

sns.despine(fig=fig)
axA[0].spines["bottom"].set_visible(False)
plt.subplots_adjust(left=0.150)
# plt.tight_layout()
plt.savefig('Fig8.png', dpi=300)
# plt.savefig('Fig8.pdf', dpi=300)
plt.show()

# f.write(f'Max DBLO in Gou - {np.max(df[df["type"] == "Gou"].loc[:, "DBLO150 (mV)"])}\n')
# f.write(f'Number of Models in Gou - {len(df[df["type"] == "Gou"])}\n')
# f.write(f'Number of high DBLO Models in Gou - {len(df[df["type"] == "Gou"][df["DBLO150 (mV)"] > 14.3])}\n')
# f.write(f'Number of moderate DBLO Models in Gou - {len(df[df["type"] == "Gou"][(df["DBLO150 (mV)"] <= 14.3) & (df["DBLO150 (mV)"] > 10)])}\n')
# f.write(f'DBLO vs Na_T mvhalf - {r:1.2f}, {pvalue:1.2e}\n')

