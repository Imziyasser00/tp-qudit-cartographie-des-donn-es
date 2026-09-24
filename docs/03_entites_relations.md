# Entités, attributs et relations

## 1. Entités

| Entité | Rôle | Attributs principaux | Origine |
|---|---|---|---|
| EQUIPE | Sélection nationale | nom | home_team, away_team, team, winner, current |
| TOURNOI | Compétition ou type de match | nom | tournament |
| MATCH | Rencontre entre deux équipes | date, ville, pays, terrain neutre, score domicile, score extérieur | results.csv |
| BUT | But marqué pendant un match | buteur, minute, penalty, but contre son camp | goalscorers.csv |
| TIRS_AU_BUT | Séance de tirs au but d'un match | vainqueur, première équipe à tirer | shootouts.csv |
| ANCIEN_NOM | Ancien nom d'une équipe | nom ancien, date début, date fin | former_names.csv |

## 2. Relations et cardinalités

EQUIPE      1 ───── N  MATCH        (équipe à domicile)
EQUIPE      1 ───── N  MATCH        (équipe à l'extérieur)
TOURNOI     1 ───── N  MATCH
MATCH       1 ───── N  BUT          (un match a 0 à N buts)
EQUIPE      1 ───── N  BUT          (équipe créditée du but)
MATCH       1 ───── 0..1 TIRS_AU_BUT
EQUIPE      1 ───── N  TIRS_AU_BUT  (équipe vainqueur)
EQUIPE      1 ───── N  TIRS_AU_BUT  (équipe qui tire en premier, optionnel)
EQUIPE      1 ───── N  ANCIEN_NOM

## 3. Justification des choix

- **EQUIPE est une table à part** : les noms d'équipes apparaissent dans quatre
  fichiers et sont répétés des dizaines de milliers de fois. Une table unique
  évite les doublons et les fautes de frappe.
- **Deux relations MATCH → EQUIPE** : un match a toujours exactement une équipe
  à domicile et une à l'extérieur, donc deux clés étrangères distinctes.
- **TOURNOI est une table à part** : le nom du tournoi est répété pour tous
  les matchs de la compétition.
- **BUT est en 1-N avec MATCH** : un match peut avoir 0 but (0-0) ou plusieurs.
- **TIRS_AU_BUT est en 0..1 avec MATCH** : seuls 683 matchs ont une séance de
  tirs au but, et un match n'en a jamais plus d'une. On sépare pour ne pas avoir
  de colonnes presque toujours vides dans MATCH.
- **Pas d'entité JOUEUR** : le fichier ne contient que le nom du buteur, sans
  identifiant, sans date de naissance. Deux joueurs différents peuvent porter le
  même nom, et créer une table JOUEUR reviendrait à inventer des identités.
  `buteur` reste donc un attribut texte de BUT.
- **Ville et pays restent dans MATCH** : ce sont des attributs descriptifs sans
  relation propre. Le pays est le nom à l'époque du match (ex. Gold Coast),
  ce qui ne correspond pas à un nom d'EQUIPE actuel.
- **ANCIEN_NOM est lié à EQUIPE** : chaque ligne relie un ancien nom à un
  nom actuel, avec une période de validité.
- **Clé technique** : les fichiers n'ont pas d'identifiant de match. On crée
  `id_match`, alimenté à l'import à partir de date + home_team + away_team.

## 4. Points de vigilance

- Un but ou une séance de tirs au but doit retrouver son match via
  date + home_team + away_team. Il faudra vérifier que chaque ligne trouve
  exactement un match.
- `scorer` et `minute` peuvent être NULL (44 et 254 lignes).