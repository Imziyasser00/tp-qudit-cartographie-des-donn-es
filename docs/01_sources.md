# Sources de données

Les 4 fichiers proviennent du même jeu de données : **International football results
from 1872**, collecté et maintenu par Mart Jürisoo (martj42).

| Fichier | Description | Format | Nature |
|---|---|---|---|
| `results.csv` | Résultats des matchs internationaux masculins (date, équipes, scores, tournoi, lieu) | CSV | Structurée |
| `goalscorers.csv` | Buts marqués (buteur, minute, penalty, csc) | CSV | Structurée |
| `shootouts.csv` | Vainqueur des séances de tirs au but | CSV | Structurée |
| `former_names.csv` | Anciens noms des équipes nationales avec leurs dates | CSV | Structurée |

## Informations communes

- **Organisation / origine** : Mart Jürisoo (@martj42), publié sur Kaggle et GitHub
- **URL Kaggle** : https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017
- **URL GitHub** : https://github.com/martj42/international_results
- **Couverture** : matchs internationaux masculins de 1872 à aujourd'hui (environ 49 000 matchs)
- **Exclusions** : pas de Jeux olympiques, ni de matchs impliquant une équipe B, U-23 ou une sélection de ligue

## Liens entre les fichiers

Il n'y a **pas d'identifiant de match** dans les fichiers. Le lien se fait par
la combinaison `date + home_team + away_team`. Cette clé naturelle sera remplacée
par une clé primaire technique (`id_match`) dans la base PostgreSQL.

## Points d'attention (qualité des données)

- Les noms d'équipes utilisent le nom **actuel** (ex. l'« Ireland » de 1882 apparaît comme Northern Ireland).
- Les noms de pays (colonne `country`) utilisent le nom **de l'époque** du match.
- Certains scores peuvent être vides (`NA`) pour des matchs sans résultat connu.
- `former_names.csv` sert à faire le lien entre les anciens et les noms actuels.