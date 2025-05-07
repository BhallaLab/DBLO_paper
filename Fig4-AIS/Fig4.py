import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy.signal import butter, filtfilt
from pprint import pprint
import os
import pickle
import json
from goMultiprocessing import Multiprocessthis_appendsave
from copy import deepcopy
import MOOSEModel_ as mm
import os
import subprocess
import scipy.stats as scs
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import statsmodels.formula.api as smf
import scipy.stats as sst
import moose
import matplotlib.image as mpimg

sns.set(style="ticks")
sns.set_context("paper")

fig = plt.figure(figsize=(7, 9), constrained_layout=False)
# fig = plt.figure(constrained_layout=True)
gs = GridSpec(3, 2, figure=fig)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, 0])

subgs = gs[1, 1].subgridspec(2, 1, hspace=0.1, height_ratios=[0.35, 0.65])
axDhigh = fig.add_subplot(subgs[0,0])
axDlow = fig.add_subplot(subgs[1,0])

axE = fig.add_subplot(gs[2, 0])

subgs = gs[2, 1].subgridspec(2, 1, hspace=0.1, height_ratios=[0.35, 0.65])
axFhigh = fig.add_subplot(subgs[0,0])
axFlow = fig.add_subplot(subgs[1,0])

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA, axB, axC, axDhigh, axE, axFhigh]):
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

f = open('NOTES.txt', 'w')
#######################################

#############Panel A############################
image = plt.imread('AISsoma_Anzal.png')
position = axA.get_position()
Aposition = axA.transAxes.transform(axA.get_children()[0].get_position())
axA.imshow(image, aspect='auto')
left, bottom, width, height = position.x0, position.y0, position.width, position.height
zoom = 1
axA.set_position((left, bottom+height-zoom*height, width*image.shape[0]/image.shape[1]*zoom, height*zoom ))
axA.get_children()[0].set_position(axA.transAxes.inverted().transform(Aposition))
axA.axis('off')
#######################################


###### Panel B C ############################
# Load models from the JSON file
basemodels_list = []
file_path = "activemodels_activeAIS.json"
with open(file_path, "r") as file:
    for line in file:
        basemodel = json.loads(line)
        basemodels_list.append(basemodel)

print(f'Number of valid activeAIS models: {len(basemodels_list)}')

DBLO_150pA_list = []
AP1amp_150pA_list = []
RA_list = []
for model in basemodels_list:
    DBLO_150pA_list.append(model["Features"]["DBLO_1.5e-10"])
    AP1amp_150pA_list.append(model["Features"]["AP1_amp_1.5e-10"])
    RA_list.append(model["Parameters"]["Passive"]["sm_RA"])

axB.scatter(RA_list, np.array(DBLO_150pA_list)*1e3, c='C7', s=4)
axB.set_xlabel(r'RA ($\Omega$m)')
axB.set_ylabel('DBLO (mV)')
axB.set_xscale('log')

axC.scatter(RA_list, np.array(AP1amp_150pA_list)*1e3, c='C7', s=4)
axC.set_ylabel(r'Spike height (mV)')
axC.set_xlabel(r'RA ($\Omega$m)')
axC.set_xscale('log')


highDBLOmodelidx = np.argsort(DBLO_150pA_list)[-1]
lowDBLOmodelidx = np.argsort(DBLO_150pA_list)[0]
highDBLOmodel = basemodels_list[highDBLOmodelidx]
lowDBLOmodel = basemodels_list[lowDBLOmodelidx]

# pprint(highDBLOmodel)
t150, Itrace150, Vtrace150, Ca = mm.runModel(highDBLOmodel, 150e-12, refreshKin=True)
axDhigh.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='high DBLO', c='C2')
axDhigh.set_xlim(400, 1500)
axDhigh.legend(frameon=False, loc='center right')
axDhigh.set_title("Representative models")
axDhigh.tick_params(labelleft=True, labelbottom=False, bottom = False, left=True)
t150, Itrace150, Vtrace150, Ca = mm.runModel(lowDBLOmodel, 150e-12, refreshKin=True)
axDlow.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='low DBLO', c='C3')
axDlow.set_xlabel("Time (ms)")
axDlow.set_ylabel("Voltage (mV)")
axDlow.set_xlim(400, 1500)
axDlow.legend(frameon=False, loc='center right')

axB.scatter(RA_list[highDBLOmodelidx], np.array(DBLO_150pA_list)[highDBLOmodelidx]*1e3, c='C2', s=100, marker='X')
axB.scatter(RA_list[lowDBLOmodelidx], np.array(DBLO_150pA_list)[lowDBLOmodelidx]*1e3, c='C3', s=100, marker='X')
axC.scatter(RA_list[highDBLOmodelidx], np.array(AP1amp_150pA_list)[highDBLOmodelidx]*1e3, c='C2', s=100, marker='X')
axC.scatter(RA_list[lowDBLOmodelidx], np.array(AP1amp_150pA_list)[lowDBLOmodelidx]*1e3, c='C3', s=100, marker='X')


############# Stats #####################
m_DBLO, b_DBLO, r_DBLO, pvalue_DBLO, _ = scs.linregress(RA_list, np.array(DBLO_150pA_list)*1e3)
print(f'{r_DBLO:1.2f}', f'{pvalue_DBLO:1.2e}')
m_amp, b_amp, r_amp, pvalue_amp, _ = scs.linregress(RA_list, np.array(AP1amp_150pA_list)*1e3)
print(f'{r_amp:1.2f}', f'{pvalue_amp:1.2e}')

