import cirq
import numpy as np
import matplotlib.pyplot as plt

def zz_pump(sys,env,p):
    yield cirq.CNOT(sys[1],sys[0])
    #|phi+> -> |0>|+>
    #|phi-> -> |0>|->
    #|psi+> -> |1>|+>
    #|psi-> -> |1>|->
    #|phi+>, |phi-> are in +1 eigenspace of zz
    #activate effect if sys[0]==0
    yield cirq.X(env[0])
    yield cirq.CNOT(sys[0],env[0])
    #rotate according to pumping efficiency
    #RX(t)|0>=cos(t/2)|0>-isin(t/2)|1>
    #cos^2(t/2)=1-p => 1+cos(t)=2-2p => t=arccos(1-2p)
    yield cirq.Rx(rads=np.arccos(1-2*p)).on(sys[0]).controlled_by(env[0])
    #undo everything
    #do we really need the below CNOT? I don't think so...
    yield cirq.CNOT(sys[0],env[0])
    yield cirq.CNOT(sys[1],sys[0])

def xx_pump(sys,env,p):
    yield cirq.CNOT(sys[1],sys[0])
    #convert sys[1]: |+> -> |0>, |-> -> |1>
    yield cirq.H(sys[1])
    #|phi+>, |psi+> are in +1 eigenspace of xx
    #activate effect if sys[1]==0
    yield cirq.X(env[0])
    yield cirq.CNOT(sys[1],env[0])
    #now rotate on sys[1]
    yield cirq.Rx(rads=np.arccos(1-2*p)).on(sys[1]).controlled_by(env[0])
    yield cirq.CNOT(sys[1],env[0])
    #apply back the H
    yield cirq.H(sys[1])
    yield cirq.CNOT(sys[1],sys[0])

def zz_xx_pump(sys,env,p):
    yield cirq.CNOT(sys[1],sys[0])
    yield cirq.X(env[0])
    yield cirq.CNOT(sys[0],env[0])
    yield cirq.Rx(rads=np.arccos(1-2*p)).on(sys[0]).controlled_by(env[0])
    yield cirq.CNOT(sys[0],env[0])
    yield cirq.H(sys[1])
    yield cirq.X(env[1])
    yield cirq.CNOT(sys[1],env[1])
    yield cirq.Rx(rads=np.arccos(1-2*p)).on(sys[1]).controlled_by(env[1])
    yield cirq.CNOT(sys[1],env[1])
    yield cirq.H(sys[1])
    yield cirq.CNOT(sys[1],sys[0])


def encode_bell(sys):
    yield cirq.H(sys[0])
    yield cirq.CNOT(sys[0],sys[1])

def decode_bell(sys):
    yield cirq.CNOT(sys[0],sys[1])
    yield cirq.H(sys[0])

def calc_pump(pump,sys,env,p,repcnt):
    #|phi+>
    circuit00 = cirq.Circuit()
    circuit00.append(encode_bell(sys))
    circuit00.append(pump(sys,env,p))
    circuit00.append(decode_bell(sys))
    circuit00.append(cirq.measure(sys, key = 'answer'))

    #|psi+>
    circuit01 = cirq.Circuit()
    circuit01.append(cirq.X.on(sys[1]))
    circuit01.append(encode_bell(sys))
    circuit01.append(pump(sys,env,p))
    circuit01.append(decode_bell(sys))
    circuit01.append(cirq.measure(sys, key = 'answer'))

    #|phi->
    circuit10 = cirq.Circuit()
    circuit10.append(cirq.X.on(sys[0]))
    circuit10.append(encode_bell(sys))
    circuit10.append(pump(sys,env,p))
    circuit10.append(decode_bell(sys))
    circuit10.append(cirq.measure(sys, key = 'answer'))

    #|psi->
    circuit11 = cirq.Circuit()
    circuit11.append(cirq.X.on(sys[0]))
    circuit11.append(cirq.X.on(sys[1]))
    circuit11.append(encode_bell(sys))
    circuit11.append(pump(sys,env,p))
    circuit11.append(decode_bell(sys))
    circuit11.append(cirq.measure(sys, key = 'answer'))

    simulator = cirq.Simulator()

    result00 = simulator.run(circuit00,repetitions=repcnt)
    histogram00 = result00.histogram(key = 'answer')

    result01 = simulator.run(circuit01,repetitions=repcnt)
    histogram01 = result01.histogram(key = 'answer')

    result10 = simulator.run(circuit10,repetitions=repcnt)
    histogram10 = result10.histogram(key = 'answer')

    result11 = simulator.run(circuit11,repetitions=repcnt)
    histogram11 = result11.histogram(key = 'answer')

    final_hist = histogram00+histogram01+histogram10+histogram11

    for x in final_hist:
        final_hist[x]/=(4*repcnt)

    return final_hist

def calc_plot(pump,sys,env,probs,repcnt):
    hists = [calc_pump(pump,sys,env,p,repcnt) for p in probs]
    pops = [[],[],[],[]]
    for counts in hists:
        for i in range(4):
            pops[i].append(counts[i])

    plt.scatter(probs,pops[0],label='|phi+>')
    plt.scatter(probs,pops[1],label='|psi+>')
    plt.scatter(probs,pops[2],label='|phi->')
    plt.scatter(probs,pops[3],label='|psi->')
    plt.legend()
    plt.show()
    
env = [cirq.LineQubit(0),cirq.LineQubit(3)]
sys = [cirq.LineQubit(1),cirq.LineQubit(2)]
probs = np.linspace(0,1,num=20)
repcnt = 1000

calc_plot(zz_pump,sys,env,probs,repcnt)
calc_plot(xx_pump,sys,env,probs,repcnt)
calc_plot(zz_xx_pump,sys,env,probs,repcnt)
