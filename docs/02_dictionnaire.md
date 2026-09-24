# Dictionnaire de données

Légende des types : **Date**, **Texte**, **Entier**, **Booléen**.
Les types PostgreSQL correspondants sont détaillés dans le modèle logique.

## 1. results.csv : résultats des matchs

| Champ | Description | Type | Exemple |
|---|---|---|---|
| date | Date à laquelle le match a été joué | Date | 1872-11-30 |
| home_team | Nom de l'équipe qui joue à domicile (nom actuel de la sélection) | Texte | Scotland |
| away_team | Nom de l'équipe qui joue à l'extérieur (nom actuel) | Texte | England |
| home_score | Buts de l'équipe domicile à la fin du match, prolongations incluses, tirs au but exclus | Entier | 0 |
| away_score | Buts de l'équipe extérieur, même règle que home_score | Entier | 0 |
| tournament | Nom de la compétition ou type de match | Texte | Friendly |
| city | Ville ou zone administrative où le match a été joué | Texte | Glasgow |
| country | Pays où le match a été joué, avec le nom **de l'époque** | Texte | Scotland |
| neutral | Indique si le match a eu lieu sur terrain neutre (TRUE) ou non (FALSE) | Booléen | FALSE |

## 2. goalscorers.csv : buts marqués

| Champ | Description | Type | Exemple |
|---|---|---|---|
| date | Date du match (sert à retrouver le match) | Date | 1916-07-02 |
| home_team | Équipe domicile du match (sert à retrouver le match) | Texte | Chile |
| away_team | Équipe extérieur du match (sert à retrouver le match) | Texte | Uruguay |
| team | Équipe qui a marqué le but | Texte | Uruguay |
| scorer | Nom du joueur qui a marqué | Texte | José Piendibene |
| minute | Minute du but | Entier | 44 |
| own_goal | Indique si le but est un but contre son camp | Booléen | FALSE |
| penalty | Indique si le but a été marqué sur penalty | Booléen | FALSE |

## 3. shootouts.csv : séances de tirs au but

| Champ | Description | Type | Exemple |
|---|---|---|---|
| date | Date du match (sert à retrouver le match) | Date | 1967-08-22 |
| home_team | Équipe domicile du match | Texte | India |
| away_team | Équipe extérieur du match | Texte | Taiwan |
| winner | Équipe qui a gagné la séance de tirs au but | Texte | Taiwan |
| first_shooter | Équipe qui a tiré en premier (souvent vide pour les anciens matchs) | Texte | (vide) |

## 4. former_names.csv : anciens noms des équipes

| Champ | Description | Type | Exemple |
|---|---|---|---|
| current | Nom actuel de la sélection nationale | Texte | Benin |
| former | Ancien nom porté par cette sélection | Texte | Dahomey |
| start_date | Date de début d'utilisation de l'ancien nom | Date | 1959-11-08 |
| end_date | Date de fin d'utilisation de l'ancien nom | Date | 1975-11-30 |

## Clés naturelles et liens entre fichiers

| Lien | Colonnes de jointure |
|---|---|
| goalscorers → results | date + home_team + away_team |
| shootouts → results | date + home_team + away_team |
| former_names → results | current = home_team / away_team |

## Observations sur la qualité des données

- Aucun fichier ne possède d'identifiant technique de match.
- `first_shooter` est vide pour les anciennes séances de tirs au but : la colonne devra accepter NULL.
- Les colonnes `team` (goalscorers) et `winner` (shootouts) répètent un nom d'équipe : elles devront devenir des clés étrangères vers la table des équipes.
- Les noms d'équipe sont du texte répété des milliers de fois : c'est ce qui justifie une table `EQUIPE` dédiée.
- `results.csv` (49 547 lignes) : aucune valeur manquante.
- `goalscorers.csv` (47 914 lignes) : `scorer` est vide pour 44 buts et `minute`
  pour 254 buts. Ces deux colonnes devront accepter NULL.