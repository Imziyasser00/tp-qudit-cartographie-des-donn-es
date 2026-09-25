# Architecture — Pipeline Data temps réel (Football)

```mermaid
flowchart TD
    subgraph SRC["Sources"]
        API["API football-data.org<br/>(matchs live / récents)"]
        S2["Source 2 : CSV TP1<br/>(results, goalscorers, shootouts, former_names)"]
    end

    subgraph ING["Ingestion"]
        PROD["Producer Python<br/>(interroge l'API en boucle)"]
        KAFKA["Kafka<br/>topic: matches_live"]
        S2READER["Lecteur Source 2<br/>(batch CSV)"]
    end

    subgraph AGG["Agrégation"]
        AGGSVC["Service d'agrégation<br/>(jointure équipe + historique)"]
    end

    subgraph STORE["Data Lake"]
        RAWAPI["raw/api/"]
        RAWS2["raw/source2/"]
        AGGZONE["aggregated/"]
    end

    subgraph PROC["Traitement"]
        SPARK["PySpark<br/>(types, doublons, nulls, normalisation)"]
    end

    subgraph DB["Stockage propre"]
        PG[("PostgreSQL<br/>football_international")]
    end

    subgraph VIZ["Exploitation"]
        DASH["Data Viz<br/>(Metabase / Grafana)"]
    end

    subgraph MON["Monitoring"]
        PROM["Prometheus"]
        GRAF["Grafana"]
    end

    API --> PROD --> KAFKA
    S2 --> S2READER
    KAFKA --> AGGSVC
    S2READER --> AGGSVC
    KAFKA -.copie brute.-> RAWAPI
    S2READER -.copie brute.-> RAWS2
    AGGSVC --> AGGZONE
    RAWAPI --> SPARK
    RAWS2 --> SPARK
    AGGZONE --> SPARK
    SPARK --> PG
    PG --> DASH

    KAFKA -.métriques.-> PROM
    PG -.métriques.-> PROM
    SPARK -.métriques.-> PROM
    PROM --> GRAF
```

## Services Docker prévus

| Service | Rôle | Image de base |
|---|---|---|
| `zookeeper` | Coordination Kafka | `confluentinc/cp-zookeeper` |
| `kafka` | Broker de messages | `confluentinc/cp-kafka` |
| `producer-api` | Interroge football-data.org, publie sur Kafka | Python custom |
| `source2-reader` | Lit les CSV TP1, les copie dans le Data Lake | Python custom |
| `aggregator` | Consomme Kafka + Source 2, agrège | Python custom |
| `spark` | Traitement PySpark (raw → clean) | `bitnami/spark` |
| `postgres` | Base de données finale | `postgres:16` |
| `dataviz` | Tableau de bord | `metabase/metabase` |
| `prometheus` | Collecte des métriques | `prom/prometheus` |
| `grafana` | Visualisation du monitoring | `grafana/grafana` |

## Volumes de persistance

| Volume | Contenu |
|---|---|
| `datalake_data` | `raw/api/`, `raw/source2/`, `aggregated/` |
| `postgres_data` | Données PostgreSQL |
| `prometheus_data` | Historique des métriques |
| `grafana_data` | Dashboards Grafana |