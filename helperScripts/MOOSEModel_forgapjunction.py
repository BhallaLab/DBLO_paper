# exec(open('MOOSEModel_15.py').read())
# Has been modified heavily to be used in Parametersearch_again folder. Do not use as an api
# v3 takes care of Ca_B while giving an option to modify kinetics
# v5 added option to free SK channel kinetics. HHChannel2D cannot be parameterized right now.
# v6 Added a vclamp option
# v7 Instead of manually using ChanGate, now kinetic variabless from supported channel rdesigneur files can be directly changed. No backward compatibility
# v8 Fixed the vclamp where the output ws V instead of I
# v9 No longer prints the annoying rdesigneur statements
# v10 deleting a moose element which does not exists now gives a seg fault (current BhallaLab master branch). Modifies the scrit to avoid getting seg faults
# v11 kineticVars issue resolved
# v12 added refreshkinetics or not option. If using the kinetics as used in the kinetics file directly, refreshkin=False. Not properly implemented as of now. Use v11 for now
# v13 Has a synaptic input function
# v14 fixed an issue where ca dynamics B term was not properly changed.
# v14_custom2 for CV_EPSPfreq_amp
# v15 There has been several v14s. v15 compiles all these versions finally
# v16 Now also works if Ca_conc mechanisms not present in the model
# v17 Now you can specify the file and modelnumber to plot directly
# v17_multicompt_somamulti For model with channels in soma. In the parameterdict, specify morphology swc file. Pass gbar, cm, rm, ra instead of their absolute versions. vclamp does not work right now.
# This particular version is for multicompt model with all the channels only in the soma. B is an absolute quantity but pass in gbar, cm, rm, ra values.
# v18 Added apaProto function
# v18 2compt: The 2 compt model. Morpho is fixed. We have now 5 passive parameters - sm_RM, sm_CM, dend_RM, dend_CM, Ra (which is the average of both compt RAs)
# v19 2compt: Ballandstick does not work properly when running another simulation after the first one ends. Replaces it with manually described morphology
# v20: Added a way to also run chirp stimulus
# v21: added an option to add taper to the dendrites
# v22: Don't delete library. That led to kinetics being defined again which took time
# v23: Some fixes
# v24: Option to inject n number of synapses
# _: Some change specifically needed for this folder but do not remember what

import moose
import rdesigneur_forgapjunction as rd
import numpy as np
import matplotlib.pyplot as plt
# import xmltodict
import sys
import os
import io
import importlib
import numpy.random as nr
import argparse
from copy import deepcopy

sys.path.insert(1, "../Kinetics")


# elecid_ori = None
elecPlotDt = 5e-5
elecDt = 5e-6

def makeBallandstickProto(sm_len=10.075e-6, sm_diam=10.075e-6, dend_len=500e-6, dend_diam_start=4e-6, dend_diam_end=1e-6, num_dend_segments=10, Em=-82e-3, sm_RM = 0.06837242, sm_CM= 0.03759487, sm_RA = 1.49295246, dend_RM=1.86794368, dend_CM=0.02411617, dend_RA=1.18):
    if not moose.exists('/library/BNeuron'):
        BNeuron = moose.Neuron( '/library/BNeuron' )
    else:
        BNeuron = moose.element( '/library/BNeuron' )
    soma = rd.buildCompt( BNeuron, 'soma', RM = sm_RM, RA = sm_RA, CM = sm_CM, dia = sm_diam, x = 0.0, y = 0.0, z = 0.0, dx = sm_len, dy = 0.0, dz = 0.0, Em = Em, initVm = Em)
    prev = soma
    dend_diam = iter(np.linspace(dend_diam_start, dend_diam_end, num_dend_segments))
    for i in range(num_dend_segments):            
        compt = rd.buildCompt( BNeuron, f'dend{i}', RM = dend_RM, RA = dend_RA, CM = dend_CM, dia = next(dend_diam), x = sm_len + i*dend_len/num_dend_segments, y = 0.0, z = 0.0, dx = dend_len/num_dend_segments, dy = 0.0, dz = 0.0, Em = Em, initVm = Em)
        moose.connect(prev, 'axial', compt, 'raxial')
        prev = compt

    return BNeuron

