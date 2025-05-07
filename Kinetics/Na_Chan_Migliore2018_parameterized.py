# exec(open('../../Compilations/Kinetics/Na_Chan_(Migliore2018).py').read())
# Na channel taken from mod files of Migliore2018: na3n.mod
# Problems: q10 same for both X and Y gates.
# Not completely fitted

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
ENa = 0.092
EK = -0.100
Eh = -0.030
ECa = 0.140
Em = -0.065

#################################
m_vhalf_inf, m_slope_inf, m_A, m_B, m_C, m_D, m_E, m_F = -0.03843252,  0.0072, -0.03372518,  0.02202809,  0.001     , 0.001     ,  0.04497893,  0.0006807
h_vhalf_inf, h_slope_inf, h_A, h_B, h_C, h_D, h_E, h_F = -0.05,-0.004, -0.04560635, 0.0043351,0.01197735, 0.02616514,0.00854018, 0.03900142
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

def Na_Chan(name):
    Na = moose.HHChannel( '/library/' + name )
    Na.Ek = ENa
    Na.Gbar = 300.0*SOMA_A
    Na.Gk = 0.0
    Na.Xpower = 3.0
    Na.Ypower = 1
    Na.Zpower = 0
    Na.useConcentration = False

    def ChanGate(v,vhalf_inf, slope_inf, A, B, C, D, E, F):
        # alge model
        Inf = 1/(1+np.exp((v-vhalf_inf)/-slope_inf))
        yl = (v-A)/-B
        yr = (v-A)/E
        Tau = (C + (1 + yl/(np.sqrt(1+yl**2)))/2) * (D + (1 + yr/(np.sqrt(1+yr**2)))/2) * F
        Tau[Tau<0.00002] = 0.00002
        return [Inf,Tau]

    minf, mtau = ChanGate(v, m_vhalf_inf, m_slope_inf, m_A, m_B, m_C, m_D, m_E, m_F)
    hinf, htau = ChanGate(v, h_vhalf_inf, h_slope_inf, h_A, h_B, h_C, h_D, h_E, h_F)

    xgate = moose.element( Na.path + '/gateX' )
    xgate.min = Vmin
    xgate.max = Vmax
    xgate.divs = Vdivs
    xgate.tableA = minf/mtau
    xgate.tableB = 1.0/mtau

    ygate = moose.element( Na.path + '/gateY' )
    ygate.min = Vmin
    ygate.max = Vmax
    ygate.divs = Vdivs
    ygate.tableA = hinf/htau
    ygate.tableB = 1.0/htau

    return Na

if __name__ == "__main__":
    moose.Neutral('library')
    Na_Chan('Na_Chan')

    fig, axs = plt.subplots(2,1)
    axs[0].plot(v, (moose.element('library/Na_Chan/gateX').tableA/moose.element('library/Na_Chan/gateX').tableB)**3, label='nInf')
    axs[0].plot(v, moose.element('library/Na_Chan/gateY').tableA/moose.element('library/Na_Chan/gateY').tableB, label='lInf')
    # axs[0].plot(v, moose.element('library/Na_Chan/gateZ').tableA/moose.element('library/Na_Chan/gateZ').tableB, label='sInf')
    axs[0].set_ylabel('Inf')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(v, 1/moose.element('library/Na_Chan/gateX').tableB, label='nTau')
    axs[1].plot(v, 1/moose.element('library/Na_Chan/gateY').tableB, label='lTau')
    # axs[1].plot(v, 1/moose.element('library/Na_Chan/gateZ').tableB, label='sTau')
    axs[1].set_ylabel('Tau')
    axs[1].legend()
    axs[1].grid()

    plt.show()