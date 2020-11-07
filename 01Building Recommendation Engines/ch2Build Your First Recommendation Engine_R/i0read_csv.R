library(crayon)

cat(black$bold$bgCyan("读取电影打分"), '\n')


ratings <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
ratings

cat(black$bold$bgCyan("头6条记录"), '\n')
head(ratings)

cat(black$bold$bgCyan("数据维度"), '\n')
dim(ratings)

cat(black$bold$bgCyan("输入数据的结构"), '\n')
str(ratings)

'levels(ratings$critic)'; levels(ratings$critic)
'levels(ratings$title)';  levels(ratings$title)
'levels(ratings$rating)'; levels(ratings$rating)
cat(black$bold$bgCyan("sort(unique(ratings$rating), decreasing = F)"), '\n')
sort(unique(ratings$rating), decreasing = F)