def Parameterdict_parser(Parameterdict):
    """
    Parses Parameterdict and returns rdesigneur function Parameters

    Arguements:
    Parameterdict -- A valid Parameterdict
    """
    depth = 0.1
    F = 96485.3329
    Model = Parameterdict["Parameters"]

    Parameters = {}
    # sm_area = (
    #     np.pi
    #     * float(Model["Morphology"]["sm_diam"])
    #     * float(Model["Morphology"]["sm_len"])
    # )
    # dend_area = (
    #     np.pi
    #     * float(Model["Morphology"]["dend_diam"])
    #     * float(Model["Morphology"]["dend_len"])
    # )
    # cellProto = [
    #     [
    #         "somaProto",
    #         "soma",
    #         float(Model["Morphology"]["sm_diam"]),
    #         float(Model["Morphology"]["sm_len"]),
    #     ]
    # ]
    # cellProto = [['ballAndStick', 'soma', float(Model["Morphology"]["sm_diam"]), float(Model["Morphology"]["sm_len"]), float(Model["Morphology"]["dend_diam"]), float(Model["Morphology"]["dend_len"]), 1]]
    # cellProto = [Model["Morphology"], 'elec'],

    if moose.exists('library'):
        library = moose.element( '/library' )
    else:
        library = moose.Neutral( '/library' )
    makeBallandstickProto(sm_len=Model["Morphology"]["sm_len"], sm_diam=Model["Morphology"]["sm_diam"], dend_len=Model["Morphology"]["dend_len"], dend_diam_start=Model["Morphology"]["dend_diam_start"], dend_diam_end=Model["Morphology"]["dend_diam_end"], num_dend_segments=Model["Morphology"]["num_dend_segments"], Em=Model["Passive"]["Em"], sm_RM = Model["Passive"]["sm_RM"], sm_CM= Model["Passive"]["sm_CM"], sm_RA = Model["Passive"]["sm_RA"], dend_RM=Model["Passive"]["dend_RM"], dend_CM=Model["Passive"]["dend_CM"], dend_RA=Model["Passive"]["dend_RA"])
    cellProto = [['elec','BNeuron']]
    sm_area = np.pi*Model["Morphology"]["sm_len"]*Model["Morphology"]["sm_diam"]

    chanProto = []
    chanDistrib = []
    chd = Model["Channels"]
    for channel in chd.keys():
        chanProto.append([chd[channel]["Kinetics"] + "." + channel + "()", channel])
        if "gbar" in chd[channel].keys():
            chanDistrib.append(
                [channel, "soma", "Gbar", str(chd[channel]["gbar"])]
            )
        elif "Gbar" in chd[channel].keys():
            chanDistrib.append(
                [channel, "soma", "Gbar", str(chd[channel]["Gbar"]/sm_area)]
            )
        Parameters[channel + "_Erev"] = chd[channel]["Erev"]

    if "Ca_Conc" in Model.keys():
        chanProto.append([Model["Ca_Conc"]["Kinetics"] + ".Ca_Conc()", "Ca_conc"])
        chanDistrib.append(
            [
                "Ca_conc",
                "soma",
                "CaBasal",
                str(Model["Ca_Conc"]["Ca_base"]),
                "tau",
                str(Model["Ca_Conc"]["Ca_tau"]),
            ]
        )

    Parameters["cellProto"] = cellProto
    Parameters["chanProto"] = chanProto
    Parameters["chanDistrib"] = chanDistrib
    # Parameters["passiveDistrib"] = passiveDistrib
    if "Ca_Conc" in Model.keys():
        Parameters["Ca_B"] = float(Model["Ca_Conc"]["Ca_B"])

    return Parameters


