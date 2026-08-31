"""Interface CLI du simulateur quantique."""

from __future__ import annotations

from quantum_cli.display import format_probabilities, format_state_vector
from quantum_cli.experiments import (
    bell_experiment,
    coin_experiment,
    dice_experiment,
    loaded_dice_experiment,
)
from quantum_cli.explanations import explain
from quantum_cli.quantum import QuantumEngine


class QuantumCLI:
    """Parse les commandes et exécute les actions associées."""

    def __init__(self) -> None:
        self.engine = QuantumEngine()

    def handle_command(self, raw_command: str) -> str:
        """Interprète une commande utilisateur."""
        command = raw_command.strip()
        if not command:
            return ""

        if command == "exit":
            return "Au revoir."

        if command == "help":
            return self._help_text()

        if command.startswith("qubits "):
            try:
                count = int(command.split()[1])
            except ValueError:
                return "Erreur : nombre de qubits invalide."
            try:
                return self.engine.create_circuit(count)
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command == "reset":
            return self.engine.reset()

        if command.startswith("h "):
            try:
                q = int(command.split()[1])
            except ValueError:
                return "Utilisation : h Q"
            try:
                self.engine.apply_h(q)
                return f"Porte H appliquée sur q{q}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("x "):
            try:
                q = int(command.split()[1])
            except ValueError:
                return "Utilisation : x Q"
            try:
                self.engine.apply_x(q)
                return f"Porte X appliquée sur q{q}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("y "):
            try:
                q = int(command.split()[1])
            except ValueError:
                return "Utilisation : y Q"
            try:
                self.engine.apply_y(q)
                return f"Porte Y appliquée sur q{q}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("z "):
            try:
                q = int(command.split()[1])
            except ValueError:
                return "Utilisation : z Q"
            try:
                self.engine.apply_z(q)
                return f"Porte Z appliquée sur q{q}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("cnot "):
            parts = command.split()
            if len(parts) != 3:
                return "Utilisation : cnot CONTRÔLE CIBLE"
            try:
                control = int(parts[1])
                target = int(parts[2])
                self.engine.apply_cnot(control, target)
                return f"Porte CNOT appliquée : q{control} -> q{target}"
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("rx "):
            parts = command.split()
            if len(parts) != 3:
                return "Utilisation : rx Q ANGLE"
            try:
                qubit = int(parts[1])
                angle = float(parts[2])
                self.engine.apply_rx(qubit, angle)
                return f"Porte RX({angle}°) appliquée sur q{qubit}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("ry "):
            parts = command.split()
            if len(parts) != 3:
                return "Utilisation : ry Q ANGLE"
            try:
                qubit = int(parts[1])
                angle = float(parts[2])
                self.engine.apply_ry(qubit, angle)
                return f"Porte RY({angle}°) appliquée sur q{qubit}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command.startswith("rz "):
            parts = command.split()
            if len(parts) != 3:
                return "Utilisation : rz Q ANGLE"
            try:
                qubit = int(parts[1])
                angle = float(parts[2])
                self.engine.apply_rz(qubit, angle)
                return f"Porte RZ({angle}°) appliquée sur q{qubit}."
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command == "state":
            try:
                state = self.engine.get_state()
                return format_state_vector(state)
            except ValueError as exc:
                return f"Error: {exc}"

        if command == "probabilities":
            try:
                probs = self.engine.get_probabilities()
                return format_probabilities(probs)
            except ValueError as exc:
                return f"Error: {exc}"

        if command.startswith("measure"):
            parts = command.split()
            shots = 1
            if len(parts) > 1:
                try:
                    shots = int(parts[1])
                except ValueError:
                    return "Utilisation : measure [N]"
            try:
                result = self.engine.measure(shots)
                output = ["Résultats de mesure :"]
                if shots == 1:
                    bitstring = next(iter(result.counts))
                    reversed_bitstring = bitstring[::-1]
                    output = [f"Résultat de mesure : {reversed_bitstring}"]
                else:
                    reversed_counts = {k[::-1]: v for k, v in result.counts.items()}
                    for bitstring, count in sorted(reversed_counts.items()):
                        probability = count / result.totals
                        output.append(f"|{bitstring}>    {count}    {probability * 100:.2f}%")
                return "\n".join(output)
            except ValueError as exc:
                return f"Erreur : {exc}"

        if command == "coin":
            counts = coin_experiment(1000)
            heads = counts.get("0", 0)
            tails = counts.get("1", 0)
            return f"Pile ou face quantique\n\nFACE : {heads}\nPILE : {tails}"

        if command.startswith("coin "):
            try:
                shots = int(command.split()[1])
            except ValueError:
                return "Utilisation : coin [N]"
            counts = coin_experiment(shots)
            heads = counts.get("0", 0)
            tails = counts.get("1", 0)
            return f"Pile ou face quantique\n\nFACE : {heads}\nPILE : {tails}"

        if command == "dice":
            counts = dice_experiment(1000)
            return self._format_face_counts(counts)

        if command.startswith("dice "):
            try:
                shots = int(command.split()[1])
            except ValueError:
                return "Utilisation : dice [N]"
            counts = dice_experiment(shots)
            return self._format_face_counts(counts)

        if command == "loaded-dice":
            return format_state_vector(loaded_dice_experiment())

        if command == "bell":
            counts = bell_experiment(1000)
            lines = ["État de Bell :"]
            for bitstring, ratio in sorted(counts.items()):
                lines.append(f"|{bitstring}>    {ratio}")
            return "\n".join(lines)

        if command.startswith("bell "):
            try:
                shots = int(command.split()[1])
            except ValueError:
                return "Utilisation : bell [N]"
            counts = bell_experiment(shots)
            lines = ["État de Bell :"]
            for bitstring, value in sorted(counts.items()):
                lines.append(f"|{bitstring}>    {value}")
            return "\n".join(lines)

        if command.startswith("explain "):
            target = command.split()[1]
            return explain(target)

        return f"Unknown command: {command}"

    def _help_text(self) -> str:
        return """Simulation Quantique

==== Simulation ====
qubits N
state
measure [N]
reset

==== Portes de Pauli ====
x Q
y Q
z Q

==== Porte de Hadamard ====
h Q

==== Portes à plusieurs qubits ====
cnot CONTRÔLE CIBLE

==== Portes de rotation ====
rx Q ANGLE
ry Q ANGLE
rz Q ANGLE

==== Exemples d'utilisation ====
coin [N]
dice [N]
loaded-dice
bell [N]

==== Explications pédagogiques ====
explain [x | y | z | h | cnot | rx | ry | rz | measure | coin | dice | loaded-dice | bell]
probabilities

==== Quitter ====
exit
"""

    def _format_face_counts(self, counts: dict[str, int]) -> str:
        lines = ["Faces :"]
        for face in sorted(counts, key=lambda k: int(k)):
            lines.append(f"{face} : {counts[face]}")
        return "\n".join(lines)




def main() -> None:
    """Boucle interactive principale."""
    print("Quantum CLI")
    print("Version 0.1.0")
    print("Atelier pédagogique de calcul quantique")
    print("Un qubit peut être dans une superposition. Tapez 'help' pour voir les commandes.")
    cli = QuantumCLI()
    while True:
        try:
            raw = input("> ")
        except EOFError:
            print()
            break
        if raw.strip() == "exit":
            print("Au revoir.")
            break
        response = cli.handle_command(raw)
        if response:
            print(response)


if __name__ == "__main__":
    main()
