# Chargement PostgreSQL

## Script
`postgres/load_to_postgres.py`

## Logique
- Lecture de `datalake/clean/matches_clean.csv`
- Résolution des clés étrangères : recherche ou création d'une ligne
  `equipe`/`tournoi` pour chaque nom rencontré (cache en mémoire pour éviter
  les lookups répétés)
- Insertion dans `match` avec gestion de l'idempotence via
  `ON CONFLICT (date_match, id_equipe_domicile, id_equipe_exterieur, source) DO NOTHING`

## Évolutions du schéma TP1 nécessaires pour TP2
- Colonnes ajoutées à `match` : `source`, `id_externe`, `statut`
  (voir `postgres/02_alter_for_tp2.sql`)
- `ville` rendue nullable : la source API ne fournit jamais le lieu du match,
  contrairement aux données historiques CSV où elle est toujours renseignée
- Contrainte `UNIQUE (date_match, id_equipe_domicile, id_equipe_exterieur, source)`
  ajoutée pour permettre le rechargement du pipeline sans dupliquer les données

## Résultat du chargement

| Source | Lignes chargées |
|---|---|
| csv_historique | 49 546 |
| api_live | 97 |
| **Total** | **49 643** |

## Vérification de la déduplication

Le fichier `results.csv` du TP1 contenait un doublon identifié lors de l'audit
(1 ligne avec la même date + mêmes équipes). La contrainte `UNIQUE` a
automatiquement rejeté ce doublon lors du chargement : 49 547 lignes lues
côté CSV, 49 546 réellement insérées. Ce comportement confirme que la
contrainte fonctionne comme prévu.

## Vérification des relations (JOIN)

```sql
SELECT m.date_match, e1.nom AS domicile, e2.nom AS exterieur,
       m.score_domicile, m.score_exterieur, t.nom AS tournoi, m.source
FROM match m
JOIN equipe e1 ON m.id_equipe_domicile = e1.id_equipe
JOIN equipe e2 ON m.id_equipe_exterieur = e2.id_equipe
JOIN tournoi t ON m.id_tournoi = t.id_tournoi
WHERE m.source = 'api_live'
ORDER BY m.date_match DESC
LIMIT 5;
```

Résultat : les noms d'équipes et de tournois sont correctement résolus,
confirmant que les clés étrangères fonctionnent.