def generateModel(
    Parameterdict, CurrInjection=150e-12, vClamp=None, refreshKin=True, syn=False, synwg=0.0, synfq=5
):
    """
    Returns in-silico model current clamp. Except Ca_B everything is set up

    Arguements:
    Parameterdict -- A valid Parameterdict
    CurrInjection -- Current clamp level, float or a string if specifying exact stimulation
    """

    if moose.exists("/model"):
        moose.delete("/model")
    if moose.exists("/Graphs"):
        moose.delete("/Graphs")
    # if moose.exists("/library"):
    #     moose.delete("/library")
    if moose.exists('/library/BNeuron'):
        moose.delete('/library/BNeuron')

    if syn:
        moose.seed()
    # global elecid_ori
    Parameters = Parameterdict_parser(Parameterdict)
    preStimTime = 0.5
    injectTime = 0.5
    postStimTime = 0.5

    # try:
    #     # [moose.delete(x) for x in ['/model', '/library']]
    #     # moose.delete("/model")
    #     # moose.delete("/Graphs")
        # rdes.elecid = moose.element(elecid_ori)
    # except:
    #     pass

    if syn:
        synGbar = 1
    else:
        synGbar = 1e-8

    # print(Parameters["cellProto"])
    if vClamp:
        rdes = rd.rdesigneur(
            elecPlotDt=elecPlotDt,
            elecDt=elecDt,
            cellProto=Parameters["cellProto"],
            chanProto=Parameters["chanProto"],
            chanDistrib=Parameters["chanDistrib"],
            stimList=[["soma", "1", ".", "vclamp", vClamp]],
            plotList=[
                ["soma", "1", ".", "Vm", "soma Membrane potential MOOSE"],
                ["soma", "1", "vclamp", "current", "Soma holding current"],
                ["soma", "1", "Ca_conc", "Ca", "Soma Calcium concentration"],
            ],
        )
    elif isinstance(CurrInjection, list):
        synlist_chanProto = [["make_glu()", f"glu{i}"] for i in range(syn)]
        synlist_chanDistrib = [[f"glu{i}", "soma", "Gbar", f"{synGbar}"] for i in range(syn)]
        synlist_stimList = [["soma", f"{synwg}", f"glu{i}", "randsyn", f"max(sin(2*3.14*{synfq}*t), 0)*100"] for i in range(syn)]
        rdes = rd.rdesigneur(
            elecPlotDt=elecPlotDt,
            elecDt=elecDt,
            cellProto=Parameters["cellProto"],
            chanProto=Parameters["chanProto"] + synlist_chanProto,
            chanDistrib=Parameters["chanDistrib"]+synlist_chanDistrib,
            stimList=[CurrInjection]+synlist_stimList,
            plotList=[
                # ["axon_1_2", "1", ".", "Vm", "AIS Membrane potential MOOSE"],
                ["soma", "1", ".", "Vm", "soma Membrane potential MOOSE"],
                ['soma', '1', '.', 'inject', 'Stimulus current'],
                ["soma", "1", "Ca_conc", "Ca", "Soma Calcium concentration"],
                # ["soma", "1", "K_A_Chan", "Gk", "Soma K_A_Chan Gbar"],
                # ["soma", "1", "K_DR_Chan", "Gk", "Soma K_DR_Chan Gbar"],
                # ["soma", "1", "Na_Chan", "Ik", "Soma Na_Chan current"],
                # ["soma", "1", "K_A_Chan", "Ik", "Soma K_A_Chan current"],
                # ["soma", "1", "K_DR_Chan", "Ik", "Soma K_DR_Chan current"],
                # ["soma", "1", "K_M_Chan", "Ik", "Soma K_M_Chan current"],
                # ["soma", "1", "K_SK_Chan", "Ik", "Soma K_SK_Chan current"],
                # ["soma", "1", "Ca_L_Chan", "Ik", "Soma Ca_L_Chan current"],
                # ["soma", "1", ".", "Im", "Soma membrane current"],
            ],
        )
    else:
        synlist_chanProto = [["make_glu()", f"glu{i}"] for i in range(syn)]
        synlist_chanDistrib = [[f"glu{i}", "soma", "Gbar", f"{synGbar}"] for i in range(syn)]
        synlist_stimList = [["soma", f"{synwg}", f"glu{i}", "randsyn", f"max(sin(2*3.14*{synfq}*t), 0)*100"] for i in range(syn)]
        rdes = rd.rdesigneur(
            elecPlotDt=elecPlotDt,
            elecDt=elecDt,
            cellProto=Parameters["cellProto"],
            chanProto=Parameters["chanProto"] + synlist_chanProto,
            chanDistrib=Parameters["chanDistrib"]+synlist_chanDistrib,
            stimList=[
                [
                    "soma",
                    "1",
                    ".",
                    "inject",
                    f"(t>={preStimTime} && t<={preStimTime+injectTime}) ? {CurrInjection} : 0",
                ]] + synlist_stimList,
            plotList=[
                # ["axon_1_2", "1", ".", "Vm", "AIS Membrane potential MOOSE"],
                ["soma", "1", ".", "Vm", "soma Membrane potential MOOSE"],
                ['soma', '1', '.', 'inject', 'Stimulus current'],
                ["soma", "1", "Ca_conc", "Ca", "Soma Calcium concentration"],
                # ["soma", "1", "K_A_Chan", "Gk", "Soma K_A_Chan Gbar"],
                # ["soma", "1", "K_DR_Chan", "Gk", "Soma K_DR_Chan Gbar"],
                # ["soma", "1", "Na_Chan", "Ik", "Soma Na_Chan current"],
                # ["soma", "1", "K_A_Chan", "Ik", "Soma K_A_Chan current"],
                # ["soma", "1", "K_DR_Chan", "Ik", "Soma K_DR_Chan current"],
                # ["soma", "1", "K_M_Chan", "Ik", "Soma K_M_Chan current"],
                # ["soma", "1", "K_SK_Chan", "Ik", "Soma K_SK_Chan current"],
                # ["soma", "1", "Ca_L_Chan", "Ik", "Soma Ca_L_Chan current"],
                # ["soma", "1", ".", "Im", "Soma membrane current"],
            ],
        )

    if refreshKin:  #True if in the new run, the kinetics was changed.
        for chan in Parameterdict["Parameters"]["Channels"].keys():
            imm = Parameterdict["Parameters"]["Channels"][chan]["Kinetics"].split("/")[
                -1
            ]
            exec(f"import {imm}")
            exec(f"importlib.reload({imm})")

            if "KineticVars" in Parameterdict["Parameters"]["Channels"][chan].keys():
                for var in Parameterdict["Parameters"]["Channels"][chan][
                    "KineticVars"
                ].keys():
                    valuee = Parameterdict["Parameters"]["Channels"][chan][
                        "KineticVars"
                    ][var]
                    exec(f"{imm}.{var} = {valuee}")
            exec(f"{imm}.{chan}('{chan}')")

    for chan in moose.wildcardFind("/library/#[CLASS==HHChannel]"):
        moose.element(f"/library/{chan.name}").Ek = Parameters[chan.name + "_Erev"]

    for chan in moose.wildcardFind("/library/#[CLASS==HHChannel2D]"):
        moose.element(f"/library/{chan.name}").Ek = Parameters[chan.name + "_Erev"]

    # Setup clock table to record time
    clk = moose.element("/clock")
    moose.Neutral("Graphs")
    plott = moose.Table("/Graphs/plott")
    moose.connect(plott, "requestOut", clk, "getCurrentTime")

    print("MOOSE Model generated")
    # elecid_ori = rdes.elecid.path
    return rdes


