"""Fonctions d'affichage pédagogique pour les états, probabilités et circuits."""

from __future__ import annotations

from typing import Sequence


def format_state_vector(state: Sequence[complex], show_all: bool = False) -> str:
    """Affiche un état quantique avec amplitudes et probabilités."""
    lines: list[str] = ["Quantum state:"]
    for index, amplitude in enumerate(state):
        # Round to 10 decimal places to avoid floating-point artifacts
        amplitude_rounded = round(amplitude.real, 10) + round(amplitude.imag, 10) * 1j
        probability = abs(amplitude_rounded) ** 2
        if not show_all and abs(amplitude_rounded) < 1e-10:
            continue
        bitstring = format(index, f"0{int(__import__('math').log2(len(state)))}b") if len(state) > 1 else "0"
        # Display as real if imaginary part is negligible
        amplitude_display = amplitude_rounded.real if abs(amplitude_rounded.imag) < 1e-12 else amplitude_rounded
        lines.append(
            f"|{bitstring}>    amplitude = {amplitude_display}    "
            f"probability = {probability * 100:.3f}%"
        )
    return "\n".join(lines)


def format_probabilities(probabilities: Sequence[float]) -> str:
    """Affiche les probabilités sous forme lisible."""
    lines: list[str] = []
    for index, value in enumerate(probabilities):
        # Round to 10 decimal places to avoid floating-point artifacts
        value_rounded = round(value, 10)
        if value_rounded < 1e-10:
            continue
        bitstring = format(index, f"0{int(__import__('math').log2(len(probabilities)))}b") if len(probabilities) > 1 else "0"
        lines.append(f"|{bitstring}>    {value_rounded * 100:.3f}%")
    return "\n".join(lines)


def format_counts(counts: dict[str, int]) -> str:
    """Affiche les résultats d'un tirage avec les comptages."""
    lines = ["Measurement results:"]
    for key, value in sorted(counts.items()):
        lines.append(f"|{key}>    {value}")
    return "\n".join(lines)
