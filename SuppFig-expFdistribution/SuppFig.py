import sys 
sys.path.insert(1, "../helperScripts")

# import pylustrator
# pylustrator.start()

# import matplotlib
import matplotlib.pyplot as plt
# import numpy as np
# import features as fts
# import expcells
# from tqdm import tqdm
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
# from scipy.signal import butter, filtfilt
# import os
# from pprint import pprint
# import scipy.stats as scs


sns.set(style="ticks")
sns.set_context("paper")

# Create two subplots side by side
fig = plt.figure(figsize=(8, 3), constrained_layout=True)
# fig = plt.figure(figsize=(4.69, 3.135), constrained_layout=True)
gs = GridSpec(2, 5, figure=fig)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[0, 2])
axD = fig.add_subplot(gs[0, 3])
axE = fig.add_subplot(gs[0, 4])

axF = fig.add_subplot(gs[1, 0])
axG = fig.add_subplot(gs[1, 1])
axH = fig.add_subplot(gs[1, 2])
axI = fig.add_subplot(gs[1, 3])
axJ = fig.add_subplot(gs[1, 4])

# add a, b, c text to each subplot axis
fig.transFigure.inverted().transform([0.5,0.5])
for i, ax in enumerate([axA, axB, axC, axD, axE, axF,axG,axH, axI, axJ]):
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

################################################################################

df_exppasF = pd.read_pickle("../helperScripts/expactiveF.pkl")

def plottheplot(axx, featurename, multiplier, label):
    ax = sns.boxplot(
        ax=axx,
        data=df_exppasF,
        y=df_exppasF[featurename] * multiplier,
        showfliers=False,
        width=0.3,
        color='C7',
        zorder=2
    )
    sns.stripplot(
        ax=ax,
        data=df_exppasF,
        y=df_exppasF[featurename] * multiplier,
        zorder=3,
        color='C1',
    )
    ax.set_ylabel(label)
    ax.axhspan(df_exppasF.min()[featurename]*multiplier, df_exppasF.max()[featurename]*multiplier, color='C9', alpha=0.3)

plottheplot(axA, 'Input resistance', 1e-6, r"Input resistance (M$\Omega$)")
plottheplot(axB, 'Cell capacitance', 1e12, "Cell capacitance (pF)")
plottheplot(axC, "E_rest_0", 1e3, "$E_{rest}$ (mV)")
plottheplot(axD, "Time constant", 1e3, "$tau_m$ (ms)")
plottheplot(axE, "sagrat_m50", 1, "sag_rat (1)")

#############################################################################
df_expactiveF = pd.read_pickle("../helperScripts/expactiveF.pkl")
df_expsummaryactiveF = pd.read_pickle("../helperScripts/expsummaryactiveF.pkl")

def plottheplot(axx, featurename, multiplier, label):
    ax = sns.boxplot(
        ax=axx,
        data=df_expactiveF,
        y=df_expactiveF[featurename] * multiplier,
        showfliers=False,
        width=0.3,
        color='C7',
        zorder=2
    )
    sns.stripplot(
        ax=ax,
        data=df_expactiveF,
        y=df_expactiveF[featurename] * multiplier,
        zorder=3,
        color='C1',
    )
    ax.set_ylabel(label)
    ax.axhspan(df_expsummaryactiveF['10th quantile'][featurename]*multiplier, df_expsummaryactiveF['90th quantile'][featurename]*multiplier, color='C9', alpha=0.3)


plottheplot(axF, "AP1_width_1.5e-10", 1e3, "AP1 width (ms)")
plottheplot(axG, "freq_1.5e-10", 1, "firing frequency (Hz)")
plottheplot(axH, "ISIavg_1.5e-10", 1e3, "Mean ISI (ms)")
plottheplot(axI, "AP1_amp_1.5e-10", 1e3, "AP1 amplitude (mV)")
plottheplot(axJ, "DBLO_1.5e-10", 1e3, "DBLO (mV)")



############################################################
# Show the plots
sns.despine(fig=fig)
plt.savefig('FigSupp.png', dpi=300)
plt.show()

