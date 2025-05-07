## exec(open('Migliore2018CA1pyrIclamp.py').read())

from neuron import h,gui
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sbn
# sbn.set()

h('load_file("Figure8control.hoc")')

v_vec = h.Vector()             # Membrane potential vector
t_vec = h.Vector()             # Time stamp vector
v_vec.record(h.soma[0](0.5)._ref_v)
t_vec.record(h._ref_t)

# h.iclamp = None

stim = h.IClamp(h.soma[0](0.5))
stim.delay = 200
stim.amp = 1.05
stim.dur = 500
h.finitialize()
h.tstop = 800
h.run()

plt.plot(np.array(t_vec)*1e-3,np.array(v_vec)*1e-3)
plt.show()

np.savez('output.npz', delay=stim.delay*1e-3, amp=stim.amp*1e-9, t_vec = np.array(t_vec)*1e-3, v_vec = np.array(v_vec)*1e-3)

