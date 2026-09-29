# Validation de l'édition publique

Vérifications effectuées le 28 septembre 2026 sur la copie de publication. Les sources de production n'ont pas été modifiées.

## Vérifié

- Parcours navigateur vérifié avec chiffres, accents, Unicode et balises collées : résultat affiché et texte préservé.
- Trois tests Python : vocabulaire, présence des métriques et du balisage, conservation de chiffres/caractères Unicode et échappement HTML.
- Un test JavaScript : texte conservé, balises utilisateur échappées.
- Syntaxe Python et JavaScript, validité des fichiers JSON, liens internes des guides.
- Installation temporaire des dépendances Python nécessaires au développement, sans modifier l'installation de production.
- Recherche de motifs de secrets et exclusion des environnements, données privées et polices non vérifiées.

## Limites

L'audit de sécurité est partiel. Les tests ne constituent pas une validation d'efficacité de lecture. L'application Tk, l'intégration Wix, les exports PDF/DOCX dans chaque navigateur et les binaires macOS/Windows nécessitent une validation sur leurs environnements cibles. Les ports Python et JavaScript n'ont pas une sortie aléatoire identique.
