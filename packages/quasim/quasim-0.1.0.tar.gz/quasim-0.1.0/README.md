# QuaSim: Qua(ntum Simulation made) Sim(ple)

[QuaSim](https://github.com/westoun/quasim) is a Python library for
simulating quantum circuits. It was created partly as a learning project,
partly out of necessity.
For my master thesis, I required a quantum circuit simulator that was easy
to set up, had low overhead, and was comparatively faster than [Qiskit](https://www.ibm.com/quantum/qiskit)
on the amount of qubits that my experiments required.

Aside from a low degree of overhead and dependencies (numpy only), QuaSim's speed gain
comes down to the way it detects and handles entanglement, since entanglement is the
reason why quantum circuits experience exponential resource growth when simulated
on classical computers.

Unless a qubit has been entangled with other qubits through the use of a controlled gate,
QuaSim stores and evolves its state independently from all other qubits.
Once two qubits become entangled, they form a joined qubit group, which is then stored and
evolved independently from the remaining qubits in the system.
Joined states are only used when they cannot be avoided.
At each time step, a completely unentangled circuit would only need to keep
track of N qubit states, instead of $2^N$ state combinations and, hence, would
only require gate matrices of dimension $2\times2$ instead of $2^N\times2^N$.

For a more foundational introduction to the mathematics and intuition of quantum
circuit simulation, I recommend [Aws Albarghouthi's](https://pages.cs.wisc.edu/~aws/)
great article ["A Quantum Circuit Simulator in 27 Lines of Python"](https://barghouthi.github.io/2021/08/05/quantum/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install quasim.

```bash
pip install quasim
```

## Usage

```python
from quasim import QuaSim, Circuit
from quasim.gates import H, CX, X

circuit = Circuit(2)
circuit.apply(H(target_qubit=0))
circuit.apply(CX(control_qubit=0, target_qubit=1))

simulator = QuaSim()
simulator.evaluate_circuit(circuit)

print(circuit.state)
print(circuit.probabilities)
print(circuit.probability_dict)
```

## Benchmarking

The benchmarking folder contains code that compares the performance of
QuaSim to [Qiskit](https://www.ibm.com/quantum/qiskit), a popular framework
in the context of quantum computing.
It compares both approaches in terms of execution time and simulation results.
Before executing any of the scripts,
make sure you have all the required requirements installed as specified in
benchmark/requirements.txt.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
