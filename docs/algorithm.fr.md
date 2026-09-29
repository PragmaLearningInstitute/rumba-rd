# Comprendre le moteur de mise en forme RUMBA.RD

Cette explication suit `desktop/Function.py` et son port navigateur `web/rumbaEngine.js`. RUMBA.RD transforme la présentation d'un texte sans produire un nouveau texte avec une IA générative. La [présentation sur le site PLI](https://pragmalearninginstitute.com/rumba-rd) fournit le contexte du projet ; le code présent est la référence pour les paramètres.

## 1. Analyser le texte d'entrée

Le moteur détecte approximativement le français ou l'anglais à partir de marqueurs lexicaux. Il compte les mots et estime les syllabes par groupes de voyelles. Ce sont des heuristiques : mots composés, abréviations, noms propres, nombres et langues mélangées peuvent dégrader l'estimation.

Le score de Flesch dépend de la longueur moyenne des phrases et du nombre estimé de syllabes par mot, avec des coefficients selon la langue retenue. Ce score est une description simplifiée de l'entrée. La mise en gras ne modifie ni les mots ni les phrases et ne permet pas de prétendre que le texte est devenu linguistiquement plus facile.

L'attribut historique `zipf_common_ratio` est la part de mots reconnus dans le dictionnaire `common_words`. Il ne repose pas sur un corpus fréquentiel chiffré, ne donne pas une fréquence Zipf et ne doit pas être rapporté comme tel dans une étude.

## 2. Segmenter et construire des blocs

Le découpage conserve mots, espaces, ponctuation, chiffres et autres caractères. Les mots sont ensuite divisés en unités approximatives pour construire les blocs de sélection. Ce découpage n'est pas un syllabificateur linguistique validé.

La taille initiale du bloc est 6 pour un score Flesch inférieur à 74, 8 au-dessus de 82 et 7 entre ces valeurs. Une marche aléatoire bornée fait varier la taille entre 4 et 11 avec un paramètre de dispersion de 1,3. Les seuils sont des choix du logiciel, pas des normes de lisibilité.

## 3. Choisir les repères typographiques

Une pondération gaussienne asymétrique favorise certaines positions dans le bloc : dispersion 2,4 d'un côté et 3,7 de l'autre. Le seuil de sélection dépend de la longueur du bloc, avec une valeur de base de 0,14 et un plafond à 0,98. Une cadence 3/2 intervient suivant la taille du bloc. Pour reproduire exactement la sélection, utiliser la fonction complète et conserver la graine aléatoire.

Le rendu marque les unités retenues avec `<strong>` en HTML et `**` en Markdown. Le texte incorporé dans le HTML est échappé ; une balise collée par un utilisateur reste du texte. Les feuilles de style et polices déterminent ensuite l'apparence effective du gras.

## 4. Reproduire un résultat

Conserver le texte original, la graine, le commit, l'implémentation choisie, la police, la taille, l'interligne et la largeur de la zone de lecture. Deux graines peuvent changer les repères sans changer les métriques initiales. Python et JavaScript utilisent des générateurs différents : la même valeur numérique de graine ne suffit pas à aligner leurs sorties.

## Interpréter et évaluer

La conservation des mots se teste automatiquement ; l'utilité pour la lecture exige des observations distinctes. Mesurer séparément durée, compréhension, confort déclaré et qualité des données. Éviter d'attribuer un gain à l'emphase si les conditions diffèrent aussi par texte, police, contraste ou ordre. Le [guide d'évaluation](evaluation.fr.md) détaille ces précautions et la relation avec le toolkit oculométrique.
