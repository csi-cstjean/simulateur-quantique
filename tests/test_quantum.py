import math

from quantum_cli.quantum import QuantumEngine


def test_initial_state_two_qubits():
    engine = QuantumEngine()
    engine.create_circuit(2)
    state = engine.get_state()
    assert state[0] == 1 + 0j
    assert all(abs(v) < 1e-12 for v in state[1:])


def test_hadamard_has_balanced_distribution():
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_h(0)
    counts = engine.run_shots(2000)
    assert abs(counts.get("0", 0) - counts.get("1", 0)) < 500


def test_cnot_basis_mapping():
    engine = QuantumEngine()
    engine.create_circuit(2)
    engine.apply_cnot(0, 1)
    state = engine.get_state()
    assert abs(state[0] - 1) < 1e-9
    assert all(abs(v) < 1e-9 for v in state[1:])

    engine.reset()
    engine.create_circuit(2)
    engine.apply_x(1)
    engine.apply_cnot(0, 1)
    state = engine.get_state()
    assert abs(state[1] - 1) < 1e-9


def test_x_gate():
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_x(0)
    state = engine.get_state()
    assert abs(state[0]) < 1e-12
    assert abs(state[1] - 1) < 1e-12


def test_y_gate():
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_y(0)
    state = engine.get_state()
    assert abs(state[0]) < 1e-12
    # Y|0> = i|1>, so the amplitude should be i (or -i depending on convention)
    assert abs(abs(state[1]) - 1) < 1e-12
    # Check that it's complex
    assert abs(state[1].imag) > 0.99

    engine.reset()
    engine.create_circuit(1)
    engine.apply_x(0)
    engine.apply_y(0)
    state = engine.get_state()
    # Y|1> = -i|0>
    assert abs(abs(state[0]) - 1) < 1e-12
    assert abs(state[1]) < 1e-12


def test_z_gate():
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_z(0)
    state = engine.get_state()
    assert abs(state[0] - 1) < 1e-12
    assert abs(state[1]) < 1e-12

    engine.reset()
    engine.create_circuit(1)
    engine.apply_x(0)
    engine.apply_z(0)
    state = engine.get_state()
    assert abs(state[0]) < 1e-12
    assert abs(state[1] + 1) < 1e-12


def test_rx_identity():
    """RX(0°) doit être l'identité."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_rx(0, 0)
    state = engine.get_state()
    assert abs(state[0] - 1) < 1e-9
    assert abs(state[1]) < 1e-9


def test_rx_180_flips_qubit():
    """RX(180°) doit inverser le qubit (similaire à X, à une phase près)."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_rx(0, 180)
    state = engine.get_state()
    assert abs(state[0]) < 1e-9
    assert abs(abs(state[1]) - 1) < 1e-9


def test_rx_progressive():
    """RX progressif doit modifier les amplitudes."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_rx(0, 90)
    state = engine.get_state()
    expected = math.cos(math.radians(45))
    assert abs(abs(state[0]) - expected) < 1e-9
    assert abs(abs(state[1]) - expected) < 1e-9


def test_ry_identity():
    """RY(0°) doit être l'identité."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_ry(0, 0)
    state = engine.get_state()
    assert abs(state[0] - 1) < 1e-9
    assert abs(state[1]) < 1e-9


def test_ry_90_balanced():
    """RY(90°) appliqué à |0> doit donner 50/50."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_ry(0, 90)
    probs = engine.get_probabilities()
    assert abs(probs[0] - 0.5) < 0.01
    assert abs(probs[1] - 0.5) < 0.01


def test_ry_60_correct_probabilities():
    """RY(60°) appliqué à |0> doit donner cos²(30°)≈0.75 et sin²(30°)≈0.25."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_ry(0, 60)
    state = engine.get_state()
    expected_0 = math.cos(math.radians(30))
    expected_1 = math.sin(math.radians(30))
    assert abs(state[0] - expected_0) < 1e-9
    assert abs(state[1] - expected_1) < 1e-9


def test_ry_180_flips_qubit():
    """RY(180°) doit inverser le qubit."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_ry(0, 180)
    state = engine.get_state()
    assert abs(state[0]) < 1e-9
    assert abs(abs(state[1]) - 1) < 1e-9


def test_rz_identity():
    """RZ(0°) doit être l'identité."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_rz(0, 0)
    state = engine.get_state()
    assert abs(state[0] - 1) < 1e-9
    assert abs(state[1]) < 1e-9


def test_rz_no_probability_change_on_basis_state():
    """RZ ne doit pas changer les probabilités d'un état de base."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_rz(0, 90)
    state = engine.get_state()
    probs = abs(state) ** 2
    assert abs(probs[0] - 1.0) < 1e-9
    assert abs(probs[1]) < 1e-9


def test_rz_phase_on_superposition():
    """RZ doit introduire une phase complexe sur une superposition."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_h(0)
    engine.apply_rz(0, 90)
    state = engine.get_state()
    # Les probabilités restent 50/50
    probs = abs(state) ** 2
    assert abs(probs[0] - 0.5) < 1e-9
    assert abs(probs[1] - 0.5) < 1e-9
    # Mais les amplitudes sont complexes
    assert abs(state[0].imag) > 0.1
    assert abs(state[1].imag) > 0.1


def test_rotations_preserve_normalization():
    """Les rotations doivent préserver la normalisation."""
    engine = QuantumEngine()
    engine.create_circuit(2)
    engine.apply_h(0)
    engine.apply_ry(1, 45)
    engine.apply_rz(0, 90)
    state = engine.get_state()
    norm = sum(abs(v) ** 2 for v in state)
    assert abs(norm - 1.0) < 1e-9

