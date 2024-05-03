from qiskit import QuantumCircuit
from qiskit_scaleway import ScalewayProvider

provider = ScalewayProvider()

provider = ScalewayProvider(
    project_id="ae84de1f-c006-4383-8f92-8cc7f76bc07d",
    secret_key="6af5f1ab-cb28-4bc3-b297-9a95d4ac7c65",
    url='https://agw.stg.fr-par-2.internal.scaleway.com/qaas/v1alpha1'
)

# # List all operational backends
# backends = provider.backends(operational=False)
# print(backends)

# # List all backends with a minimum number of qbits
# backends = provider.backends(min_num_qubits=35)
# print(backends)

# Retrieve a backend by providing search criteria. The search must have a single match
backend = provider.get_backend("aer_simulation_4l40s")

# Define a quantum circuit that produces a 4-qubit GHZ state.
circuit = QuantumCircuit(2, 2, name='Bell state')
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()

circuit.draw()


shots = 1

# Create job to a new QPU's session (or on an existing one)
job = backend.run(circuit, shots=shots)


# Send your job
result = job.result()


print(result)
