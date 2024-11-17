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
import MOOSEModel as mm
from matplotlib.cm import viridis, tab20, tab20c
from matplotlib.colors import to_rgba
from copy import deepcopy

import statsmodels.formula.api as smf
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

sns.set(style="ticks")
sns.set_context("paper")
plt.rcParams['xtick.labelsize']='small'
plt.rcParams['ytick.labelsize']='small'

def add_caxes(fig, rect):
    '''
    rect - > [x_upperleft, y_upperleft, x_lowerright, y_lowerright]
    (0,0) is situated at upper left corner of the figure
    '''
    x_upperleft, y_upperleft, x_lowerright, y_lowerright = rect
    return fig.add_axes([x_upperleft, 1-y_lowerright, x_lowerright- x_upperleft, y_lowerright- y_upperleft])


# Create a figure
fig = plt.figure(figsize=(8, 10))
# fig = plt.figure(figsize=(6, 10))

# Define the subplot positions (using [x_upperleft, y_upperleft, x_lowerright, y_lowerright] format)
axA = add_caxes(fig, [0.1, 0.05, 0.375, 0.25])
axB = add_caxes(fig, [0.425, 0.05, 0.70, 0.25])
axC_CaL = add_caxes(fig, [0.8, 0.05, 1.0, 0.2375])
axC_CaN = add_caxes(fig, [0.8, 0.2875, 1.0, 0.475])
axC_CaR = add_caxes(fig, [0.8, 0.525, 1.0, 0.7125])
axC_CaT = add_caxes(fig, [0.8, 0.7625, 1.0, 0.95])
axD_rephighDBLO = add_caxes(fig, [0.1, 0.35, 0.375, 0.58])
axD_rephighDBLOcurr = add_caxes(fig, [0.1, 0.6, 0.375, 0.65])
axD_DBLOvsNaP = add_caxes(fig, [0.425, 0.35, 0.7, 0.65])
axE_DBLOvsGk = add_caxes(fig, [0.1, 0.75, 0.35, 0.95])
axE_rep = add_caxes(fig, [0.45, 0.75, 0.7, 0.95])
axE_ill = add_caxes(fig, [0.47, 0.77, 0.58, 0.93])
# gs_outer = GridSpec(5, 2, figure=fig, height_ratios=[1, 1, 1, 1, 1], wspace=0.5, hspace=0.5)
# axA = fig.add_subplot(gs_outer[0, 0])
# axB = fig.add_subplot(gs_outer[0, 1])
# axC_CaL = fig.add_subplot(gs_outer[1, 0])
# axC_CaN = fig.add_subplot(gs_outer[1, 1])
# axC_CaR = fig.add_subplot(gs_outer[2, 0])
# axC_CaT = fig.add_subplot(gs_outer[2, 1])
# gs_D_repbis= gs_outer[3, 0].subgridspec(
#     2, 1, height_ratios=[3, 1], wspace=0.1, hspace=0.5
# )
# axD_rephighDBLO = fig.add_subplot(gs_D_repbis[0, 0])
# axD_rephighDBLOcurr = fig.add_subplot(gs_D_repbis[1, 0])
# axD_DBLOvsNaP = fig.add_subplot(gs_outer[3, 1])
# axE_DBLOvsGk = fig.add_subplot(gs_outer[4, 0])
# axE_rep =  fig.add_subplot(gs_outer[4, 1])
# axE_ill = add_caxes(fig, [0.47, 0.77, 0.58, 0.93])

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA, axB, axC_CaL, axD_rephighDBLO, axE_DBLOvsGk]):
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
for i, ax in enumerate([axC_CaL, axC_CaN, axC_CaR, axC_CaT]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig
    y_infig = y_infig + 20
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

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axD_rephighDBLO, axD_rephighDBLOcurr, axD_DBLOvsNaP]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig
    y_infig = y_infig + 20
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

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axE_DBLOvsGk, axE_rep]):
    x_infig, y_infig = ax.transAxes.transform([0,1])
    x_infig = x_infig
    y_infig = y_infig + 20
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

NOTESf = open('NOTES.txt', 'w')
######## Panel A ######################
df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

basemodel_unified_list = []
file_path = "activemodels_imp_Eb2_NaTallen.json"
with open(file_path, "r") as file:
    for line in tqdm(file):
        basemodel = json.loads(line)
        if (basemodel["Features"]["AP1_amp_1.5e-10"]>=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "10th quantile"]) & (basemodel["Features"]["AP1_amp_1.5e-10"]<=df_expsummaryactiveF.loc["AP1_amp_1.5e-10", "90th quantile"]):
            basemodel_unified_list.append(basemodel)

