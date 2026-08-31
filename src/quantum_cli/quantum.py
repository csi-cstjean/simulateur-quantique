"""Couche logique quantique, basée sur Qiskit et Aer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


@dataclass
class MeasurementResult:
    """Résultat de mesure dans un format simple."""

    counts: Dict[str, int]
    totals: int


class QuantumEngine:
    """Petit wrapper autour de Qiskit pour rendre le code pédagogique."""

    MAX_QUBITS = 16

    def __init__(self) -> None:
        self.circuit: Optional[QuantumCircuit] = None
        self.backend = AerSimulator()

    def create_circuit(self, qubits: int) -> str:
        """Crée un circuit dont la base est |0...0>."""
        if qubits <= 0:
            raise ValueError("number of qubits must be greater than 0.")
        if qubits > self.MAX_QUBITS:
            raise ValueError(f"maximum number of qubits is {self.MAX_QUBITS}.")
        self.circuit = QuantumCircuit(qubits)
        return f"Initialized {qubits} qubits."

    def reset(self) -> str:
        """Réinitialise le circuit."""
        self.circuit = None
        return "Circuit reset."

    def _require_circuit(self) -> QuantumCircuit:
        if self.circuit is None:
            raise ValueError("initialize a quantum circuit first.")
        return self.circuit

    def _valid_qubit(self, qubit: int) -> int:
        circuit = self._require_circuit()
        if qubit < 0 or qubit >= circuit.num_qubits:
            raise ValueError(f"qubit {qubit} does not exist.")
        return qubit

    def apply_h(self, qubit: int) -> None:
        """Applique la porte H sur un qubit."""
        self.circuit = self._require_circuit()
        self.circuit.h(self._valid_qubit(qubit))

    def apply_x(self, qubit: int) -> None:
        """Applique la porte X sur un qubit."""
        self.circuit = self._require_circuit()
        self.circuit.x(self._valid_qubit(qubit))

    def apply_y(self, qubit: int) -> None:
        """Applique la porte Y sur un qubit."""
        self.circuit = self._require_circuit()
        self.circuit.y(self._valid_qubit(qubit))

    def apply_z(self, qubit: int) -> None:
        """Applique la porte Z sur un qubit."""
        self.circuit = self._require_circuit()
        self.circuit.z(self._valid_qubit(qubit))

    def apply_cnot(self, control: int, target: int) -> None:
        """Applique la porte CNOT."""
        self.circuit = self._require_circuit()
        control = self._valid_qubit(control)
        target = self._valid_qubit(target)
        if control == target:
            raise ValueError("control and target qubits must be different.")
        self.circuit.cx(control, target)

    def apply_rx(self, qubit: int, angle_degrees: float) -> None:
        """Applique la porte RX(θ) où θ est en degrés."""
        self.circuit = self._require_circuit()
        angle_radians = np.radians(angle_degrees)
        self.circuit.rx(angle_radians, self._valid_qubit(qubit))

    def apply_ry(self, qubit: int, angle_degrees: float) -> None:
        """Applique la porte RY(θ) où θ est en degrés."""
        self.circuit = self._require_circuit()
        angle_radians = np.radians(angle_degrees)
        self.circuit.ry(angle_radians, self._valid_qubit(qubit))

    def apply_rz(self, qubit: int, angle_degrees: float) -> None:
        """Applique la porte RZ(θ) où θ est en degrés."""
        self.circuit = self._require_circuit()
        angle_radians = np.radians(angle_degrees)
        self.circuit.rz(angle_radians, self._valid_qubit(qubit))

    def get_state(self) -> np.ndarray:
        """Retourne l'état quantique dans l'ordre de bits attendu par la CLI."""
        circuit = self._require_circuit()
        state = Statevector.from_instruction(circuit).reverse_qargs()
        return np.asarray(state.data, dtype=complex)

    def get_probabilities(self) -> np.ndarray:
        """Retourne les probabilités de chaque état."""
        state = self.get_state()
        probabilities = np.abs(state) ** 2
        return probabilities

    def run_shots(self, shots: int = 1000) -> Dict[str, int]:
        """Exécute un circuit sur un qubit unique et retourne les comptes 0/1."""
        if shots <= 0:
            raise ValueError("number of shots must be greater than 0.")
        circuit = self._require_circuit()
        if circuit.num_qubits != 1:
            raise ValueError("run_shots is intended for 1-qubit circuits.")
        measurement = circuit.copy()
        measurement.measure_all()
        result = self.backend.run(measurement, shots=shots).result().get_counts()
        return {"0": int(result.get("0", 0)), "1": int(result.get("1", 0))}

    def measure(self, shots: int = 1) -> MeasurementResult:
        """Mesure le circuit en effectuant un nombre fixé de shots."""
        circuit = self._require_circuit()
        if shots <= 0:
            raise ValueError("number of shots must be greater than 0.")
        result_circuit = circuit.copy()
        result_circuit.measure_all()
        result = self.backend.run(result_circuit, shots=shots).result()
        counts = result.get_counts()
        normalized = {key: int(value) for key, value in counts.items()}
        return MeasurementResult(counts=normalized, totals=shots)

    @staticmethod
    def _mapping_from_bitstring(bitstring: str) -> Optional[int]:
        mapping = {
            "000": 1,
            "001": 2,
            "010": 3,
            "011": 4,
            "100": 5,
            "101": 6,
        }
        return mapping.get(bitstring, None)

    def sample_dice(self, shots: int = 1000) -> Dict[str, int]:
        """Lance un dé quantique équitable avec méthode de rejet pour 110 et 111."""
        if shots <= 0:
            raise ValueError("number of shots must be greater than 0.")

        counts = {str(i): 0 for i in range(1, 7)}
        accepted = 0
        circuit = QuantumCircuit(3)
        circuit.h(range(3))

        while accepted < shots:
            measurement = circuit.copy()
            measurement.measure_all()
            result = self.backend.run(measurement, shots=1).result().get_counts()
            bitstring = next(iter(result.keys()))
            mapping = self._mapping_from_bitstring(bitstring)
            if mapping is None:
                continue
            counts[str(mapping)] += 1
            accepted += 1
        return counts

    def sample_coin(self, shots: int = 1000) -> Dict[str, int]:
        """Lance une pièce quantique et retourne les comptes sur 0 et 1."""
        if shots <= 0:
            raise ValueError("number of shots must be greater than 0.")

        circuit = QuantumCircuit(1)
        circuit.h(0)
        measurement = circuit.copy()
        measurement.measure_all()
        result = self.backend.run(measurement, shots=shots).result().get_counts()
        counts = {"0": int(result.get("0", 0)), "1": int(result.get("1", 0))}
        return counts

    def bell_counts(self, shots: int = 1000) -> Dict[str, int]:
        """Simule l'état de Bell et retourne les comptes 00/11/01/10."""
        if shots <= 0:
            raise ValueError("number of shots must be greater than 0.")

        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        measurement = circuit.copy()
        measurement.measure_all()
        result = self.backend.run(measurement, shots=shots).result().get_counts()
        return {key: int(value) for key, value in result.items()}
