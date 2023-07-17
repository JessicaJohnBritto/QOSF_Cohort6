import numpy as np
from collections import Counter
import json

# importing Qiskit
from qiskit_ibm_provider import IBMProvider

provider = IBMProvider()

probs = np.linspace(0,1,5)
ini_list = ['00','01','10','11']

#00 phi+
#01 phi-
#10 psi+
#11 psi-

def return_counts(job_id):
    counts = None
    job = provider.backend.retrieve_job(job_id.strip())
    if not job.done():
        print(job_id.strip()+' is not complete') # to avoid silent fail
        return counts
    results = job.result()
    counts = results.get_counts()
    pump_res = []
    for i in range(0,60,len(ini_list)*len(probs)):
        y_00 = []
        y_01 = []
        y_10 = []
        y_11 = []
        
        for j in range(len(probs)):
            cnt = Counter()
            cnt += Counter(counts[i+j])
            cnt += Counter(counts[i+j+5])
            cnt += Counter(counts[i+j+10])
            cnt += Counter(counts[i+j+15])
            y_00.append(cnt.get('00',0)+cnt.get('0 0',0))
            y_01.append(cnt.get('01',0)+cnt.get('0 1',0))
            y_10.append(cnt.get('10',0)+cnt.get('1 0',0))
            y_11.append(cnt.get('11',0)+cnt.get('1 1',0))
        pump_res.append([y_00,y_01,y_10,y_11])

    return pump_res

all_res = None
with open('mre_sim_12.txt') as file:
    all_res = [return_counts(job_id) for job_id in file]

with open('mre_sim_12_res.json','w') as file:
    json.dump(all_res, file)