def runModel(
    Parameterdict,
    CurrInjection=150e-12,
    vClamp=None,
    refreshKin=True,
    Truntime=None,
    syn=False,
    synwg=0.0, synfq=5
):
    """
    CurrInjection: in A. Put None if using vClamp
    """
    if syn:
        moose.seed()
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    preStimTime = 0.5
    injectTime = 0.5
    postStimTime = 0.5

    rdes = generateModel(
        Parameterdict,
        CurrInjection=CurrInjection,
        vClamp=vClamp,
        refreshKin=refreshKin,
        syn=syn, synwg=synwg, synfq=synfq
    )
    rdes.buildModel()

    if moose.exists("/model[0]/elec[0]/soma[0]/vclamp"):
        moose.element("/model/elec/soma/vclamp").gain = (
            moose.element("/model/elec/soma").Cm / elecDt
        )
        moose.element("/model/elec/soma/vclamp").tau = 5 * elecDt
        moose.element("/model/elec/soma/vclamp").ti = elecDt * 2
        moose.element("/model/elec/soma/vclamp").td = 0

    Parameters = Parameterdict_parser(Parameterdict)
    for Ca_concelement in moose.wildcardFind("/model/elec/##[CLASS==ZombieCaConc]"):
        parrent = Ca_concelement.parent
        Ca_concelement.B = Parameters["Ca_B"]

    # #### Temp plotting gates ########
    # Na_Chan_X = moose.Table('Graphs/Na_Chan_X')
    # moose.connect(Na_Chan_X, "requestOut", moose.element('/model/elec/soma/Na_Chan'), "getX")
    # Na_Chan_Y = moose.Table('Graphs/Na_Chan_Y')
    # moose.connect(Na_Chan_Y, "requestOut", moose.element('/model/elec/soma/Na_Chan'), "getY")
    # K_A_Chan_X = moose.Table('Graphs/K_A_Chan_X')
    # moose.connect(K_A_Chan_X, "requestOut", moose.element('/model/elec/soma/K_A_Chan'), "getX")
    # K_A_Chan_Y = moose.Table('Graphs/K_A_Chan_Y')
    # moose.connect(K_A_Chan_Y, "requestOut", moose.element('/model/elec/soma/K_A_Chan'), "getY")
    # ################################

    moose.reinit()
    if Truntime is None:
        moose.start(preStimTime + injectTime + postStimTime)
    else:
        moose.start(Truntime)

    # rdes.display()
    Vmvec = moose.element("/model/graphs/plot0").vector
    Ivec = moose.element("/model/graphs/plot1").vector
    tvec = moose.element("/Graphs/plott").vector
    if moose.exists("/model[0]/elec[0]/soma[0]/Ca_conc"):
        Cavec = moose.element("/model/graphs/plot2").vector
    else:
        Cavec = None

    # I_Na_Chan_vec = moose.element("/model/graphs/plot2").vector
    # I_K_A_Chan_vec = moose.element("/model/graphs/plot3").vector
    # I_K_DR_Chan_vec = moose.element("/model/graphs/plot4").vector
    # I_K_M_Chan_vec = moose.element("/model/graphs/plot5").vector
    # I_K_SK_Chan_vec = moose.element("/model/graphs/plot6").vector
    # I_Ca_L_Chan_vec = moose.element("/model/graphs/plot7").vector
    # Im_vec = moose.element("/model/graphs/plot8").vector

    sys.stdout = old_stdout
    return [tvec, Ivec, Vmvec,Cavec]
    # return [tvec, Vmvec, Cavec, I_Na_Chan_vec, I_K_A_Chan_vec, I_K_DR_Chan_vec, I_K_M_Chan_vec, I_K_SK_Chan_vec, I_Ca_L_Chan_vec]


