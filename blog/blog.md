# Simulating open quantum systems with qbraid-SDK

During the Quantum Computing Mentorship Program from the [Quantum Open Source Foundation](https://qosf.org/) (QOSF), which connects people
from diverse backgrounds with mentors from academia and industry, we had access to the Qbraid services. This blog will 
explain our experience using Qbraid in our project.

The project goal was to understand how to simulate open quantum systems using gate-based quantum computing. Using as a guide the previous 
work by [García-Pérez, et al.](https://www.nature.com/articles/s41534-019-0235-y).

We did simulations of two Open Quantum System models, Collisional and Markovian Reservoir, with noise simulations, 
the latest IBM devices (ibmq_kyoto, ibmq_osaka) and the Oxford Quantum Circuits (OQC) device Lucy. Extending on previous results. Using the [Mitiq](https://mitiq.readthedocs.io/en/stable/)
toolkit, we apply Zero-Noise extrapolation (ZNE), an error mitigation technique, and analyze their deviation from the theoretical 
results for the models under study. For both models, by applying ZNE, we reduced the error and overlapped it with the theoretical results.


Markovian Reservoir          |  Collisional Model 
:-------------------------:|:-------------------------:
<img src="mre_1.png" alt="drawing" width="400"/> | <img src="collisional.png" alt="drawing" width="400"/> 
*Results from ibmb_kyoto for the (Left) Markovian reservoir simulation and (Right) Collisional model with ZNE and 1024 shots. The points correspond
to the experimental results, while the dashed lines show the theoretical prediction*


One of the main hassles of working on this type of project is the different frameworks necessary to run the simulations 
and in real QPU. We used Mitiq, Qiskit, [Cirq](https://github.com/quantumlib/Cirq), and [AWS braket](https://github.com/amazon-braket/amazon-braket-sdk-python) in this project. Since Mitiq is based on Cirq, it is better 
to work directly with it and use Mitiq's noise scaling methods. Then, to run in the IBM QPUs, the circuits must be 
transpiled to Qiskit. We can do this by passing the Cirq circuits to QASM and then to Qiskit to use the transpile method.
Finally, to run the circuits in Lucy from OQC, AWS braket must be used. Given the gate basis for the hardware and topology, 
the circuit will increase in depth.

The use of multiple frameworks can complicate the actual applications that we want to explore with quantum computing. 
Using the QBraid-SDK environment, a Python toolkit for cross-framework abstraction, transpilation, and execution of
quantum programs on hardware and simulators, facilitated the implementation of multiple quantum frameworks. Also,
it facilitates the connection with AWS quantum services.

![Image](open_systes.png)
*Workflow used to simulated the Collisional and Markovian reservoir model using the qbraid-SDK*

Further results and models are explained in the [arxiv paper](https://arxiv.org/abs/2401.06535)