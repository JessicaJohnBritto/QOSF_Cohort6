import cirq
from numpy import binary_repr
import matplotlib.pyplot as plt

#get numbers and bits required
a = int(input("Input a: "))
b = int(input("Input b: "))
bitcnt = max(len(binary_repr(a)),len(binary_repr(b)))
a_repr = binary_repr(a,bitcnt)
b_repr = binary_repr(b,bitcnt)

#declare registers
a_reg = cirq.LineQubit.range(bitcnt)
b_reg = cirq.LineQubit.range(bitcnt,2*bitcnt)
res_reg = cirq.LineQubit.range(2*bitcnt,4*bitcnt)

#prepare states of registers
def num_prep(rep,reg):
    bitcnt = len(reg)
    for i in range(bitcnt):
        if int(rep[i]) == 1:
            yield cirq.X(reg[i])

circuit = cirq.Circuit()
circuit.append(num_prep(a_repr,a_reg))
circuit.append(num_prep(b_repr,b_reg))

#make qft generator
def qft(reg):
    bitcnt = len(reg)
    for i in range(bitcnt):
        yield cirq.H(reg[i])
        for j in range(i+1,bitcnt):
            rot_gate = cirq.CZPowGate(exponent = 0.5**(j-i))
            yield rot_gate(reg[j],reg[i])

#use qft subcircuit to transform res_reg
circuit.append(qft(res_reg))

#multiply a and b
def multiplier(reg_1,reg_2,reg_3):
    bitcnt = len(reg_1)
    for i in range(bitcnt):
        for j in range(bitcnt):
            for k in range(2*bitcnt):
                rot_gate = cirq.CCZPowGate(exponent = 0.5**(i+j+1-k))
                yield rot_gate(reg_1[i],reg_2[j],reg_3[k])

def adder(reg_1,reg_2):
    bitcnt = len(reg_1)
    for i in range(bitcnt):
        for j in range(2*bitcnt):
            rot_gate = cirq.CZPowGate(exponent = 0.5**(i-j+bitcnt))
            yield rot_gate(reg_1[i],reg_2[j])

circuit.append(multiplier(a_reg,b_reg,res_reg))
#circuit.append(adder(a_reg,res_reg))
#circuit.append(adder(b_reg,res_reg))

#inverse qft on result
def iqft(reg):
    bitcnt = len(reg)
    for i in reversed(range(0,bitcnt)):
        for j in reversed(range(i+1,bitcnt)):
            rot_gate = cirq.CZPowGate(exponent = -0.5**(j-i))
            yield rot_gate(reg[j],reg[i])
        yield cirq.H(reg[i])

circuit.append(iqft(res_reg))

#get result
circuit.append(cirq.measure(res_reg, key = 'answer'))
simulator = cirq.Simulator()
result = simulator.run(circuit)
histogram = result.histogram(key = 'answer')
_ = cirq.plot_state_histogram(histogram, plt.subplot())
plt.show()
#print(result)

#print(circuit)
