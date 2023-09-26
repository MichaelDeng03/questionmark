from pyspark.sql import SparkSession
import numpy as np
import pandas as pd
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType, ArrayType
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# Initialize a Spark session
spark = SparkSession.builder.appName("KMeansWithSpark").getOrCreate()

# Load your data into Spark DataFrames
df_city = spark.read.csv("path/to/your/data.csv", header=True, inferSchema=True)

# Define a UDF to calculate Haversine distance
@udf(VectorUDT())
def haversine_dist(p1, p2):
    lon1, lat1 = p1
    lon2, lat2 = p2
    pi = np.pi
    R = 6371000  # Earth radius in meters
    phi1 = lat1 * pi / 180  # Convert to radians
    phi2 = lat2 * pi / 180  # Convert to radians
    delta_phi = (lat2 - lat1) * pi / 180
    delta_lambda = (lon2 - lon1) * pi / 180

    a = (np.sin(delta_phi / 2)) ** 2 + np.cos(phi1) * np.cos(phi2) * ((np.sin(delta_lambda / 2)) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c  # Haversine distance between point1 and point2 in meters
    return Vectors.dense(round(distance, 2))

# Assemble latitude and longitude into a single feature vector
vec_assembler = VectorAssembler(inputCols=["longitude", "latitude"], outputCol="features")
df_city = vec_assembler.transform(df_city)

# Create a KMeans instance
kmeans = KMeans().setK(5).setSeed(1)

# Fit the model
model = kmeans.fit(df_city)

# Get cluster centers
cluster_centers = model.clusterCenters()

# Show cluster centers
for i, center in enumerate(cluster_centers):
    print(f"Cluster {i + 1} Center: {center}")

# Assign each data point to a cluster
clustered_data = model.transform(df_city)

# Show the cluster assignments
clustered_data.select("longitude", "latitude", "prediction").show()

# Stop the Spark session
spark.stop()
