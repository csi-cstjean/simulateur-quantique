from quantum_cli.cli import QuantumCLI


def test_cli_handles_qubits_and_reset():
    cli = QuantumCLI()
    assert cli.handle_command("qubits 2") == "Initialized 2 qubits."
    assert cli.handle_command("reset") == "Circuit reset."
    help_text = cli.handle_command("help")
    # Check for pedagogical structure in the new help text
    assert "Simulation" in help_text and "Portes de Pauli" in help_text
    assert cli.handle_command("exit") == "Au revoir."
