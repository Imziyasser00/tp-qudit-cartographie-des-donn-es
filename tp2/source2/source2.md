# Source 2 — Fichiers CSV historiques (TP1)

## Rôle dans le pipeline
Source batch, statique. Contrairement à l'API (source 1, temps réel), cette
source ne change pas au fil du temps : elle sert de socle historique pour
enrichir les matchs récents collectés en continu.

## Mécanisme de récupération
Un script Python (`source2/reader.py`) copie les 4 fichiers CSV du TP1 vers
le Data Lake, sous `raw/source2/<timestamp>/`, à chaque exécution. L'horodatage
permet de tracer quand chaque copie a été faite, même si le contenu source
ne change pas.

## Format et fichiers
| Fichier | Lignes | Description |
|---|---|---|
| results.csv | 49 547 | Résultats de matchs internationaux, 1872 à aujourd'hui |
| goalscorers.csv | 47 914 | Buts marqués par match |
| shootouts.csv | 683 | Séances de tirs au but |
| former_names.csv | 36 | Anciens noms d'équipes |

Détails complets : voir le dictionnaire de données du TP1
(`../docs/02_dictionnaire.md` à la racine du dépôt).

## Nature
Structurée (CSV avec en-têtes).