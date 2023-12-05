import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator
import numpy as np
import json

# importing Qiskit
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

#importing Mitiq
from mitiq.zne import inference

provider = IBMProvider()

shots = 4000
n = 15
tt = np.pi/6
g = 1
t = g*(tt)
T = [i*t for i in range(1,n+1)]

with open('./Data/Real/1.json') as file:
    all_res = json.load(file)

with open('./Data/Sim/1.json') as file:
    all_res_sim = json.load(file)

scale_factors = [1,2,3,4]

res_real = np.zeros((n))
res_mit = np.zeros((n))
res_sim = np.zeros((n))

def mitigate(scale_factors,exp_vals):
    mit_val,std_dev,opt_par,cov_mat,model = inference.LinearFactory.extrapolate(scale_factors,exp_vals,full_output=True)
    print(f'Standard deviation from linear fit is {std_dev}. Value is {mit_val}.')
    return mit_val


for i in range(n): #For the current collision count
    exp_vals = []
    sf_real = []
    for m in range(len(scale_factors)): #Get exp_val for each scale_factor
        if all_res[m]==None:
            continue
        exp_vals.append(all_res[m][i][0]/shots)
        sf_real.append(scale_factors[m])
    res_real[i] = all_res[0][i][0]/shots    #Store real values
    print(f'Mitigating collision count {i+1}.')
    res_mit[i] = mitigate(sf_real,exp_vals)    #Store mitigated values
    res_sim[i] = all_res_sim[0][i][0]/20000  #Store simulated values

plt.rcParams['text.usetex'] = True

plt.rc('axes', axisbelow=True)
plt.grid()
plt.title('Collisional model (correlated case)')
plt.scatter(T,res_real,s=20,c='red',label='Unmitigated')
plt.scatter(T,res_mit,s=20,c='green',label='Mitigated')
plt.plot(T,res_sim,linestyle='--')
plt.xticks(T[::2],fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel(r'$t$',fontsize=15)
plt.ylabel(r'$Re(\rho_{12})$',fontsize=15)
plt.legend()
plt.show()

plt.rcParams['text.usetex'] = False

##for i in range(len(pump_list)): #For the current pump
##    for j in range(4):  #For the current initial state
##        fig, axs = plt.subplots(4,5,figsize=(10,6),layout='constrained')
##        for k in range(len(probs)):
##            axs[0,k].set_title(str(probs[k]))
##        for l in range(len(ini_list)):
##            axs[l,0].set_ylabel(ini_state_list[l])
##        for l in range(len(ini_list)):  #For the final state
##            for k in range(len(probs)): #For the current probability
##                exp_vals = []
##                sf_real = []
##                for m in range(len(scale_factors)): #Get exp_val for each scale_factor
##                    if all_res[m]==None:
##                        continue
##                    exp_vals.append(all_res[m][i][j][k][l]/shots)
##                    sf_real.append(scale_factors[m])
##                axs[l,k].scatter(sf_real,exp_vals,s=10)
##                axs[l,k].xaxis.set_major_locator(MultipleLocator(5))
##                axs[l,k].yaxis.set_major_locator(LinearLocator(numticks=4))
##        fig.suptitle(pump_list[i]+' '+ini_state_list[j])
##    plt.show()
