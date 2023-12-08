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
    res = np.ndarray(shape=(3,4,len(probs),4))
    for pump in range(3):
        for ini in range(4):
            for prob in range(len(probs)):
                pos = np.ravel_multi_index((pump,ini,prob),(3,4,len(probs)))
                cnt = counts[pos]
                res[pump][ini][prob][0] = cnt.get('00',0)+cnt.get('0 0',0)
                res[pump][ini][prob][1] = cnt.get('01',0)+cnt.get('0 1',0)
                res[pump][ini][prob][2] = cnt.get('10',0)+cnt.get('1 0',0)
                res[pump][ini][prob][3] = cnt.get('11',0)+cnt.get('1 1',0)

    return res.tolist()

all_res = None
with open('./Jobs/Real_new/1.txt') as file:
    all_res = [return_counts(job_id) for job_id in file]

with open('./Data/Real_new/1.json','w') as file:
    json.dump(all_res, file)
