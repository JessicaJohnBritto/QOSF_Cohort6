import numpy as np

# importing Qiskit
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

#importing Mitiq
from mitiq.zne.scaling import fold_gates_at_random
from mitiq.zne.scaling import insert_id_layers
from mitiq.interface.mitiq_qiskit import to_qiskit, from_qiskit

def zz_pump(q, c, p, system, ancilla, ini):
    z = QuantumCircuit(q, c)
    if ini == "01":
        z.x(q[system[0]])
    elif ini == "10":
        z.x(q[system[1]])
    elif ini == "11":
        z.x(q[system[0]])
        z.x(q[system[1]])
    
    z.cx(q[system[0]], q[system[1]])
    z.x(q[ancilla])
    z.cx(q[system[1]], q[ancilla])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    
    z.cry(theta, q[ancilla], q[system[1]])
    
    z.cx(q[system[1]], q[ancilla])
    # z.cx(q[system[0]], q[system[1]])
    z.h(q[system[0]])
    z.measure(q[system[0]], c[0])
    z.measure(q[system[1]], c[1])
    return z

def xx_pump(q, c, p, system, ancilla, ini):
    xx = QuantumCircuit(q, c)
    if ini == "01":
        xx.x(q[system[0]])
    elif ini == "10":
        xx.x(q[system[1]])
    elif ini == "11":
        xx.x(q[system[0]])
        xx.x(q[system[1]])
    
    xx.cx(q[system[0]], q[system[1]])
    xx.h(q[system[0]])
    xx.x(q[ancilla])
    xx.cx(q[system[0]], q[ancilla])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    xx.cry(theta, q[ancilla], q[system[0]])
    
    xx.cx(q[system[0]], q[ancilla])
    
    xx.measure(q[system[0]], c[0])
    xx.measure(q[system[1]], c[1])
    
    return xx

def zz_xx_pump(q, c, p, system, ancillae, ini):
    zx = QuantumCircuit(q, c)
    if ini == "01":
        zx.x(q[system[0]])
    elif ini == "10":
        zx.x(q[system[1]])
    elif ini == "11":
        zx.x(q[system[0]])
        zx.x(q[system[1]])
        
    zx.cx(q[system[0]], q[system[1]])
    zx.x(q[ancillae[0]])
    zx.cx(q[system[1]], q[ancillae[0]])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    zx.cry(theta, q[ancillae[0]], q[system[1]])
    
    zx.cx(q[system[1]], q[ancillae[0]])
    
    zx.h(q[system[0]])
    zx.x(q[ancillae[1]])
    zx.cx(q[system[0]], q[ancillae[1]])
    
    zx.cry(theta, q[ancillae[1]], q[system[0]])
    
    zx.cx(q[system[0]], q[ancillae[1]])
    
    zx.measure(q[system[0]], c[0])
    zx.measure(q[system[1]], c[1])
    
    return zx

provider = IBMProvider()
backend = provider.get_backend('ibm_perth')

shots = 20000
probs = np.linspace(0,1.0,5)

with open('mre_11.txt','a') as job_id_file:
    pump_list = [zz_pump,xx_pump,zz_xx_pump]
    sys_list = [[2,1],[2,1],[2,1]]
    anc_list = [[0],[0],[0,3]]
    ini_list = ['00','01','10','11']
    scale_factors = [11,12]

    for scale_factor in scale_factors:
        circ_list = []

        for pump,sys,anc in zip(pump_list,sys_list,anc_list):  #Loop over pump
            for ini in ini_list:    #Loop over ini
                for p in probs: #Loop over prob
                    q = QuantumRegister(4, name='q')
                    c = ClassicalRegister(2, name='c')
                    #Create circuit
                    circ = pump(q, c, p, sys, anc, ini)
                    #Transpile first pass
                    transpiled = transpile(circ,backend=backend)
                    #Convert to Mitiq
                    circ_to_mitiq = from_qiskit(transpiled)
                    #Fold circuit
                    circ_folded_mitiq = fold_gates_at_random(circ_to_mitiq, scale_factor)
                    #Convert to Qiskit
                    circ_folded = to_qiskit(circ_folded_mitiq)
                    #Transpile without optimizing
                    transpiled_folded = transpile(circ_folded, backend=backend, optimization_level=0)
                    circ_list.append(transpiled_folded)

        job = backend.run(circ_list, shots=shots)   #Run job
        job_id_file.write(job.job_id()+'\n')    #Write to file
