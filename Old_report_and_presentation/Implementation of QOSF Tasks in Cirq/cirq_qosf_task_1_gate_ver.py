import cirq
from numpy import binary_repr
import matplotlib.pyplot as plt

#make necessary gates and subcircuits
class QFT(cirq.Gate):
    """Gate that performs QFT on a specified number of qubits."""
    
    def __init__(self,qbits):
        super(QFT, self)
        self.qbits = qbits

    def _num_qubits_(self):
        return self.qbits

    def _decompose_(self, reg):
        for i in range(self.num_qubits()):
            yield cirq.H(reg[i])
            for j in range(i+1,self.num_qubits()):
                yield cirq.CZPowGate(exponent = 0.5**(j-i)).on(reg[j],reg[i])

    def _circuit_diagram_info_(self, args):
        return ["QFT"] * self.num_qubits()

def num_prep(rep,reg):
    """Takes a bitstring representation and prepares reg accordingly."""
    
    bitcnt = len(reg)
    for i in range(bitcnt):
        if int(rep[i]) == 1:
            yield cirq.X(reg[i])

def multiplier(reg_1,reg_2,reg_3):
    """Multiplies reg_1 and reg_2 and stores the result in reg_3."""
    
    bitcnt = len(reg_1)
    for i in range(bitcnt):
        for j in range(bitcnt):
            for k in range(2*bitcnt):
                rot_gate = cirq.CCZPowGate(exponent = 0.5**(i+j+1-k))
                yield rot_gate(reg_1[i],reg_2[j],reg_3[k])

def adder(reg_1,reg_2):
    """Adds reg_1 to reg_2."""
    
    bitcnt = len(reg_1)
    for i in range(bitcnt):
        for j in range(2*bitcnt):
            rot_gate = cirq.CZPowGate(exponent = 0.5**(i-j+bitcnt))
            yield rot_gate(reg_1[i],reg_2[j])

#get numbers and bits required
a = int(input("Input a: "))
b = int(input("Input b: "))
bitcnt = max(len(binary_repr(a)),len(binary_repr(b)))
a_repr = binary_repr(a,bitcnt)
b_repr = binary_repr(b,bitcnt)

#declare registers and circuit
a_reg = cirq.LineQubit.range(bitcnt)
b_reg = cirq.LineQubit.range(bitcnt,2*bitcnt)
res_reg = cirq.LineQubit.range(2*bitcnt,4*bitcnt)
circuit = cirq.Circuit()

#prepare states of registers
circuit.append(num_prep(a_repr,a_reg))
circuit.append(num_prep(b_repr,b_reg))

#use qft gate to transform res_reg
circuit.append(QFT(qbits = len(res_reg)).on(*res_reg))

#multiply a and b
circuit.append(multiplier(a_reg,b_reg,res_reg))

#inverse qft on result
circuit.append(cirq.inverse(QFT(qbits = len(res_reg)).on(*res_reg)))

#measure res_reg
circuit.append(cirq.measure(res_reg, key = 'answer'))

#simulate circuit and get result
simulator = cirq.Simulator()
result = simulator.run(circuit)

#print result
histogram = result.histogram(key = 'answer')
_ = cirq.plot_state_histogram(histogram, plt.subplot())
print(circuit)
plt.show()
