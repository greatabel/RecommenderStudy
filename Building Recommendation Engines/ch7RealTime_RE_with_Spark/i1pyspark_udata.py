import findspark
findspark.init()

import os

from pyspark import SparkContext
from pyspark import SQLContext

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = current_path.rsplit('/',1)[0] + '/data/ml-100k_udata.csv'


sc = SparkContext("local","my_pyspark")
data = sc.textFile(data_path)
print(type(data), data.count(), data.first())