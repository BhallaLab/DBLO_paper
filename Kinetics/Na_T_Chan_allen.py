# exec(open('../../Compilations/Kinetics/Na_Chan_Custom4.py').read())
# Na channel parameterized kinetics. Base is experimental kinetics by inf - Colbert Pan 2002 and Gouwens 2018 (allenbrain)
# Added a non-functional slow gate


import numpy as np
import pickle
import pandas as pd
import moose
import matplotlib.pyplot as plt

SOMA_A = 3.14e-8
F = 96485.3329
R = 8.314
celsius = 32
dt = 0.05e-3
ENa = 0.060
EK = -0.100
Eh = -0.030
ECa = 0.140
Em = -0.065

#################################
m_vhalf_inf, m_slope_inf, m_A, m_B, m_C, m_D, m_E, m_F = -0.04230235, 0.006, -0.04476696, 0.02195916, 0.01651614, 0.04558798, 0.01921329, 0.00093119
h_vhalf_inf, h_slope_inf, h_A, h_B, h_C, h_D, h_E, h_F = -66e-3, -6e-3, -0.07071566,0.02638247,0.01824088,0.06117676,0.0161364, 0.00866348
s_vhalf_inf, s_slope_inf, s_A, s_B, s_C, s_D, s_E, s_F = 1,-0.01, 100,1e-50,0,0,-1e-50, 1e-3 #The F term determines the Tau
#################################

Vmin = -0.100
Vmax = 0.100
Vdivs = 3000
# dV = (Vmax-Vmin)/Vdivs
# v = np.arange(Vmin,Vmax, dV)
v = np.linspace(Vmin,Vmax, Vdivs)
Camin = 1e-12
Camax = 1
Cadivs = 400
# dCa = (Camax-Camin)/Cadivs
# ca = np.arange(Camin,Camax, dCa)
ca = np.linspace(Camin,Camax, Cadivs)

def ChanGate(v,vhalf_inf, slope_inf, A, B, C, D, E, F):
    # alge model
    Inf = 1/(1+np.exp((v-vhalf_inf)/-slope_inf))
    yl = (v-A)/-B
    yr = (v-A)/E
    Tau = (C + (1 + yl/(np.sqrt(1+yl**2)))/2) * (D + (1 + yr/(np.sqrt(1+yr**2)))/2) * F
    Tau[Tau<0.00002] = 0.00002
    return [Inf,Tau]

def Na_T_Chan(name):
    Na_T = moose.HHChannel( '/library/' + name )
    Na_T.Ek = ENa
    Na_T.Gbar = 300.0*SOMA_A
    Na_T.Gk = 0.0
    Na_T.Xpower = 3.0
    Na_T.Ypower = 1
    Na_T.Zpower = 1
    Na_T.useConcentration = 0

    [mInf,mTau] = ChanGate(v,*[m_vhalf_inf, m_slope_inf, m_A, m_B, m_C, m_D, m_E, m_F])
    [hInf,hTau] = ChanGate(v,*[h_vhalf_inf, h_slope_inf, h_A, h_B, h_C, h_D, h_E, h_F])
    [sInf,sTau] = ChanGate(v,*[s_vhalf_inf, s_slope_inf, s_A, s_B, s_C, s_D, s_E, s_F])

    xgate = moose.element( Na_T.path + '/gateX' )
    xgate.min = Vmin
    xgate.max = Vmax
    xgate.divs = Vdivs
    xgate.tableA = mInf/mTau
    xgate.tableB = 1.0/mTau

    ygate = moose.element( Na_T.path + '/gateY' )
    ygate.min = Vmin
    ygate.max = Vmax
    ygate.divs = Vdivs
    ygate.tableA = hInf/hTau
    ygate.tableB = 1.0/hTau

    zgate = moose.element( Na_T.path + '/gateZ' )
    zgate.min = Vmin
    zgate.max = Vmax
    zgate.divs = Vdivs
    zgate.tableA = sInf/sTau
    zgate.tableB = 1.0/sTau

    return Na_T

if __name__ == "__main__":
    moose.Neutral('library')
    Na_T_Chan('Na_T_Chan')

    fig, axs = plt.subplots(2,1)
    axs[0].plot(v, (moose.element('library/Na_T_Chan/gateX').tableA/moose.element('library/Na_T_Chan/gateX').tableB)**3, label='nInf')
    axs[0].plot(v, moose.element('library/Na_T_Chan/gateY').tableA/moose.element('library/Na_T_Chan/gateY').tableB, label='lInf')
    axs[0].plot(v, moose.element('library/Na_T_Chan/gateZ').tableA/moose.element('library/Na_T_Chan/gateZ').tableB, label='sInf')
    axs[0].set_ylabel('Inf')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(v, 1/moose.element('library/Na_T_Chan/gateX').tableB, label='nTau')
    axs[1].plot(v, 1/moose.element('library/Na_T_Chan/gateY').tableB, label='lTau')
    axs[1].plot(v, 1/moose.element('library/Na_T_Chan/gateZ').tableB, label='sTau')
    axs[1].set_ylabel('Tau')
    axs[1].legend()
    axs[1].grid()

    plt.show()

