#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hychem modeling approach

Encoded by: Raoul Mazumdar, PhD in Aerospace Engineering (Hypersonic Propulsion)
            Royal Melbourne Institute of Technology (RMIT)
            Date:1 August 2018
"""
import os
import time
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt
ct.suppress_thermo_warnings()

P0 = [1] #atm
T0 = [1100]
nt = 210000 #Steps
nF = 1 #No. of moles
nO2 = 5 #No. of moles
nN2 = 18.8 #No. of moles
tol = 10 # 10% ignition diff from baseline


inputFile = 'USC_C1_C3.cti'
gas = ct.Solution(inputFile)
gas.TPX = T0[0], P0[0]*ct.one_atm, 'C3H8:%s, O2:%s, N2:%s' %(nF,nO2,nN2)        
r = ct.IdealGasConstPressureReactor(gas) #constant pressure reactor.
sim = ct.ReactorNet([r])
states = ct.SolutionArray(gas, extra=['t'])
time = 0.0
for n in range(nt):
    print(n)
    time += 1.0e-7
    sim.advance(time)
    states.append(r.thermo.state, t=time)
dyTh = np.diff(states.T)
igny = ( ( 1.0e-7 )*( np.argmax(dyTh) ) )  


plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.plot(states.t,states.T)
plt.title('PSR Simulation')
plt.text(igny, states.T[np.argmax(dyTh)] , 'Ignition Point', fontsize=10)
plt.show()

            

