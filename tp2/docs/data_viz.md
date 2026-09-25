# Data Visualization — Metabase

## Choix technique
Metabase, connecté directement à PostgreSQL (`football_international`),
conteneurisé via Docker (`dataviz/docker-compose.dataviz.yml`).

## Connexion
- Hôte : `host.docker.internal` (le conteneur Metabase accède à PostgreSQL
  installé nativement sur la machine hôte)
- Port : 5432
- Base : football_international

## Dashboard : "Football - Vue d'ensemble"

| Carte | Requête | Visualisation |
|---|---|---|
| Répartition des matchs par source | Compte les matchs par origine (API vs historique CSV) | Camembert/Barres |
| Top 10 des tournois | Classement des compétitions par nombre de matchs | Barres |
| Matchs récents (API) | Détail des derniers matchs collectés en direct | Table |
| Top 15 des équipes | Équipes ayant joué le plus de matchs dans l'historique | Barres |

Capture d'écran : `dashboard_metabase.png`