DBLO_list = np.array([a["Features"]["DBLO_1.5e-10"] for a in basemodel_unified_list])
highDBLOmodel = np.array(basemodel_unified_list)[np.argsort(DBLO_list)[-1]]
stim_start = 0.5
tvec, _, Vmvec, _ = mm.runModel(highDBLOmodel, 150e-12, refreshKin=True)
axA.plot((tvec-stim_start)*1e3, Vmvec*1e3, color='C2', label='high DBLO')
axA.set_xlabel('Time (ms)')
axA.set_ylabel('Voltage (mV)')
axA.set_xlim(-0.1*1e3, 0.6*1e3)
axA.set_ylim(-100e-3*1e3, 60e-3*1e3)
axA.set_title("Representative \n high DBLO model")
print(highDBLOmodel["Features"]["DBLO_1.5e-10"], sum(DBLO_list>14.3e-3))
NOTESf.write(f'{highDBLOmodel["Features"]["DBLO_1.5e-10"] = }\n')
NOTESf.write(f'{sum(DBLO_list>14.3e-3) = }\n')

#######################################
################## Panel B#####################
Na_T_Chan_Gbar = [a["Parameters"]["Channels"]["Na_T_Chan"]["Gbar"]*1e6 for a in basemodel_unified_list]
K_DR_Chan_Gbar = [a["Parameters"]["Channels"]["K_DR_Chan"]["Gbar"]*1e6 for a in basemodel_unified_list]
Gbarratio = np.array(Na_T_Chan_Gbar)/np.array(K_DR_Chan_Gbar)
spikes = [a["Features"]["freq_1.5e-10"] / 2 for a in basemodel_unified_list]
baseID_list = np.array([a["Parameters"]["notes"] for a in basemodel_unified_list])

tempdict = {"Gbarratio":Gbarratio, "DBLO":DBLO_list, "spikes":spikes, "baseID":baseID_list}
tempdata = pd.DataFrame(tempdict)
md = smf.mixedlm("Gbarratio ~ DBLO", tempdata, groups=tempdata["baseID"])
# mdf = md.fit(method=['powell', 'nm', 'bfgs'], maxiter=10000, xtol=1e-4)
mdf = md.fit()
print(mdf.summary())
print(mdf.random_effects)
print(mdf.pvalues)
NOTESf.write(f'{mdf.summary()=}\n')
NOTESf.write(f'{mdf.random_effects=}\n')
NOTESf.write(f'{mdf.pvalues=}\n')


cmap = tab20
norm = plt.Normalize(0, len(set(baseID_list)) - 1)
colors = np.array([cmap(norm(list(tempdata['baseID'].unique()).index(label))) for label in baseID_list])
# Scatter plot of the observed data
for i,baseID in enumerate(tempdata['baseID'].unique()):
    baseID_data = tempdata[tempdata['baseID'] == baseID]
    c = colors[baseID_list==baseID]
    # axB.scatter(baseID_data['DBLO'], baseID_data['Gbarratio'], label=f'{i}', c=c, s=3, alpha=0.6)
    axB.scatter(baseID_data['DBLO'], baseID_data['Gbarratio'], c=c, s=3, alpha=0.6)

# Fitted line for the fixed effect
x = np.linspace(tempdata['DBLO'].min(), tempdata['DBLO'].max(), 100)
y = mdf.params['Intercept'] + mdf.params['DBLO'] * x
axB.plot(x, y, '--', color='black', label='Fixed effect')

# Random effects for each baseID
random_effects = mdf.random_effects
for baseID, re in random_effects.items():
    c = colors[baseID_list==baseID]
    x = np.linspace(tempdata[tempdata["baseID"]==baseID]['DBLO'].min(), tempdata[tempdata["baseID"]==baseID]['DBLO'].max(), 100)
    # axB.plot(x, mdf.params['Intercept'] + re['Group'] + re['DBLO'] * x, label=f'Random Effect {baseID}')
    axB.plot(x, mdf.params['Intercept'] + re['Group'] + mdf.params['DBLO'] * x, c=c[0])

axB.plot(0,0, color= 'black', label='Random effects')

axB.set_xlabel('DBLO (mV)')
axB.set_ylabel(r'$\frac{Na\_T\_Chan\_Gbar}{K\_DR\_Chan\_Gbar}$')
# axB.legend(frameon=False, title="Base imp model id", loc='center left', bbox_to_anchor=(1, 0.5),  markerscale=2)
axB.legend(frameon=False)
################################################################################################################