def plotModel(
    Parameterdict,
    CurrInjection=150e-12,
    vClamp=None,
    refreshKin=True,
    Truntime=None,
    syn=False,
    synwg=0.0, synfq=5
):
    """
    Returns in-silico model current clamp

    Arguements:
    Parameterdict -- A valid Parameterdict address, string
    CurrInjection -- Current clamp level, float
    """
    moose.seed()
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    preStimTime = 0.5
    injectTime = 0.5
    postStimTime = 0.5

    rdes = generateModel(
        Parameterdict,
        CurrInjection=CurrInjection,
        vClamp=vClamp,
        refreshKin=refreshKin,
        syn=syn, synwg=synwg, synfq=synfq
    )
    rdes.buildModel()

    if moose.exists("/model[0]/elec[0]/soma[0]/vclamp"):
        moose.element("/model/elec/soma/vclamp").gain = (
            moose.element("/model/elec/soma").Cm / elecDt
        )
        moose.element("/model/elec/soma/vclamp").tau = 5 * elecDt
        moose.element("/model/elec/soma/vclamp").ti = elecDt * 2
        moose.element("/model/elec/soma/vclamp").td = 0

    Parameters = Parameterdict_parser(Parameterdict)
    for Ca_concelement in moose.wildcardFind("/model/elec/##[CLASS==ZombieCaConc]"):
        parrent = Ca_concelement.parent
        Ca_concelement.B = Parameters["Ca_B"]

    moose.reinit()
    if Truntime is None:
        moose.start(preStimTime + injectTime + postStimTime)
    else:
        moose.start(Truntime)

    sys.stdout = old_stdout

    rdes.display()
    return rdes

