import numpy as np
from collections import Counter
import json

# importing Qiskit
from qiskit_ibm_provider import IBMProvider

provider = IBMProvider()

n = 15

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
    res = np.zeros(shape=(n,2))
    for i in range(n):
        cnt = counts[i]
        for j in range(2**4):
            if j%2 == 0:
                res[i][0] += cnt.get(bin(j)[2:].zfill(4),0)
            else:
                res[i][1] += cnt.get(bin(j)[2:].zfill(4),0)

    return res.tolist()

all_res = None
with open('./Jobs/Real/3.txt') as file:
    all_res = [return_counts(job_id) for job_id in file]

with open('./Data/Real/3.json','w') as file:
    json.dump(all_res, file)