#### Panel C ###################################################################################################
Cachan_axeslist = [axC_CaL, axC_CaN, axC_CaR, axC_CaT]
for ii,Cachan in enumerate(['CaL', 'CaN', 'CaR', 'CaT']):
    # i_list = []
    # with open(f'{Cachan}/i.pkl', "rb") as f:
    #     while True:
    #         try:
    #             i_list.append(pickle.load(f))
    #         except Exception:
    #             break
    # i_list_argsort = np.argsort(i_list)

    # tvec_list = []
    # with open(f'{Cachan}/tvec.pkl', "rb") as f:
    #     while True:
    #         try:
    #             tvec_list.append(pickle.load(f))
    #         except Exception:
    #             break
    # tvec_list = np.array(tvec_list)[i_list_argsort]

    # # Vmvec_list = []
    # # with open(f'{Cachan}/Vmvec.pkl', "rb") as f:
    # #     while True:
    # #         try:
    # #             Vmvec_list.append(pickle.load(f))
    # #         except Exception:
    # #             break
    # # Vmvec_list = np.array(Vmvec_list)[i_list_argsort]

    # Cavec_list = []
    # with open(f'{Cachan}/Cavec.pkl', "rb") as f:
    #     while True:
    #         try:
    #             Cavec_list.append(pickle.load(f))
    #         except Exception:
    #             break
    # Cavec_list = np.array(Cavec_list)[i_list_argsort]

    # medianCa_list = np.array([np.median(Cavec_list[i][(tvec_list[i]>0.5) & (tvec_list[i]<=1)]) for i in range(len(Cavec_list))])
    with open(f'{Cachan}/medianCa.pkl', "rb") as f:
        medianCa_list = pickle.load(f)

    Cachan_axeslist[ii].scatter(DBLO_list*1e3, medianCa_list*1e6, color='C7', s=3)
    Cachan_axeslist[ii].set_title(Cachan)
    Cachan_axeslist[ii].get_xaxis().set_visible(False)
    # Cachan_axeslist[ii].xlabel('DBLO (mV)')
    Cachan_axeslist[ii].set_ylabel('Median Ca conc (nM)')
    m, b, r, pvalue, _ = scs.linregress(np.array(DBLO_list*1e3), medianCa_list*1e6)
    NOTESf.write(f'DBLO vs {Cachan} = {m, b, r, pvalue}\n')

# axC_CaR.set_ylabel('Median Ca conc (nM)')
axC_CaT.set_xlabel('DBLO (mV)')
axC_CaT.get_xaxis().set_visible(True)

################################################################################################################
######## Panel D ########################################################################################################

minNaP_list_unified = np.load('Na_P_Gbar_lowerbound_bistable_unified.npy', allow_pickle=True)

repbismodel = deepcopy(basemodel_unified_list[-1])
repbismodel["Parameters"]["Channels"]["Na_P_Chan"] = {
                "Gbar": 1e-9,
                "Erev": 0.060,
                "Kinetics": "../Kinetics/Na_P_Chan_Migliore2018",
                "KineticVars": {"mvhalf": -50.4e-3, "mvslope": 4.53e-3}, #Migliore - {"mvhalf": -52.3e-3, "mvslope": 6.8e-3} #Brown1994 - {"mvhalf": -50.4e-3, "mvslope": 4.53e-3}
            }

repbismodel["Parameters"]["Channels"]["Na_P_Chan"]["Gbar"] = minNaP_list_unified[-1]

stim_start = 0.5
stim_end = 1
stimlist_bis = [
    "soma",
    "1",
    ".",
    "inject",
    f"(t>{stim_start} & t<{stim_start+0.5}) * {150e-12} + (t>{stim_start+1} & t<{stim_start+1.5}) * {-50e-12}",
]
tvec, Ivec, Vmvec, Ca = mm.runModel(repbismodel, CurrInjection=stimlist_bis, Truntime=2.5)

axD_rephighDBLO.plot(tvec*1e3, Vmvec*1e3, c='C7')
axD_rephighDBLO.set_ylabel('Voltage (mV)')
axD_rephighDBLO.get_xaxis().set_visible(False)
axD_rephighDBLO.set_title('Representative \n bistable model')

axD_rephighDBLOcurr.plot(tvec*1e3, Ivec*1e12, c='black')
axD_rephighDBLOcurr.set_xlabel('Time (ms)')
axD_rephighDBLOcurr.set_ylabel('Current (pA)')

# Filter out pairs where either value is None
filtered_pairs = [(x, y) for x, y in zip(DBLO_list, minNaP_list_unified) if x is not None and y is not None]
DBLO_list_filtered_unified, minNaP_list_filtered_unified = zip(*filtered_pairs)

