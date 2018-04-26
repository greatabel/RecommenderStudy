library(crayon)

cat(black$bold$bgCyan("读取电影打分"), '\n')


MyData <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
MyData