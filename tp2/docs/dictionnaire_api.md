# Dictionnaire de données — Source 1 : API football-data.org

## Endpoint utilisé
`GET https://api.football-data.org/v4/matches?dateFrom=YYYY-MM-DD&dateTo=YYYY-MM-DD`
- Authentification : header `X-Auth-Token`
- Contrainte du plan gratuit : la période entre dateFrom et dateTo ne peut pas dépasser 10 jours

## Champs retenus

| Champ JSON | Description | Type | Exemple | Remarque |
|---|---|---|---|---|
| id | Identifiant unique du match côté API | Entier | 555017 | Sert de clé naturelle pour éviter les doublons |
| utcDate | Date et heure UTC du match | Date/heure (ISO 8601) | 2026-09-20T00:00:00Z | À convertir en DATE pour rejoindre le modèle TP1 |
| status | État du match | Texte (énumération) | FINISHED | Valeurs possibles : SCHEDULED, TIMED, IN_PLAY, PAUSED, FINISHED, POSTPONED, CANCELLED |
| homeTeam.name | Nom de l'équipe à domicile | Texte | São Paulo FC | |
| awayTeam.name | Nom de l'équipe à l'extérieur | Texte | SC Internacional | |
| score.fullTime.home | Score final domicile | Entier ou NULL | 1 | NULL si le match n'est pas terminé |
| score.fullTime.away | Score final extérieur | Entier ou NULL | 0 | NULL si le match n'est pas terminé |
| competition.name | Nom de la compétition | Texte | Campeonato Brasileiro Série A | Correspond à `tournoi.nom` |
| area.name | Pays/zone de la compétition | Texte | Brazil | Correspond approximativement à `match.pays` |
| venue | Lieu du match | Texte ou absent | — | **Jamais renseigné sur le plan gratuit** (0/37 matchs testés) → traité comme NULL |

## Observations d'audit

- Sur un échantillon de 37 matchs (20–29 sept. 2026), un seul statut observé : `FINISHED`.
  Les autres statuts existent dans la documentation officielle mais n'ont pas été
  rencontrés sur cette fenêtre ; le pipeline doit les gérer même sans exemple observé.
- Le champ `venue` n'est jamais renseigné sur le plan gratuit : `ville` sera NULL
  pour toutes les données issues de l'API, contrairement à la source TP1 où elle
  est toujours renseignée.
- `score.fullTime` peut être NULL pour les matchs non terminés (SCHEDULED, TIMED...).

## Lien avec la source 2 (CSV TP1)

Le rapprochement entre un match API et l'historique CSV se fait par nom d'équipe
(`homeTeam.name` / `awayTeam.name` ↔ `equipe.nom`). Un contrôle de cohérence des noms
sera nécessaire à l'agrégation, car l'API et les CSV n'utilisent pas forcément
exactement les mêmes libellés (ex. "São Paulo FC" vs un nom simplifié).