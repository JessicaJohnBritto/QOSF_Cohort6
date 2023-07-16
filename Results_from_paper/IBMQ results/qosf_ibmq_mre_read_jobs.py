import matplotlib.pyplot as plt
import numpy as np
import json

# importing Qiskit
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

#importing Mitiq
from mitiq.zne import inference

provider = IBMProvider()

probs = np.linspace(0,1,5)
shots = 20000
pump_list = ['ZZ pump','XX pump','ZZ XX pump']
ini_list = ['00','01','10','11']

all_res = None
with open('mre_11_res.json') as file:
    all_res = json.load(file)

all_res_sim = None
with open('mre_sim_res.json') as file:
    all_res_sim = json.load(file)

scale_factors = list(range(1,15))

res_mitigated = np.ndarray((len(pump_list),len(ini_list),len(probs)))
res_sim = np.ndarray((len(pump_list),len(ini_list),len(probs)))

##for i in range(len(pump_list)): #For the current pump
##    for j in range(len(ini_list)):  #For the current state
##        for k in range(len(probs)): #For the current probability
##            exp_vals = []
##            sf_real = []
##            for l in range(len(scale_factors)): #Get exp_val for each scale_factor
##                if all_res[l]==None:
##                    continue
##                exp_vals.append(all_res[l][i][j][k]/(4*shots))
##                sf_real.append(scale_factors[l])
##            try:
##                mitig_val = inference.ExpFactory.extrapolate(sf_real,exp_vals) #Extrapolate and get mitigated value
##                if k<1 or mitig_val>1.1 or mitig_val<-0.1:
##                    mitig_val = inference.LinearFactory.extrapolate(sf_real,exp_vals) #Extrapolate and get mitigated value
##            except inference.ExtrapolationError:
##                mitig_val = inference.LinearFactory.extrapolate(sf_real,exp_vals) #Extrapolate and get mitigated value
##            #res_mitigated[i,j,k] = all_res[0][i][j][k]/(4*shots)    #Store mitigated values
##            res_mitigated[i,j,k] = mitig_val    #Store mitigated values
##            res_sim[i,j,k] = all_res_sim[0][i][j][k]/(4*20000)  #Store simulated values

for i in range(len(pump_list)): #For the current pump
    fig, axs = plt.subplots(4,5,layout='tight')
    for k in range(len(probs)):
        axs[0,k].set_title(str(probs[k]))
    for j in range(len(ini_list)):
        axs[j,0].set_ylabel(ini_list[j])
    for j in range(len(ini_list)):  #For the current state
        for k in range(len(probs)): #For the current probability
            exp_vals = []
            sf_real = []
            for l in range(len(scale_factors)): #Get exp_val for each scale_factor
                if all_res[l]==None:
                    continue
                exp_vals.append(all_res[l][i][j][k]/(4*shots))
                sf_real.append(scale_factors[l])
            axs[j,k].scatter(sf_real,exp_vals,s=10)
    fig.suptitle(pump_list[i])
    fig.show()

##for pump_name,mitig_res,sim_res in zip(pump_list,res_mitigated,res_sim):
##    plt.title(pump_name)
##    plt.scatter(probs,np.array(mitig_res[0]),label='psi+ m',s=20)
##    plt.scatter(probs,np.array(mitig_res[1]),label='psi- m',s=20)
##    plt.scatter(probs,np.array(mitig_res[2]),label='phi+ m',s=20)
##    plt.scatter(probs,np.array(mitig_res[3]),label='phi- m',s=20)
##    plt.plot(probs,np.array(sim_res[0]),label='psi+ s',linestyle='--')
##    plt.plot(probs,np.array(sim_res[1]),label='psi- s',linestyle='--')
##    plt.plot(probs,np.array(sim_res[2]),label='phi+ s',linestyle='--')
##    plt.plot(probs,np.array(sim_res[3]),label='phi- s',linestyle='--')
##    plt.legend()
##    plt.show()
