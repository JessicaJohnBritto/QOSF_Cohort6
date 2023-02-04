import cirq
import numpy as np
import matplotlib.pyplot as plt

def prepare_correlated(env):
    yield cirq.H(env[0])
    yield cirq.CNOT(env[0],env[1])
    yield cirq.CNOT(env[1],env[2])

def prepare_uncorrelated(env):
    for qb in env:
        yield cirq.H(qb)

def collide(env,sys,theta):
    yield cirq.CNOT(env,sys)
    yield cirq.Rz(rads=2*theta).on(sys)
    yield cirq.CNOT(env,sys)

def collision_pattern_correlated(env,sys,n,theta):
    for i in range(n):
        yield from collide(env[1+(i%2)],sys,theta)

def collision_pattern_uncorrelated(env,sys,n,theta):
    for i in range(n):
        yield from collide(env[i],sys,theta)

def meas_coherence(sys):
    yield cirq.H(sys)
    yield cirq.measure(sys, key = 'answer')

def collision_circuit(env,sys,prepare_ancilla,collision_pattern,n,theta):
    yield cirq.H(sys)
    yield from prepare_ancilla(env)
    yield from collision_pattern(env,sys,n,theta)
    yield from meas_coherence(sys)


n = 7
g = 1
tau = np.pi/6
t = np.array(list(range(1,n+1)))*tau
theta = g*tau
rho_12_corr = []
rho_12_uncorr = []

sys = cirq.LineQubit(0)
env = cirq.LineQubit.range(1,n+1)

simulator = cirq.Simulator()
repcnt = 500

for i in range(1,n+1):
    circuit = cirq.Circuit(collision_circuit(env,sys,prepare_correlated,collision_pattern_correlated,i,theta))
    result = simulator.run(circuit,repetitions=repcnt)
    histogram = result.histogram(key = 'answer')

    rho_12_corr.append((histogram[0]-histogram[1])/repcnt)

for i in range(1,n+1):
    circuit = cirq.Circuit(collision_circuit(env,sys,prepare_uncorrelated,collision_pattern_uncorrelated,i,theta))
    result = simulator.run(circuit,repetitions=repcnt)
    histogram = result.histogram(key = 'answer')
    rho_12_uncorr.append((histogram[0]-histogram[1])/repcnt)

def corrfunc(time):
    return np.cos(time)**2-np.sin(time)**2

def uncorrfunc(i):
    return np.power(np.cos(2*g*tau),i/tau)

x_ax = np.linspace(0,t[-1],num=1000)

plt.scatter(t,rho_12_corr,label='correlated')
plt.plot(x_ax,corrfunc(x_ax),linestyle='--')
plt.scatter(t,rho_12_uncorr,label='uncorrelated')
plt.plot(x_ax,uncorrfunc(x_ax),linestyle='--')
plt.legend()
plt.show()
    