axD_DBLOvsNaP.scatter(np.array(DBLO_list)*1e3, [x *1e9 if x is not None else None for x in minNaP_list_unified], color='C7', label=r'$\it{bistable}$', s=3)
axD_DBLOvsNaP.set_xlabel('DBLO at 150 pA (mV)')
axD_DBLOvsNaP.set_ylabel('Na_P_Chan_Gbar (nS)')
axD_DBLOvsNaP.set_title('Minimum Na_P_Chan_Gbar \n needed for bistability')
# axD_DBLOvsNaP.legend(frameon=False)
# axD_DBLOvsNaP.text(5,80, f'r = {np.corrcoef([DBLO_list_filtered_unified, minNaP_list_filtered_unified])[0][1]:.2f}')
NOTESf.write(f'DBLO_list_filtered_unified vs minNaP_list_filtered_unified = {np.corrcoef([DBLO_list_filtered_unified, minNaP_list_filtered_unified])[0][1]:.2f}\n')

def replaceNone(array, replacer):
    if replacer!=None:
        return np.array([x if x is not None else replacer for x in array])
    else:
        return np.array([x for x in array if x is not None])

highDBLO_minNaP = replaceNone(minNaP_list_unified[np.array(DBLO_list)>14.3e-3], None)
lowDBLO_minNaP = replaceNone(minNaP_list_unified[np.array(DBLO_list)<=10e-3], None)
t_stat, p_value = scs.ttest_ind(highDBLO_minNaP, lowDBLO_minNaP, equal_var=False)
NOTESf.write(f'{np.nanmean(highDBLO_minNaP) =:.2e}, {np.nanstd(highDBLO_minNaP) =:.2e}\n')
NOTESf.write(f'{np.nanmean(lowDBLO_minNaP) =:.2e}, {np.nanstd(lowDBLO_minNaP) =:.2e}\n')
NOTESf.write(f'highDBLO_minNaP vs lowDBLO_minNaP ttest {p_value =:.3e}\n')

################################################################################################################
###### Panel E #################################################################################################
gapmodel_imp_list = []
file_path = 'Models_gapjuncfeatures_par_300pA.json'
with open(file_path, "r") as file:
    for line in tqdm(file):
        gapmodel = json.loads(line)
        gapmodel_imp_list.append(gapmodel)

Gk0list = np.array([a["gapjuncfeatures"]["minGk0"] for a in gapmodel_imp_list])
Gk1list = np.array([a["gapjuncfeatures"]["minGk1"] for a in gapmodel_imp_list])
DBLO300list = np.array([a["Features"]["DBLO_3e-10"] for a in gapmodel_imp_list])

axE_DBLOvsGk.scatter(DBLO300list*1e3, Gk0list*1e9, label=r'$Gk_{min}$ for AP1', color='C5', s=3)
axE_DBLOvsGk.scatter(DBLO300list*1e3, Gk1list*1e9, label=r'$Gk_{min}$ for AP2', color='C6', s=3)
axE_DBLOvsGk.legend(frameon=False)
axE_DBLOvsGk.set_xlabel('DBLO at 300 pA (mV)')
axE_DBLOvsGk.set_ylabel('Gap junction conductance (nS)')

m, b, r, pvalue, _ = scs.linregress(DBLO300list*1e3, Gk0list*1e9)
NOTESf.write(f'DBLO300 vs Gkmin 1 = {m, b, r, pvalue}\n')
m, b, r, pvalue, _ = scs.linregress(DBLO300list*1e3, Gk1list*1e9)
NOTESf.write(f'DBLO300 vs Gkmin 2 = {m, b, r, pvalue}\n')

_ = np.load('Vmvec_gap.npz') #Load the stored Vm traces of gap junction neurons generated by gapjunction_singletrace.py
tvec_gap, Vmvec1_gap, Vmvec2_gap = _['tvec_gap'], _['Vmvec1_gap'], _['Vmvec2_gap']

axE_rep.plot(np.array(tvec_gap)*1e3, np.array(Vmvec1_gap)*1e3, label='Neuron 1', color='C4')
axE_rep.plot(np.array(tvec_gap)*1e3, np.array(Vmvec2_gap)*1e3, label='Neuron 2', color='C8')
axE_rep.set_xlabel('Time (ms)')
axE_rep.set_ylabel('Membrane potential (mV)')
axE_rep.set_xlim(450, 600)
axE_rep.set_ylim(-85, 40)
axE_rep.legend(frameon=False)
axE_rep.set_title('Representative neuron pairs \n showing spikelets')

image = plt.imread('Gap_junction.png')
axE_ill.imshow(image, aspect='equal')
axE_ill.axis('off')

################################################################################################################
######################
sns.despine(fig=fig)
axC_CaL.spines['bottom'].set_visible(False)
axC_CaN.spines['bottom'].set_visible(False)
axC_CaR.spines['bottom'].set_visible(False)
axD_rephighDBLO.spines['bottom'].set_visible(False)
# # plt.tight_layout()
plt.savefig('Fig9.png', dpi=300)
# # plt.savefig('Fig8.pdf', dpi=300)
plt.show()

NOTESf.close()