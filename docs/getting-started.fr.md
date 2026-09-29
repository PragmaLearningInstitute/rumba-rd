# Utiliser RUMBA.RD : installation, mise en forme et export

RUMBA.RD applique des repères typographiques à un texte fourni par l'utilisateur. Son intérêt est de rendre la transformation visible et son calcul inspectable. Pour un essai sans installation, ouvrir [RUMBA.RD sur le site de Pragma Learning Institute](https://pragmalearninginstitute.com/rumba-rd).

## Première utilisation

Depuis la racine du dépôt, lancer `python3 -m http.server 8080 --bind 127.0.0.1 --directory web`, puis ouvrir `http://127.0.0.1:8080/rumba-rd-light.html`. Coller quelques phrases, appliquer la mise en forme, puis comparer avec l'original. Le contenu lexical doit rester identique : seuls les repères visuels changent.

Vérifier les nombres, les accents, les symboles et les retours de ligne sur votre document. Cette édition corrige une perte de chiffres et de caractères Unicode présente dans l'ancien découpage. Le HTML utilisateur est échappé avant d'être inséré dans la sortie.

Choisir une police réellement installée. Une substitution de police peut modifier les lignes, la largeur des mots et la pagination. Commencer par l'export HTML et contrôler le résultat avant d'envoyer un PDF ou un document Word.

## Exécuter l'application Python

Créer un environnement virtuel à la racine, l'activer et installer `desktop/requirements.txt`, comme dans le [README](../README.md). Tk est fourni par certaines distributions Python ; vérifier son fonctionnement avec `python -m tkinter` avant de lancer `python desktop/app.py`.

L'interface permet de coller un texte, de choisir la famille et la taille de police, de changer le thème et d'exporter. L'interligne est fixé à 1,5 dans le rendu de bureau. Les scripts `desktop/scripts/` proposent aussi des commandes de lancement et de construction avec PyInstaller. Une construction reste dépendante du système cible ; ce dépôt ne contient pas de binaire signé.

## Appeler le moteur dans un script

Depuis le dossier `desktop/` :

```python
from Function import gaussReformulator
from formatter import OutputStyle, render_html_document
from pathlib import Path

text = "En 2026, Léa lit 12 lignes et compare deux mises en forme."
result = gaussReformulator(text, seed=42)
assert result.plain_text == text
Path("demo.html").write_text(
    render_html_document(result, OutputStyle(font_family="Arial", font_size=13)),
    encoding="utf-8",
)
print(result.analysis.flesch_score)
```

Le résultat contient `plain_text`, `markdown_text`, `html_text` et `analysis`. Le texte brut est la référence pour vérifier la conservation du contenu. Le score Flesch est calculé sur ce texte d'entrée ; il ne mesure pas un bénéfice causé par la mise en gras.

## Intégrer la version Wix

Le dossier [Wix Velo](../desktop/wix_velo/README.md) contient les modules publics, une fonction backend et un exemple de code de page. Reproduire les identifiants des composants attendus par `page_code/readerPage.js`. Tester le traitement sur un site de développement et déterminer si les textes doivent être envoyés au backend : le traitement dans un navigateur autonome et un appel backend n'ont pas la même frontière de données.

## Exports et confidentialité

Le traitement principal ne demande aucune clé d'API d'IA. Dans le navigateur, certaines bibliothèques d'export sont téléchargées à la demande depuis un CDN. Dans l'application Python, PDF et DOCX utilisent les paquets installés localement. Les fichiers exportés contiennent votre texte : choisir leur dossier et leur diffusion en conséquence.

La télémétrie web est désactivée par défaut. Une activation exige une configuration explicite et une information adaptée aux utilisateurs. Le dépôt ne contient ni texte personnel d'apprenant ni export de production.

## Dépannage

| Problème | Action |
| --- | --- |
| Modules JavaScript bloqués | Servir le dossier par HTTP ; éviter `file://` |
| Fenêtre Python absente | Tester Tk et vérifier l'environnement virtuel actif |
| Police différente | Installer légalement la police choisie ou utiliser une police système commune |
| Export PDF/DOCX web indisponible | Vérifier les bibliothèques CDN ou utiliser HTML |
| Résultats Python et JavaScript différents | Conserver la même implémentation, version et graine pour une comparaison |
| Formattage sans bénéfice apparent | Examiner l'usage avec le lecteur ; aucune amélioration individuelle n'est garantie |
