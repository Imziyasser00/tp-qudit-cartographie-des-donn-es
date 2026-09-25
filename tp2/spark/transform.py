import glob
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.appName("football_clean").master("local[*]").getOrCreate()

# 1. Charger le dernier fichier agrégé
AGG_DIR = "../datalake/aggregated"
files = sorted(glob.glob(os.path.join(AGG_DIR, "matches_aggregated_*.csv")))
if not files:
    raise FileNotFoundError("Aucun fichier agrégé trouvé. Lancez aggregator/aggregate.py d'abord.")
latest_file = files[-1]
print(f"Lecture de : {latest_file}")

df = spark.read.csv(latest_file, header=True, inferSchema=False)
print(f"Lignes brutes chargées : {df.count()}")

# 2. Typage explicite des colonnes
df = df.withColumn("score_domicile", F.col("score_domicile").cast(IntegerType()))
df = df.withColumn("score_exterieur", F.col("score_exterieur").cast(IntegerType()))
df = df.withColumn("date_match", F.to_date(F.col("date_match"), "yyyy-MM-dd"))

# 3. Normalisation des noms d'équipes / compétitions (trim + espaces multiples)
for col_name in ["equipe_domicile", "equipe_exterieur", "competition", "pays", "ville"]:
    df = df.withColumn(col_name, F.trim(F.regexp_replace(F.col(col_name), r"\s+", " ")))

# 4. Gestion des valeurs manquantes
# - ville : NULL toléré (déjà NULL pour toutes les lignes API)
# - scores : NULL toléré uniquement si statut != FINISHED
lignes_avant = df.count()
df = df.filter(
    (F.col("statut") != "FINISHED") |
    (F.col("score_domicile").isNotNull() & F.col("score_exterieur").isNotNull())
)
lignes_apres = df.count()
print(f"Lignes supprimées (score manquant sur match terminé) : {lignes_avant - lignes_apres}")

# 5. Suppression des doublons
# - doublons stricts (toutes colonnes identiques)
avant = df.count()
df = df.dropDuplicates()
print(f"Doublons stricts supprimés : {avant - df.count()}")

# - doublons API par id_externe (garder une seule ligne par match API)
avant = df.count()
df_api = df.filter(F.col("source") == "api_live").dropDuplicates(["id_externe"])
df_csv = df.filter(F.col("source") == "csv_historique")
df = df_csv.unionByName(df_api)
print(f"Doublons API par id_externe supprimés : {avant - df.count()}")

# 6. Résultat final
print(f"Lignes propres finales : {df.count()}")
df.show(5, truncate=False)

# 7. Écriture du résultat propre (via pandas pour éviter les soucis Hadoop/winutils sur Windows)
OUTPUT_DIR = "../datalake/clean"
os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf = df.toPandas()
output_file = os.path.join(OUTPUT_DIR, "matches_clean.csv")
pdf.to_csv(output_file, index=False, encoding="utf-8")
print(f"Données propres écrites dans {output_file}")

spark.stop()