############ Write to NOTES.txt ###############
f.write(f'RA vs DBLO linear regressin - {r_DBLO:1.2f}, pvalue {pvalue_DBLO:1.2e}\n')
f.write(f'RA vs AP1 amp linear regressin - {r_amp:1.2f}, pvalue {pvalue_amp:1.2e}\n')
f.write(f"Highest DBLO model's DBLO - {np.array(DBLO_150pA_list)[highDBLOmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[highDBLOmodelidx]*1e3} mV and RA - {RA_list[highDBLOmodelidx]}\n")
f.write(f"Lowest DBLO model's DBLO - {np.array(DBLO_150pA_list)[lowDBLOmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[lowDBLOmodelidx]*1e3} mV and RA - {RA_list[lowDBLOmodelidx]}\n")


############### Panel E and F ####################################################################################################

# Load models from the JSON file
basemodels_list = []
file_path = "activemodels_activeAIS+soma.json"
with open(file_path, "r") as file:
    for line in file:
        basemodel = json.loads(line)
        basemodels_list.append(basemodel)

print(f'Number of valid activeAIS+activesoma models: {len(basemodels_list)}')

DBLO_150pA_list = []
AP1amp_150pA_list = []
RA_list = []
for model in basemodels_list:
    DBLO_150pA_list.append(model["Features"]["DBLO_1.5e-10"])
    AP1amp_150pA_list.append(model["Features"]["AP1_amp_1.5e-10"])
    RA_list.append(model["Parameters"]["Passive"]["sm_RA"])


df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

axE.axvspan(14.3, 23.6, color='C2', alpha=0.3)
axE.axvspan(10, 14.3, color='C8', alpha=0.3)
axE.axhspan(df_expsummaryactiveF['10th quantile']["AP1_amp_1.5e-10"]*1e3, df_expsummaryactiveF['90th quantile']["AP1_amp_1.5e-10"]*1e3, color='C9', alpha=0.3)
axE.scatter(np.array(DBLO_150pA_list)*1e3, np.array(AP1amp_150pA_list)*1e3, c='C7', s=4)
axE.set_ylabel(r'Spike height (mV)')
axE.set_xlabel('DBLO (mV)')

m_DBLOvsAP1amp, b_DBLOvsAP1amp, r_DBLOvsAP1amp, pvalue_DBLOvsAP1amp, _ = sst.linregress(np.array(DBLO_150pA_list)*1e3, np.array(AP1amp_150pA_list)*1e3)

inset_ax = inset_axes(axE,
                      width="50%",  # width as a % of parent_bbox
                      height="50%", # height as a % of parent_bbox
                      loc='upper center',  # location inside the axes
                      bbox_to_anchor=(0.1, 0.2, 1, 1),  # (x0, y0, width, height)
                      bbox_transform=axE.transAxes,
                      borderpad=2)

img = mpimg.imread('soma_dendrite_back_propagation_Anal.png')  # or .jpg, etc.
inset_ax.imshow(img)
inset_ax.axis('off')


#### Panel f #########################
highDBLOmodelidx = np.argsort(DBLO_150pA_list)[-1]
lowDBLOmodelidx = np.argsort(DBLO_150pA_list)[0]
highDBLOmodel = basemodels_list[highDBLOmodelidx]
lowDBLOmodel = basemodels_list[lowDBLOmodelidx]

moose.delete('library')
t150, Itrace150, Vtrace150, Ca = mm.runModel(highDBLOmodel, 150e-12, refreshKin=True)
axFhigh.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='high DBLO', c='C2')
axFhigh.set_xlim(400, 1500)
axFhigh.legend(frameon=False, loc='center right')
axFhigh.set_title("Representative models")
axFhigh.tick_params(labelleft=True, labelbottom=False, bottom = False, left=True)
t150, Itrace150, Vtrace150, Ca = mm.runModel(lowDBLOmodel, 150e-12, refreshKin=True)
axFlow.plot(np.array(t150)*1e3, np.array(Vtrace150)*1e3, label='low DBLO', c='C3')
axFlow.set_xlabel("Time (ms)")
axFlow.set_ylabel("Voltage (mV)")
axFlow.set_xlim(400, 1500)
axFlow.legend(frameon=False, loc='center right')

axE.scatter(np.array(DBLO_150pA_list)[highDBLOmodelidx]*1e3, np.array(AP1amp_150pA_list)[highDBLOmodelidx]*1e3, c='C2', s=100, marker='X')
axE.scatter(np.array(DBLO_150pA_list)[lowDBLOmodelidx]*1e3, np.array(AP1amp_150pA_list)[lowDBLOmodelidx]*1e3, c='C3', s=100, marker='X')



#####################
############ Write to NOTES.txt ###############

f.write(f'DBLO vs AP1 amp linear regressin - {r_DBLOvsAP1amp:1.2f}, pvalue {pvalue_DBLOvsAP1amp:1.2e}\n')
f.write(f"Highest DBLO model's DBLO - {np.array(DBLO_150pA_list)[highDBLOmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[highDBLOmodelidx]*1e3} mV and RA - {RA_list[highDBLOmodelidx]}\n")
f.write(f"Lowest DBLO model's DBLO - {np.array(DBLO_150pA_list)[lowDBLOmodelidx]*1e3} mV and amp - {np.array(AP1amp_150pA_list)[lowDBLOmodelidx]*1e3} mV and RA - {RA_list[lowDBLOmodelidx]}\n")
f.write(f'Highest DBLO - {np.max(DBLO_150pA_list)*1e3} mV\n')



#####################
f.close()
sns.despine(fig=fig)
plt.tight_layout()
plt.savefig('Fig4.png', dpi=300)
# # plt.savefig('Fig8.pdf', dpi=300)
plt.show()
