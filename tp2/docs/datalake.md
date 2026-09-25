# Data Lake

## Choix technique

Le Data Lake est implémenté comme une arborescence de fichiers locale (pas de
solution cloud type S3/MinIO), un choix adapté à un projet étudiant exécuté
en local via Docker Compose. La structure respecte l'organisation demandée :
séparation claire entre données brutes (`raw/`) et données agrégées.

## Arborescence
datalake/
├── raw/
│ ├── api/
│ │ └── match_<id>.json ← un fichier par match, écrit par
│ │ aggregator/kafka_to_datalake.py
│ └── source2/
│ └── <timestamp>/
│ ├── results.csv ← copie horodatée des CSV TP1,
│ ├── goalscorers.csv écrite par source2/reader.py
│ ├── shootouts.csv
│ └── former_names.csv
└── aggregated/
└── matches_aggregated_<timestamp>.csv ← sortie de aggregator/aggregate.py


## Traçabilité

- **Source 1 (API)** : chaque match est identifié par son `id` externe
  (`match_<id>.json`). Un même match reçu plusieurs fois via Kafka écrase le
  fichier existant : la déduplication est donc naturelle au niveau du Data Lake.
  Constaté en pratique : 776 messages consommés depuis Kafka, mais seulement
  97 fichiers distincts, correspondant aux 97 matchs réellement uniques.
- **Source 2 (CSV)** : chaque exécution du lecteur crée un dossier horodaté,
  ce qui conserve un historique des copies même si le contenu source ne change pas.
- **Agrégation** : chaque exécution produit un nouveau fichier horodaté,
  sans écraser les précédents, pour garder une trace de chaque run du pipeline.

## Volumétrie observée

| Zone | Contenu | Volume |
|---|---|---|
| raw/api/ | Matchs uniques issus de l'API | 97 fichiers JSON |
| raw/source2/<timestamp>/ | Copie des CSV TP1 | 49 547 + 47 914 + 683 + 36 lignes |
| aggregated/ | Fusion source 1 + source 2 | 49 644 lignes |

## Lien avec le monitoring (Prometheus/Grafana)

Cette volumétrie (raw vs aggregated vs, plus tard, PostgreSQL) sera exposée
comme métrique pour l'indicateur **Raw vs Clean** demandé à l'étape 5 du TP.