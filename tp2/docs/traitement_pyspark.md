# Traitement PySpark

## Script
`spark/transform.py`

## Étapes de traitement appliquées

1. **Lecture** : dernier fichier agrégé (`datalake/aggregated/matches_aggregated_*.csv`)
2. **Typage** : conversion des scores en entier, de la date en type Date
3. **Normalisation** : suppression des espaces superflus dans les noms
   d'équipes, compétitions, pays et villes
4. **Valeurs manquantes** : suppression des lignes avec un match marqué
   FINISHED mais sans score renseigné
5. **Doublons** :
   - suppression des doublons stricts (toutes colonnes identiques)
   - déduplication des matchs API par `id_externe` (un match ne doit
     apparaître qu'une fois, même si Kafka a livré plusieurs messages
     pour le même match)
6. **Écriture** : résultat converti en pandas et sauvegardé dans
   `datalake/clean/matches_clean.csv`

## Résultat observé (exécution du 25/09/2026)

| Étape | Lignes |
|---|---|
| Lecture brute (agrégée) | 49 644 |
| Après suppression score manquant | 49 644 (0 supprimée) |
| Après suppression doublons stricts | 49 644 (0 supprimée) |
| Après déduplication API par id_externe | 49 644 (0 supprimée) |
| **Résultat final propre** | **49 644** |

## Remarque technique (Windows)

L'écriture native de Spark (`df.write.csv()`) nécessite `winutils.exe` et une
version de Hadoop compatible avec le JAR embarqué dans PySpark. Sur cet
environnement, un conflit de version a été rencontré (`UnsatisfiedLinkError`
sur `NativeIO$Windows`). Le contournement retenu : convertir le résultat final
en pandas (`toPandas()`) puis écrire avec `to_csv()`, ce qui évite complètement
l'écriture native Hadoop tout en gardant toute la logique de transformation
dans PySpark.