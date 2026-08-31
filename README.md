# Quantum CLI

Quantum CLI est un simulateur quantique pédagogique basé sur Qiskit et Aer. Le but est d'illustrer les concepts fondamentaux sans masquer la mécanique derrière une abstraction complexe.

## 1. Qu'est-ce qu'un qubit ?

Un qubit est l'unité de base du calcul quantique. Contrairement à un bit classique, il peut se trouver dans une superposition de l'état |0> et |1>.

## 2. Représentation d'un état quantique

Pour n qubits, il existe 2^n états de base. Un système quantique est représenté par des amplitudes complexes, une par état de base.

Exemple sur 2 qubits :

|00>, |01>, |10>, |11>

Le système initial est toujours |00...0> avec une amplitude égale à 1.

## 3. Probabilité et amplitude

La probabilité d'un état est calculée par :

probabilité = |amplitude|²

Ainsi, un amplitude de 1/sqrt(2) donne une probabilité de 50%.

## 4. Porte Hadamard

La porte H crée une superposition :

H|0> = (|0> + |1>) / sqrt(2)

Cela est la base de la pièce quantique.

## 5. Porte X

La porte X est le NON quantique :

X|0> = |1>
X|1> = |0>

## 6. Porte Z

La porte Z change la phase de |1> :

Z|0> = |0>
Z|1> = -|1>

## 7. CNOT

La porte CNOT utilise un qubit de contrôle : si le contrôle est 1, la cible est inversée.

## 8. Mesure

La mesure quantique transforme les amplitudes en probabilités. L'état du système s'effondre sur le résultat observé.

## 9. Dé quantique

Un dé à 6 faces utilise 3 qubits, car 2^3 = 8 états. Les états 110 et 111 sont rejetés pour obtenir la distribution uniforme sur les 6 faces.

## 10. Dé biaisé

Pour un dé biaisé, on prépare un état quantique avec des amplitudes dont les carrés donnent les probabilités voulues.

## 11. Intrication de Bell

La porte H puis CNOT entre deux qubits produit :

(|00> + |11>) / sqrt(2)

## 12. Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 13. Lancement

```bash
python -m quantum_cli
```

ou :

```bash
quantum-cli
```

## 14. Commandes principales

- qubits N
- reset
- h Q
- x Q
- z Q
- cnot CONTROL TARGET
- state
- probabilities
- measure [N]
- coin [N]
- dice [N]
- biased-dice FACECOUNT PROBABILITY
- bell [N]
- explain NAME
- tutorial
- quit / exit

## 15. Limitations

Ce projet est un outil pédagogique et n'est pas un simulateur quantique industriel. Il utilise Qiskit et Aer pour fournir une démonstration claire des principes.

## 16. Packaging

Consultez le fichier BUILD.md pour les instructions détaillées de compilation Linux et Windows.
