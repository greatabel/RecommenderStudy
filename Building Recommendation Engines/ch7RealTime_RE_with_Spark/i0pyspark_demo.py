import findspark
findspark.init()

from pyspark import SparkContext
from pyspark import SQLContext

sc = SparkContext("local","my_pyspark")
spark = SQLContext(sc)

from pyspark import Row
rdd = sc.parallelize([
        Row(name='Michael',age=29),
        Row(name='Andy', age=30),
        Row(name='Justin', age=19)
    ])
df1 = spark.createDataFrame(rdd)
df1.show()
