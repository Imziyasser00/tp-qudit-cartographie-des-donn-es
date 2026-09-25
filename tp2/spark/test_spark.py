from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").master("local[*]").getOrCreate()
df = spark.createDataFrame([(1, "test"), (2, "ok")], ["id", "valeur"])
df.show()
spark.stop()