# Instructions:
- First, use qosf_ibmq_mre.py to send the jobs to IBMQ and write the job IDs to a file as ./Jobs/FILE.txt.
- Write down a summary of what data FILE.txt contains as a new entry in ./Jobs/mre_settings.txt.
- Second, use qosf_ibmq_mre_fetch_and_store_jobs.py to read FILE.txt and fetch the job results, and then write the data to a JSON file as ./Data/FILE_res.json.
- Third, use qosf_ibmq_mre_read_jobs.py to read the data from FILE_res.json and analyze it.
