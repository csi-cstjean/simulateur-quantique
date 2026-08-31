import numpy as np

from quantum_cli.experiments import (
    bell_experiment,
    coin_experiment,
    dice_experiment,
    loaded_dice_experiment,
)


def test_coin_experiment_is_balanced():
    counts = coin_experiment(shots=2000)
    assert abs(counts["0"] - counts["1"]) < 500


def test_dice_experiment_is_uniform():
    counts = dice_experiment(shots=3000)
    assert len(counts) == 6
    for face in counts:
        assert abs(counts[face] - 500) < 600


def test_loaded_dice_experiment_is_biased_toward_zero():
    state = loaded_dice_experiment()
    probabilities = np.abs(state) ** 2
    assert np.isclose(probabilities.sum(), 1.0)
    assert np.isclose(probabilities[0], 0.51, atol=1e-8)
    assert np.allclose(probabilities[1:], 0.07, atol=1e-8)


def test_bell_experiment_is_entangled():
    counts = bell_experiment(shots=2000)
    assert counts.get("00", 0) + counts.get("11", 0) > 1500
    assert counts.get("01", 0) + counts.get("10", 0) < 500