def apaProto(Parameterdict, Vh = None, refreshKin=True):
    if Vh ==None:
        hold = [-55e-3,-45e-3,-35e-3,-25e-3,-15e-3,-5e-3,5e-3,15e-3,25e-3,35e-3]
        apacurr_list = []
        tbAp, IbAp, Cavec = runModel(Parameterdict, vClamp=f'-0.055 + (t>1 && t<1.1)*-0.010 + (t>1.1 && t<1.9)*{0}', refreshKin=refreshKin, Truntime=0.1)
        for Vhold in hold:
            # print(Vhold)
            tbAp, IbAp, Cabvec = runModel(Parameterdict, vClamp=f'-0.055 + (t>1 && t<1.1)*-0.010 + (t>1.1 && t<1.9)*{Vhold+55e-3}', refreshKin=False, Truntime=2)
            Parameterdict_temp = deepcopy(Parameterdict)
            if 'Gbar' in list(Parameterdict_temp['Parameters']['Channels']['K_SK_Chan'].keys()):
                Parameterdict_temp['Parameters']['Channels']['K_SK_Chan']['Gbar'] = 1e-15
            else:
                Parameterdict_temp['Parameters']['Channels']['K_SK_Chan']['gbar'] = 1e-15
            taAp, IaAp, Caavec = runModel(Parameterdict_temp, vClamp=f'-0.055 + (t>1 && t<1.1)*-0.010 + (t>1.1 && t<1.9)*{Vhold+55e-3}', refreshKin=False, Truntime=2)
            apacurr = IbAp[np.argmin(np.abs(1.925-tbAp))] - IaAp[np.argmin(np.abs(1.925-taAp))]
            # plt.figure()
            # plt.plot(tbAp, IbAp)
            # plt.plot(taAp, IaAp)
            # plt.figure()
            # plt.plot(tbAp, Cabvec)
            # plt.plot(taAp, Caavec)
            # plt.show()
            apacurr_list.append(apacurr)

        return apacurr_list
    else:
        # print(Vh)
        tbAp, IbAp, VmbAp, CabAp= runModel(Parameterdict, vClamp=f'-0.055 + (t>1 && t<1.1)*-0.010 + (t>1.1 && t<1.9)*{Vh+55e-3}', refreshKin=False, Truntime=2)
        Parameterdict_temp = deepcopy(Parameterdict)
        if 'Gbar' in list(Parameterdict_temp['Parameters']['Channels']['K_SK_Chan'].keys()):
            Parameterdict_temp['Parameters']['Channels']['K_SK_Chan']['Gbar'] = 1e-15
        else:
            Parameterdict_temp['Parameters']['Channels']['K_SK_Chan']['gbar'] = 1e-15
        taAp, IaAp, VmaAp, CaaAp = runModel(Parameterdict_temp, vClamp=f'-0.055 + (t>1 && t<1.1)*-0.010 + (t>1.1 && t<1.9)*{Vh+55e-3}', refreshKin=False, Truntime=2)
        apacurr = IbAp[np.argmin(np.abs(1.925-tbAp))] - IaAp[np.argmin(np.abs(1.925-taAp))]
        # plt.figure()
        # plt.plot(tbAp, VmbAp)
        # plt.plot(taAp, VmaAp)
        # plt.figure()
        # plt.plot(tbAp, IbAp)
        # plt.plot(taAp, IaAp)
        # plt.figure()
        # plt.plot(tbAp, IbAp-IaAp)
        # plt.figure()
        # plt.plot(tbAp, CabAp)
        # plt.plot(taAp, CaaAp)
        # plt.show()
        return apacurr

    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('-M', type=str, default='Model1', nargs='?')
    parser.add_argument('-I', type=float, default=150e-12, nargs='?')
    args = parser.parse_args()
    exec(open(args.file).read())
    plotModel(Models[args.M], args.I)
    import featuresv26_nonallen_uniform as fts
    from pprint import pprint
    import moose
    import numpy as np
    A = fts.modelfeatures(Models[args.M], stim_start=1, stim_end=1.5, apa=False)
    pprint(A)
    # Sarea = 0
    # for compt in moose.wildcardFind("/model/elec/#[CLASS==ZombieCompartment]"):
    #     SA = compt.length*np.pi*compt.diameter
    #     print(SA)
    #     Sarea = Sarea+SA
    # print(f'Total Surface area = {Sarea}')
