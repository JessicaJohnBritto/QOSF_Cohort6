import cirq
import numpy as np
import matplotlib.pyplot as plt

def depolarising(sys,env,p,phi,psi):
    #initialise ancilla
    theta = 0.5*np.arccos(1-2*p)
    yield cirq.Ry(rads=theta).on_each(env)
    #initialise system to e^(-i*psi/2)*[cos(phi/2)|0>+e^(i*psi)*sin(phi/2)|1>]
    yield cirq.Ry(rads=phi).on(sys[0])
    yield cirq.Rz(rads=psi).on(sys[0])
    #perform ops
    yield cirq.X.on(sys[0]).controlled_by(env[0])
    yield cirq.Y.on(sys[0]).controlled_by(env[1])
    yield cirq.Z.on(sys[0]).controlled_by(env[2])

env = cirq.LineQubit.range(3)
sys = [cirq.LineQubit(3)]
probs = np.linspace(0,1,num=10)
phi = np.pi/4
psi = np.pi/4
a = np.cos(phi/2)**2
b = np.sin(phi/2)*np.cos(phi/2)*(np.cos(psi)-np.sin(psi)*1j)
c = np.conj(b)
d = np.sin(phi/2)**2

def theoretical_rho00(p):
    return 0.5*p+(1-p)*a
def theoretical_Rrho01(p):
    return np.real((1-p)*b)
def theoretical_Irho01(p):
    return np.imag((1-p)*b)
def theoretical_rho11(p):
    return 0.5*p+(1-p)*d

rho00 = []
rho11 = []
Rrho01 = []
Irho01 = []

for p in probs:
    circuit = cirq.Circuit()
    circuit.append(depolarising(sys,env,p,phi,psi))
    result = cirq.experiments.single_qubit_state_tomography(
    sampler=cirq.Simulator(),  # In case of Google QCS or other hardware providers, sampler could point at real hardware.
    qubit=sys[0],
    circuit=circuit,
    repetitions=2000,
    )
    rho00_p = result.data[0,0]
    rho11_p = result.data[1,1]
    Rrho01_p = np.real(result.data[0,1])
    Irho01_p = np.imag(result.data[0,1])
    rho00.append(rho00_p)
    rho11.append(rho11_p)
    Rrho01.append(Rrho01_p)
    Irho01.append(Irho01_p)

plt.scatter(probs,rho00,label='rho00')
plt.plot(probs,theoretical_rho00(probs),linestyle='--')
plt.scatter(probs,rho11,label='rho11')
plt.plot(probs,theoretical_rho11(probs),linestyle='--')
plt.scatter(probs,Rrho01,label='Rrho01')
plt.plot(probs,theoretical_Rrho01(probs),linestyle='--')
plt.scatter(probs,Irho01,label='Irho01')
plt.plot(probs,theoretical_Irho01(probs),linestyle='--')
plt.legend()
plt.show()
