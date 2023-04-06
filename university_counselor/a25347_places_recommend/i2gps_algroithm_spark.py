#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import matplotlib.pyplot as plt
import seaborn as sns
import pyspark

# # 创建SparkSession
# spark = SparkSession.builder.appName('MusicAnalysis').getOrCreate()

# # 读取CSV文件
# df = spark.read.csv('data/image_gps_data.csv', header=True)

print(pyspark.__version__)


# In[5]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, BucketedRandomProjectionLSH
from pyspark.sql.functions import rand, udf
from pyspark.sql.types import IntegerType
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd


# # spark景点DBSCAN算法试验

# In[6]:


# Read the data from a CSV file
df = pd.read_csv("data/image_gps_data.csv")

# Plot the longitude and latitude values as a scatter plot
plt.scatter(df["longitude"], df["latitude"])
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Spatial Distribution of Data")
plt.show()

# Print the statistics of the longitude and latitude values
print("Longitude statistics:")
print(df["longitude"].describe())
print("Latitude statistics:")
print(df["latitude"].describe())


# In[7]:


# Create a SparkConf object and set the app name
conf = SparkConf().setAppName("DBSCAN Demo")

# Create a SparkContext object
sc = SparkContext(conf=conf)

# Create a SparkSession object
spark = SparkSession.builder.appName("DBSCAN Demo").getOrCreate()
# Read the data from a CSV file and create a DataFrame
df = spark.read.csv("data/image_gps_data.csv", header=True, inferSchema=True)


# In[8]:


# Select the columns that represent the spatial coordinates
cols = ["longitude", "latitude"]
df_coords = df.select(*cols)

# Convert the DataFrame to a feature vector format
vectorAssembler = VectorAssembler(inputCols=cols, outputCol="features")
df_features = vectorAssembler.transform(df_coords).select("features")

# Define the DBSCAN clustering algorithm
eps = 0.1
min_pts = 5
num_hash_tables = 5
brp = BucketedRandomProjectionLSH(inputCol="features", outputCol="hashes", numHashTables=num_hash_tables, bucketLength=eps)
model = brp.fit(df_features)
similarities = model.approxSimilarityJoin(df_features, df_features, eps, distCol="distance")
clustered = similarities.filter(f"distance <= {eps}").groupBy("datasetA").agg(F.collect_set("datasetB").alias("neighbors"))
df_final = clustered.select("neighbors").distinct()

# Show the predicted clusters
df_final.orderBy(rand()).show()


# In[15]:


# Loop through the predicted clusters
for row in df_final.collect():
    cluster = row['neighbors']
    print(f"Cluster: {cluster}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




