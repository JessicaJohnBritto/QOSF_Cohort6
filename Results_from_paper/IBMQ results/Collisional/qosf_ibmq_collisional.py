import numpy as np

# importing Qiskit
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

#importing Mitiq
from mitiq.zne.scaling import fold_gates_at_random
from mitiq.interface.mitiq_qiskit import to_qasm, from_qiskit

def corr(q, c, system, ancillae, g, t, i):
    coA = QuantumCircuit(q,c)
    
    # State Preparation
    coA.h(q[system])
    coA.h(q[ancillae[2]])
    coA.cnot(q[ancillae[2]],q[ancillae[1]])
    coA.cnot(q[ancillae[2]],q[ancillae[0]])
    
    # Collisions between the system and ancilla qubits
    for j in range(1, i+1, 1):
        if j%2 != 0:
            coA.cnot(q[ancillae[0]],q[system])
            coA.rz(2*t, q[system])
            coA.cnot(q[ancillae[0]],q[system])
        else:
            coA.cnot(q[ancillae[1]],q[system])
            coA.rz(2*t, q[system])
            coA.cnot(q[ancillae[1]],q[system])
    
    coA.h(q[system])
    
    coA.measure(q[system],c[0])
    coA.measure(q[ancillae[0]],c[1])
    coA.measure(q[ancillae[1]],c[2])
    coA.measure(q[ancillae[2]],c[3])
        
    return coA

def rewrite_qasm(qasm_str):
    lines = qasm_str.split('\n')
    out_lines = []
    measure_lines = []
    creg_lines = []
    final_output = []
    for line in lines:
        if not line.endswith(';'):
            out_lines.append(line)
            continue
        words = line[:-1].split(' ')
        if words[0] == 'measure':
            measure_lines.append(line)
        elif words[0] == 'creg':
            creg_lines.append(line)
        else:
            out_lines.append(line)
    
    for line in out_lines:
        final_output.append(line)
        if line.startswith('qreg'):
            final_output.append(f'creg c[{len(creg_lines)}];')

    for line in measure_lines:
        words = line[:-1].split(' ')
        qword = words[1]
        cword = words[3]
        final_output.append(f'measure {qword} -> c[{cword[4]}];')

    final_output.append('')

    return '\n'.join(final_output)

provider = IBMProvider()
backend = provider.get_backend('simulator_statevector')

shots = 20000

with open('./Jobs/Sim/2.txt','w') as job_id_file:
    system = 0
    ancillae = [1, 2, 3]
    n = 20
    tt = np.pi/6
    g = 1
    t = g*(tt)
    scale_factors = [1]

    for scale_factor in scale_factors:
        circ_list = []

        q = QuantumRegister(4,name = 'q')
        c = ClassicalRegister(4, name = 'c')
        for i in range(1,n+1,1):
            #Create circuit
            circ = corr(q, c, system, ancillae, g, tt, i)
            #Transpile first pass
            transpiled = transpile(circ,backend=backend,optimization_level=0)
            #Convert to Mitiq
            #circ_to_mitiq = from_qiskit(transpiled)
            #Fold circuit
            #circ_folded_mitiq = fold_gates_at_random(circ_to_mitiq, scale_factor)
            #Convert to Qiskit
            #circ_folded_qasm = rewrite_qasm(to_qasm(circ_folded_mitiq))
            #circ_folded = QuantumCircuit.from_qasm_str(circ_folded_qasm)
            #Transpile without optimizing
            #transpiled_folded = transpile(circ_folded, backend=backend, optimization_level=0)
            circ_list.append(transpiled)

        job = backend.run(circ_list, shots=shots)   #Run job
        job_id_file.write(job.job_id()+'\n')    #Write to file
        print('Submitted job with job id '+job.job_id())

print('All complete.')
