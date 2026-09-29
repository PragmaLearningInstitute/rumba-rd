# Évaluer une mise en forme de lecture de manière reproductible

Une sortie visuellement convaincante ne suffit pas à établir un effet sur la lecture. RUMBA.RD expose sa transformation pour permettre une comparaison documentée. Le [toolkit de lecture et d'oculométrie](https://github.com/PragmaLearningInstitute/reading-eye-tracking-toolkit) peut aider à organiser une collecte exploratoire ; il n'est pas un instrument clinique validé.

## Préparer une comparaison

Formuler d'abord la question : temps de lecture, compréhension ou confort ? Choisir une mesure principale avant d'observer les résultats. Préparer des textes de difficulté comparable, fixer les polices, contrastes, tailles, interlignes, géométries d'affichage et consignes. Conserver le texte exact et son empreinte, la version de RUMBA.RD et la graine utilisée.

Contrebalancer l'ordre lorsque le protocole le permet. Le même participant peut progresser par familiarisation ou se fatiguer. Deux textes différents introduisent un effet du texte ; le même texte répété introduit un effet de mémoire. Aucun de ces effets ne disparaît simplement parce qu'une condition porte le nom `plain` ou `formatted`.

## Vérifier avant de collecter

Faire un essai sans participant et vérifier la conservation du texte, les caractères spéciaux, les exports et les journaux. Vérifier ensuite l'écran réellement présenté. Une police de secours ou une fenêtre redimensionnée modifie les lignes et peut modifier le résultat comportemental.

Le toolkit rend les balises `<strong>` en gras ou demi-gras selon la police disponible. Il faut conserver `font_report.txt` et les fichiers de géométrie. Ses textes d'exemple illustrent un format de fichier ; ils ne constituent pas à eux seuls un matériel expérimental validé.

## Lire les résultats

Analyser la compréhension séparément de la vitesse. Une lecture plus rapide avec davantage d'erreurs n'est pas un bénéfice univoque. Présenter le nombre de participants, les exclusions, les données manquantes et les conditions de passation. Les angles de regard estimés par webcam et les métriques dérivées restent sensibles à l'éclairage, aux lunettes, à la pose de tête et à la calibration.

Le fichier `metrics.csv` du toolkit résume un enregistrement OpenFace entier, qui peut contenir calibration, pauses et questionnaires. Il ne constitue pas automatiquement une comparaison A/B des périodes de lecture. Une analyse par condition exige une segmentation explicite à partir des marqueurs, une gestion des données manquantes et une méthode statistique adaptée.

## Partager un résultat réutilisable

Partager d'abord le protocole, les paramètres, le code d'analyse et des exemples synthétiques. Les réponses, voix et caractéristiques faciales d'un participant ne doivent pas être ajoutées au dépôt public. Le [site de Pragma Learning Institute](https://pragmalearninginstitute.com/outils/documentation) relie la documentation des outils ; les dépôts donnent accès aux implémentations et à leurs limites.
