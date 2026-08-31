"""Expériences pédagogiques: pièce, dé, Bell."""

from __future__ import annotations

from typing import Dict

import numpy as np

from quantum_cli.quantum import QuantumEngine


def coin_experiment(shots: int = 1000) -> Dict[str, int]:
    """Simule un tirage de pièce quantique."""
    engine = QuantumEngine()
    engine.create_circuit(1)
    engine.apply_h(0)
    return engine.sample_coin(shots)


def dice_experiment(shots: int = 1000) -> Dict[str, int]:
    """Simule un dé quantique avec rejet pour les états 110 et 111."""
    engine = QuantumEngine()
    engine.create_circuit(3)
    return engine.sample_dice(shots)


def loaded_dice_experiment() -> np.ndarray:
    """Crée l'état d'un dé quantique truqué avec rotations et CNOT."""
    engine = QuantumEngine()
    engine.create_circuit(3)
    engine.apply_ry(0, 63.89611886)
    engine.apply_ry(1, 71.16505652)
    engine.apply_cnot(0, 1)
    engine.apply_ry(1, -18.83494348)
    engine.apply_cnot(0, 1)
    engine.apply_ry(2, 77.66431216)
    engine.apply_cnot(1, 2)
    engine.apply_ry(2, -12.33568784)
    engine.apply_cnot(0, 2)
    engine.apply_ry(2, -12.33568784)
    engine.apply_cnot(1, 2)
    engine.apply_ry(2, -12.33568784)
    engine.apply_cnot(0, 2)
    return engine.get_state()


def bell_experiment(shots: int = 1000) -> Dict[str, int]:
    """Crée l'état de Bell (|00> + |11>) / sqrt(2)."""
    engine = QuantumEngine()
    engine.create_circuit(2)
    engine.apply_h(0)
    engine.apply_cnot(0, 1)
    return engine.bell_counts(shots)

