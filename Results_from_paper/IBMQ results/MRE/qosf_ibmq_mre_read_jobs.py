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

probs = np.linspace(0,1,5)
shots = 4000
pump_list = ['ZZ pump','XX pump','ZZ XX pump']
ini_list = ['00','01','10','11']
ini_state_list = [r'$|00\rangle$',r'$|01\rangle$',r'$|10\rangle$',r'$|11\rangle$']
fin_state_list = [r'$\mid\Phi+\rangle$',r'$\mid\Phi-\rangle$',r'$\mid\Psi+\rangle$',r'$\mid\Psi-\rangle$']


with open('./Data/Real/mre_13_res.json') as file:
    all_res = json.load(file)

with open('./Data/Sim/mre_sim_13_res.json') as file:
    all_res_sim = json.load(file)

scale_factors = [1,2,3,4]

res_real = np.zeros((len(pump_list),len(ini_list),len(probs),4))
res_mit = np.zeros((len(pump_list),len(ini_list),len(probs),4))
res_sim = np.zeros((len(pump_list),len(ini_list),len(probs),4))

fin_res_real = np.zeros((len(pump_list),len(ini_list),len(probs)))
fin_res_mit = np.zeros((len(pump_list),len(ini_list),len(probs)))
fin_res_sim = np.zeros((len(pump_list),len(ini_list),len(probs)))

def mitigate(scale_factors,exp_vals):
##    try:
##        mit_val,std_dev,opt_par,cov_mat,model = inference.LinearFactory.extrapolate(scale_factors,exp_vals,full_output=True)
##        print(f'Standard deviation from linear fit is {std_dev}. Value is {mit_val}.')
##        if std_dev>1:
##            print('Standard deviation too large, using linear fit.')
##            mit_val,std_dev,opt_par,cov_mat,model = inference.LinearFactory.extrapolate(scale_factors,exp_vals,full_output=True)
##            print(f'Standard deviation from linear fit is {std_dev}. Value is {mit_val}.')
##    except inference.ExtrapolationError:
##        print('Exponential fit failed, using linear fit.')
##        mit_val,std_dev,opt_par,cov_mat,model = inference.LinearFactory.extrapolate(scale_factors,exp_vals,full_output=True)
##        print(f'Standard deviation from linear fit is {std_dev}. Value is {mit_val}.')
##    print(f'--------------------------------------------------------------------------------------------------------------')
    mit_val,std_dev,opt_par,cov_mat,model = inference.LinearFactory.extrapolate(scale_factors,exp_vals,full_output=True)
    print(f'Standard deviation from linear fit is {std_dev}. Value is {mit_val}.')
    return mit_val


for i in range(len(pump_list)): #For the current pump
    for j in range(len(ini_list)):  #For the initial state
        for k in range(len(probs)): #For the current probability
            for l in range(4): #For the final state
                exp_vals = []
                sf_real = []
                for m in range(len(scale_factors)): #Get exp_val for each scale_factor
                    if all_res[m]==None:
                        continue
                    exp_vals.append(all_res[m][i][j][k][l]/shots)
                    sf_real.append(scale_factors[m])
                res_real[i,j,k,l] = all_res[0][i][j][k][l]/shots    #Store real values
                print(f'Mitigating {pump_list[i]} for ' + ini_list[j] + '->' + ini_list[l] + f' with probability {probs[k]}.')
                res_mit[i,j,k,l] = mitigate(sf_real,exp_vals)    #Store mitigated values
                res_sim[i,j,k,l] = all_res_sim[0][i][j][k][l]/20000  #Store simulated values

for i in range(len(pump_list)): #For the current pump
    for j in range(len(ini_list)):  #For the initial state
        for k in range(len(probs)): #For the current probability
            for l in range(4): #For the final state
                fin_res_real[i,l,k] += res_real[i,j,k,l]
                fin_res_mit[i,l,k] += res_mit[i,j,k,l]
                fin_res_sim[i,l,k] += res_sim[i,j,k,l]

fin_res_real /= 4
fin_res_mit /= 4
fin_res_sim /= 4

#00 phi+
#01 phi-
#10 psi+
#11 psi-

plt.rcParams['text.usetex'] = True
plt.rc('axes', axisbelow=True)

for pump_name,real_res,mit_res,sim_res in zip(pump_list,fin_res_real,fin_res_mit,fin_res_sim):
    plt.grid()
    plt.title(pump_name)
    for j in range(4):
##        plt.scatter(probs,np.array(real_res[j]),label=fin_state_list[j],s=20)
        plt.scatter(probs,np.array(mit_res[j]),label=fin_state_list[j],s=20)
        plt.plot(probs,np.array(sim_res[j]),linestyle='--')
    plt.xticks(probs,fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel(r'$p$',fontsize=15)
    plt.ylabel(r'Overlap',fontsize=15)
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
