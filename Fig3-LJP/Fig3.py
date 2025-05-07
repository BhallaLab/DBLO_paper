import sys

sys.path.insert(1, "../helperScripts")
sys.path.insert(1, "../Kinetics")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.gridspec as gridspec
from matplotlib.gridspec import GridSpec
import os
import subprocess
from scipy.signal import butter, filtfilt
import expcells
import features as fts
from tqdm import tqdm
from scipy.interpolate import interp1d

sns.set(style="ticks")
sns.set_context("paper")

fig = plt.figure(figsize=(7, 6))
gs = GridSpec(2, 2, figure=fig, hspace=0.5)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, 0])
gs_inner = gs[1, 1].subgridspec(1, 2)
axD = [0]*2
axD[0] = fig.add_subplot(gs_inner[0, 0])
axD[1] = fig.add_subplot(gs_inner[0, 1])

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA, axB, axC, axD[0]]):
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
for i, ax in enumerate([axD[0], axD[1]]):
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

f = open('NOTES.txt', 'w')

### getting the kinetics ###
import moose
import Na_T_Chan_Royeck_wslow
moose.Neutral('library')
Na_T = Na_T_Chan_Royeck_wslow.Na_T_Chan("Na_T_Chan")
xgate = moose.element( Na_T.path + '/gateX' )
v = np.linspace(xgate.min, xgate.max, xgate.divs+1)
minf = xgate.tableA/xgate.tableB
mtau = 1/xgate.tableB
ygate = moose.element( Na_T.path + '/gateY' )
v = np.linspace(ygate.min, ygate.max, ygate.divs+1)
hinf = ygate.tableA/ygate.tableB
htau = 1/ygate.tableB


### LJP explaining image ###
image = plt.imread('LJP_Anzal.png')
axA.imshow(image)
axA.axis('off')

### Exp without lJP correction ###
cell2 = expcells.expcell('2023_01_04_cell_2', f'../expdata/Chirp/2023_01_04_cell_2')
T_300pA, Vm_300pA = expcells.expdata(cell2.preFIfile, Index=16)
stim_start = 0.3469
stim_end = stim_start+0.5
LJP = 15e-3
Features = fts.expfeatures(cellpath=cell2.preFIfile, stim_start=stim_start, stim_end=stim_end, LJP=0)

axB.plot((T_300pA-stim_start)*1e3, Vm_300pA*1e3, label='LJP not corrected', c='C4')
axB.plot((T_300pA-stim_start)*1e3, (Vm_300pA-LJP)*1e3, label='LJP corrected', c='C0', alpha=0.5)
axB.set_xlabel('Time (ms)')
axB.set_ylabel('Voltage (mV)')
axB.set_xlim(-0.1*1e3, 0.6*1e3)
axB.set_ylim(-0.095*1e3, 0.05*1e3)
axB.axhline(y=Features["DBL_3e-10"]*1e3, color='C4', linestyle='--')
axB.axhline(y=(Features["DBL_3e-10"]-LJP)*1e3, color='C0', linestyle='--')
axB.legend(frameon=False, loc='lower center')

f.write(f"Exp DBL pre-correction: {Features['DBL_3e-10']*1e3} mV\n")
f.write(f"Exp DBL post-LJPcorrection: {(Features['DBL_3e-10']-LJP)*1e3} mV\n")

##### The kinetics ###############
axC.plot(v*1e3, minf**3, c='C1', label='$m_{inf}^3$')
axC.plot(v*1e3, hinf, c='C5', label='$h_{inf}$')
axC.set_xlabel('Voltage (mV)')
axC.set_ylabel('steady state')
axC.set_xlim(-0.1*1e3, 0*1e3)
axC.set_title(r'Na$^+$ Channel kinetics')
axC.legend(frameon=False)

axC.axvline(x=Features["DBL_3e-10"]*1e3, color='C4', linestyle='--')
axC.axvline(x=(Features["DBL_3e-10"]-LJP)*1e3, color='C0', linestyle='--', alpha=0.5)

print(Features["DBL_3e-10"], Features["DBLO_3e-10"])

hinf_interp = interp1d(v * 1e3, hinf, kind='linear', fill_value='extrapolate')
hinf_at_vline = hinf_interp(Features["DBL_3e-10"] * 1e3)
f.write(f"hinf at DBL pre-correction: {hinf_at_vline}\n")
hinf_at_vline = hinf_interp((Features["DBL_3e-10"]-LJP)*1e3)
f.write(f"hinf at DBL post-correction: {hinf_at_vline}\n")

### gating variables ###
dt = T_300pA[1] - T_300pA[0]
def playexpv(LJP = 15e-3):
    m_list = [0]
    h_list = [1]
    for i,t in tqdm(enumerate(T_300pA[1:])):
        v_ = Vm_300pA[i+1] - LJP
        minf_, mtau_ = np.interp(v_, v, minf), np.interp(v_, v, mtau)
        m_list.append(min([1,(minf_ - m_list[-1])/mtau_*dt + m_list[-1]]))

        hinf_, htau_ = np.interp(v_, v, hinf), np.interp(v_, v, htau)
        h_list.append((hinf_ - h_list[-1])/htau_*dt + h_list[-1])

    return [m_list, h_list]

m_list, h_list = playexpv(0e-3)
axD[0].plot((T_300pA - stim_start)*1e3, np.array(m_list)**3, label='$m^3$', c='C1')
axD[0].plot((T_300pA - stim_start)*1e3, h_list, label='h', c='C5')
axD[0].set_xlim(-0.010*1e3,0.045*1e3)
axD[0].set_ylabel('gating variable')
axD[0].set_xlabel('Time (ms)')
axD[0].set_title('LJP \nnot corrected')
axD0_Vm = axD[0].twinx()
axD0_Vm.plot((T_300pA-stim_start)*1e3, Vm_300pA*1e3, label='LJP not corrected', c='C4', alpha=0.5, linewidth=1)
axD0_Vm.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
axD0_Vm.set_ylim(-0.095*1e3, 0.05*1e3)

m_list, h_list = playexpv(15e-3)
axD[1].plot((T_300pA - stim_start)*1e3, np.array(m_list)**3, label='$m^3$', c='C1')
axD[1].plot((T_300pA - stim_start)*1e3, h_list, label='h', c='C5')
axD[1].set_xlim(-0.010*1e3,0.045*1e3)
axD[1].set_xlabel('Time (ms)')
axD[1].tick_params(left=False, labelleft=False)
axD[1].set_title('LJP \ncorrected')
axD1_Vm = axD[1].twinx()
axD1_Vm.plot((T_300pA-stim_start)*1e3, (Vm_300pA-LJP)*1e3, label='LJP corrected', c='C0', alpha=0.5, linewidth=1)
axD1_Vm.set_ylim(-0.095*1e3, 0.05*1e3)
axD1_Vm.set_ylabel('Voltage (mV)', color='C0')
axD[1].tick_params(left = False)
axD1_Vm.spines['right'].set_color('C0')
axD1_Vm.tick_params(axis='y', colors='C0')

leg = axD[1].legend(frameon=False, loc='center left', bbox_to_anchor=(-0.15,0.4),handlelength=1)

# subfig.suptitle('Na gating variables', y=0.9)

## show plot ##
sns.despine(fig=fig)
axD[1].spines['left'].set_visible(False)
axD1_Vm.spines['right'].set_visible(True)
axD1_Vm.spines['left'].set_visible(False)
# plt.tight_layout()
plt.savefig('Fig3.png', dpi=300)
plt.show()
f.close()