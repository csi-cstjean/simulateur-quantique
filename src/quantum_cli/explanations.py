"""Textes pédagogiques pour exécuter des explications sur les portes et commandes."""

EXPLAINS = {
    "x": """Porte Pauli X

La porte Pauli X est une rotation de 180° autour de l'axe X de la sphère de Bloch.

Comportement :
X|0> = |1>
X|1> = |0>

C'est l'équivalent quantique d'une porte NON. Elle inverse le qubit.

Exemple :
> qubits 1
> x 0
> state

Résultat : amplitude = 1 pour |1>""",

    "y": """Porte Pauli Y

La porte Pauli Y est une rotation de 180° autour de l'axe Y de la sphère de Bloch.

Matrice :
Y = [[0, -i], [i, 0]]

Comportement :
Y|0> = i|1>
Y|1> = -i|0>

Elle inverse le qubit ET introduit une phase complexe (i ou -i).

Exemple :
> qubits 1
> y 0
> state

Résultat : amplitude = i pour |1> (100% de probabilité pour |1>)
L'amplitude est imaginaire pure mais la probabilité reste 100%.

Remarque : Y peut être écrite comme Y = iRX(180°), ce qui explique les phases complexes.""",

    "z": """Porte Pauli Z

La porte Pauli Z est une rotation de 180° autour de l'axe Z de la sphère de Bloch.

Comportement :
Z|0> = |0>
Z|1> = -|1>

Elle ne change pas les probabilités d'un état de base mais introduit une phase.

Exemple sur un état de base :
> qubits 1
> z 0
> state

Résultat : amplitude = 1 pour |0> (inchangé)

Mais avec une superposition (après H) :
> reset
> qubits 1
> h 0
> z 0
> state

Les probabilités restent 50/50 mais les amplitudes deviennent complexes.

Relation avec la phase : Z modifie la phase relative entre |0> et |1>.""",

    "h": """Porte Hadamard

La porte Hadamard est une porte quantique fondamentale qui crée des superpositions.

Transformations :
H|0> = |+> = (|0> + |1>) / sqrt(2)
H|1> = |-> = (|0> - |1>) / sqrt(2)

Résultat : les états de base deviennent des superpositions à 50/50.

Propriété clé : H est son propre inverse : H² = I (l'identité).

Peut être vue comme une rotation de 180° autour d'un axe diagonal de la sphère de Bloch.

Exemple :
> qubits 1
> h 0
> state

Résultat : 50% de |0>, 50% de |1>

Remarque : bien que RY(90°) donne le même résultat que H sur |0>, ce ne sont pas
des opérations identiques pour un état arbitraire.""",

    "cnot": """Porte CNOT (Controlled-NOT)

La porte CNOT est une porte à deux qubits qui crée l'intrication.

Comportement :
- Le qubit de contrôle reste inchangé
- Le qubit cible est inversé uniquement si le contrôle vaut 1

Table de vérité :
|00> → |00>
|01> → |01>
|10> → |11>
|11> → |10>

Application pédagogique clé : créer un état de Bell (intrication maximale)

Exemple :
> qubits 2
> h 0
> cnot 0 1
> state

Résultat : (|00> + |11>) / sqrt(2)
Les deux qubits sont maintenant intriqués : mesurer l'un définit l'autre.""",


    "measure": """Mesure

La mesure transforme les amplitudes en probabilités.

La probabilité d'un résultat est |amplitude|².
Après la mesure, le système s'effondre dans l'état mesuré.""",

    "coin": """Pile ou Face Quantique

Cette expérience utilise un qubit en superposition pour simuler un tirage aléatoire.

Étapes :
1. Créer un qubit (état |0>)
2. Appliquer une porte Hadamard pour créer la superposition
3. Mesurer 1000 fois

Résultat : environ 50% de |0> (FACE) et 50% de |1> (PILE)""",

    "dice": """Dé Quantique

Cette expérience simule un dé à 6 faces en utilisant 3 qubits en superposition.

Étapes :
1. Créer 3 qubits (état |000>)
2. Appliquer des portes Hadamard sur chaque qubit pour créer la superposition
3. Mesurer 1000 fois

Les 3 qubits en superposition donnent 8 états possibles (2³ = 8).
Les états correspondent aux faces 0 à 7, le 7 est ignoré pour un vrai dé (1-6).""",

    "loaded-dice": """Dé Quantique Truqué

Syntaxe : loaded-dice

Cette expérience construit un état à trois qubits avec des rotations RY et des
portes CNOT. Elle ne mesure pas le circuit : elle affiche son état final.

La séquence donne environ 51% de probabilité pour |000> et 7% pour chacun des
sept autres états. Le résultat est donc volontairement biaisé vers |000>.

Les portes RY règlent les amplitudes, tandis que les CNOT créent des corrélations
entre les qubits. C'est un exemple de préparation d'une distribution quantique
non uniforme.""",

    "bell": """État de Bell (Intrication)

L'état de Bell est une superposition de deux qubits intriqués.

Syntaxe : bell [N]

Étapes :
1. Créer 2 qubits (état |00>)
2. Appliquer une porte Hadamard sur le premier
3. Appliquer une porte CNOT pour créer l'intrication

Résultat : seulement |00> et |11> sont observables (probabilité 50% chacun)

Propriété clé : les deux qubits sont corrélés. Si le premier est |0>, le second
est aussi |0>. Si le premier est |1>, le second est aussi |1>.""",

    "qubits": """Créer un Circuit Quantique

Syntaxe : qubits N

Crée un circuit avec N qubits initialisés à |0>.

Exemple : qubits 2
Crée 2 qubits dans l'état |00>""",

    "reset": """Réinitialiser le Circuit

Efface le circuit quantique actuel et réinitialise l'état à vierge.

Vous devez créer un nouveau circuit avec 'qubits N' avant de continuer.""",

    "state": """Afficher l'État Quantique

Affiche l'état quantique complet du circuit avec les amplitudes et probabilités.

Chaque ligne représente un état de base possible.
L'amplitude est un nombre complexe.
La probabilité est |amplitude|².""",

    "probabilities": """Afficher les Probabilités

Affiche uniquement les probabilités d'observer chaque état quantique.

Les états avec probabilité proche de 0 ne sont pas affichés.""",

    "rx": """Porte RX (Rotation autour de l'axe X)

RX(θ) effectue une rotation de θ degrés autour de l'axe X de la sphère de Bloch.

Syntaxe : rx <qubit> <angle_degres>
Exemple : rx 0 90

L'angle est exprimé en degrés. Les angles peuvent être négatifs et supérieurs à 360°.

Propriétés :
- RX(0°) = identité (aucun changement)
- RX(180°) ≈ X (équivalent à la porte de Pauli X, à une phase près)
- RX(360°) = identité

Relation avec la porte Pauli X :
Les portes de Pauli peuvent être vues comme des cas particuliers des rotations :
RX(180°) ≈ X

Comportement : RX modifie les amplitudes et peut introduire des composantes complexes.

Expérience progressive :
> qubits 1
> rx 0 45
> state
(Les probabilités commencent à changer)

> rx 0 45
> state
(Continuez jusqu'à)

> rx 0 90
> state
(Vous devriez atteindre 50/50)""",

    "ry": """Porte RY (Rotation autour de l'axe Y)

RY(θ) effectue une rotation de θ degrés autour de l'axe Y de la sphère de Bloch.

Syntaxe : ry <qubit> <angle_degres>
Exemple : ry 0 60

C'est la porte la plus pédagogique pour montrer comment modifier les probabilités !

Propriétés :
- RY(0°) = identité (aucun changement)
- RY(180°) ≈ Y (équivalent à la porte de Pauli Y, à une phase près)
- RY(90°) appliquée à |0> donne les mêmes probabilités que H : 50/50

Relation avec la porte Pauli Y :
RY(180°) ≈ Y

Formule sur l'état |0> :
RY(θ)|0> = cos(θ/2)|0> + sin(θ/2)|1>

Exemples de probabilités :
- RY(0°) → 100% de |0>, 0% de |1>
- RY(60°) → cos²(30°) ≈ 75% de |0>, sin²(30°) ≈ 25% de |1>
- RY(90°) → 50% de |0>, 50% de |1>
- RY(180°) → 0% de |0>, 100% de |1>

Expérience pédagogique :
> qubits 1
> ry 0 60
> state

Vous devriez voir environ 75% et 25% de probabilités.""",

    "rz": """Porte RZ (Rotation autour de l'axe Z)

RZ(θ) effectue une rotation de θ degrés autour de l'axe Z de la sphère de Bloch.

Syntaxe : rz <qubit> <angle_degres>
Exemple : rz 0 90

RZ est fondamentalement différente de RX et RY : elle agit sur la phase relative
plutôt que de modifier les probabilités directement.

Propriétés :
- RZ(0°) = identité (aucun changement)
- RZ(180°) ≈ Z (équivalent à la porte de Pauli Z, à une phase près)
- RZ(360°) = identité (tour complet)

Relation avec la porte Pauli Z :
RZ(180°) ≈ Z

Point clé : Sur un état de base (|0> ou |1>), RZ ne change pas les probabilités.
Mais sur une superposition, elle modifie les phases complexes.

Démonstration 1 - RZ ne change pas les probabilités de base :
> qubits 1
> rz 0 90
> state
(L'amplitude de |0> reste 1, avec une phase)

Démonstration 2 - RZ change la phase sur une superposition :
> qubits 1
> h 0
> rz 0 90
> state
(Les amplitudes deviennent complexes ! Mais les probabilités restent 50/50)

Démonstration 3 - La phase devient observable par interférence :
> reset
> qubits 1
> h 0
> rz 0 180
> h 0
> state
(Le résultat est |1> avec une probabilité de 100%.)

Leçon pédagogique :
La phase quantique est un concept fondamental. Elle n'est pas observable
directement dans les probabilités, mais elle peut devenir visible par interférence
après d'autres opérations. C'est la base du calcul quantique avancé.""",
}


def explain(name: str) -> str:
    """Retourne une explication pédagogique pour une porte ou une commande."""
    key = name.lower()
    return EXPLAINS.get(key, f"Aucune explication disponible pour '{name}'.")
