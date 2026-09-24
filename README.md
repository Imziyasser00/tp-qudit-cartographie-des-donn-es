# TP Audit & cartographie des données : Football international

## 1. Présentation du sujet

**Thème choisi : Sport (football).**

### Contexte
Le football international génère depuis 1872 une grande quantité de données :
matchs, scores, tournois, buteurs, séances de tirs au but. Ces données existent
sous forme de fichiers CSV séparés, sans identifiants techniques qui les relient
proprement entre eux.

### Problématique
Comment transformer des fichiers CSV bruts et indépendants en une base de données
relationnelle cohérente, sans doublons, où l'on peut interroger les équipes, les
matchs, les tournois et les buteurs ?

### Objectif
À partir de données réelles, réaliser :
1. l'audit des sources et leur dictionnaire de données ;
2. l'identification des entités et relations ;
3. les modèles conceptuel et logique ;
4. une base PostgreSQL fonctionnelle, avec des données de test.