from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("Local Application").getOrCreate()

rdd = spark.sparkContext.parallelize(range(1, 100))

print("THE SUM IS HERE: ", rdd.sum())
# Stop the SparkSession
spark.stop()
