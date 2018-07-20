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
print(data.take(5))

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
ratings = data.map(lambda l: l.split('\t'))\
        .map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))
print(type(ratings), ratings.take(5))

#divide the original data into training and test datasets randomly as below using randomSplit() method:
(training, test) = ratings.randomSplit([0.8, 0.2])

spark = SQLContext(sc)
#creating a dataframe object from ratings rdd object as below:
df = spark.createDataFrame(ratings)

# Build the recommendation model using Alternating Least Squares
#setting rank and maxIter parameters
rank = 10
numIterations = 10

#calling train() method with training data, rank, maxIter params.
model = ALS.train(training, rank, numIterations)
#below code extracts each row in the test data and extracts userID, 
# ItemID and puts it in testdata pipelinedRDD object.
testdata = test.map(lambda p: (p[0], p[1]))
print('testdata.take(5)=', testdata.take(5))

pred_ind = model.predict(119, 392)
print(pred_ind)

predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
# create a ratesAndPreds object by joining original ratings and predictions
ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
from math import sqrt
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
rmse = sqrt(MSE)
print('rmse=', rmse)

