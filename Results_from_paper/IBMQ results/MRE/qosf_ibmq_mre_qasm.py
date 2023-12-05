import numpy as np

#importing Cirq
from cirq.contrib.qasm_import import circuit_from_qasm

# importing Qiskit
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

#importing Mitiq
from mitiq.interface.mitiq_qiskit import to_qasm, from_qiskit

def zz_pump(q, c, p, system, ancilla, ini):
    z = QuantumCircuit(q, c)
    if ini == "01":
        z.x(q[system[0]])
    elif ini == "10":
        z.x(q[system[1]])
    elif ini == "11":
        z.x(q[system[0]])
        z.x(q[system[1]])

    z.x(q[ancilla])
    z.cx(q[system[1]], q[ancilla])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    
    z.cry(theta, q[ancilla], q[system[1]])
    
    z.cx(q[system[1]], q[ancilla])
    z.x(q[ancilla])
    
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

    xx.x(q[ancilla])
    xx.cx(q[system[0]], q[ancilla])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    xx.cry(theta, q[ancilla], q[system[0]])
    
    xx.cx(q[system[0]], q[ancilla])
    xx.x(q[ancilla])

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

    #ZZ pump
    zx.x(q[ancillae[0]])
    zx.cx(q[system[1]], q[ancillae[0]])
    
    theta = 2 * np.arcsin(np.sqrt(p))
    zx.cry(theta, q[ancillae[0]], q[system[1]])
    
    zx.cx(q[system[1]], q[ancillae[0]])
    zx.x(q[ancillae[0]])

    #XX pump
    zx.x(q[ancillae[1]])
    zx.cx(q[system[0]], q[ancillae[1]])
    
    zx.cry(theta, q[ancillae[1]], q[system[0]])
    
    zx.cx(q[system[0]], q[ancillae[1]])
    zx.x(q[ancillae[1]])
    
    zx.measure(q[system[0]], c[0])
    zx.measure(q[system[1]], c[1])
    
    return zx

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
sys = [1,2]
anc = [0]
q = QuantumRegister(4, name='q')
c = ClassicalRegister(2, name='c')
#Create circuit
circ = transpile(zz_pump(q, c, 0, sys, anc, '00'),backend=backend,optimization_level=0)
#Convert to Mitiq
circ_qasm = circ.qasm()
circ_mitiq = from_qiskit(circ)
#Convert to Qiskit
circ_folded_qasm = to_qasm(circ_mitiq)
circ_folded = QuantumCircuit.from_qasm_str(circ_folded_qasm)
#Rewrite and convert
circ_folded_qasm_rewritten = rewrite_qasm(circ_folded_qasm)
circ_folded_rewritten = QuantumCircuit.from_qasm_str(circ_folded_qasm_rewritten)
print(circ_qasm)
print('-----------------------------------------------------')
print(circ_folded_qasm)
print('-----------------------------------------------------')
print(circ_folded)
print('-----------------------------------------------------')
print(circ_folded_qasm_rewritten)
print('-----------------------------------------------------')
print(circ_folded_rewritten)
