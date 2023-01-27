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
    yield cirq.Rz(rads=theta).on(sys)
    yield cirq.CNOT(env,sys)

def collision_pattern_correlated(env,sys,n,theta):
    for i in range(n):
        yield from collide(env[1+(i%2)],sys,theta)

def collision_pattern_uncorrelated(env,sys,n,theta):
    for i in range(n):
        yield from collide(env[i],sys,theta)

def collision_circuit(env,sys,prepare_ancilla,collision_pattern,n,theta):
    yield cirq.H(sys)
    yield from prepare_ancilla(env)
    yield from collision_pattern(env,sys,n,theta)

n = 20
g = 1
tau = np.pi/6
t = np.array(list(range(1,n+1)))*tau
theta = g*tau
rho_12_corr = []
rho_12_uncorr = []

sys = cirq.LineQubit(0)
env = cirq.LineQubit.range(1,n+1)

for i in range(1,n+1):
    circuit = cirq.Circuit(collision_circuit(env,sys,prepare_correlated,collision_pattern_correlated,i,theta))
    result = cirq.experiments.single_qubit_state_tomography(
    sampler=cirq.Simulator(),  # In case of Google QCS or other hardware providers, sampler could point at real hardware.
    qubit=sys,
    circuit=circuit,
    repetitions=5000,
    )
    rho_12_corr.append(np.real(result.data[0,1]))

for i in range(1,n+1):
    circuit = cirq.Circuit(collision_circuit(env,sys,prepare_uncorrelated,collision_pattern_uncorrelated,i,theta))
    result = cirq.experiments.single_qubit_state_tomography(
    sampler=cirq.Simulator(),  # In case of Google QCS or other hardware providers, sampler could point at real hardware.
    qubit=sys,
    circuit=circuit,
    repetitions=5000,
    )
    rho_12_uncorr.append(np.real(result.data[0,1]))

plt.scatter(t,rho_12_corr,label='correlated')
plt.scatter(t,rho_12_uncorr,label='uncorrelated')
plt.legend()
plt.show()
    
