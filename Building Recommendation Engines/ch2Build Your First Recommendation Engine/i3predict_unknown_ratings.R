library(crayon)
library(reshape2)
library(data.table)

cat(black$bold$bgCyan("预测"), '\n')


ratings <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
movie_ratings = as.data.frame(
    acast(ratings, title~critic, value.var="rating"))
sim_users = cor(movie_ratings[,1:6],use="complete.obs")

cat(black$bold$bgCyan("提取Toby的电影标题"), '\n')
rating_critic  = setDT(movie_ratings[colnames(movie_ratings)[6]],
                        keep.rownames = TRUE)[]

names(rating_critic) = c('title','rating')
rating_critic

cat(black$bold$bgCyan("分离出没有打分的标题"), '\n')
titles_na_critic = rating_critic$title[is.na(rating_critic$rating)]
titles_na_critic


cat(black$bold$bgCyan("SQL 找出所有记录根据上面过滤出的电影名字"), '\n')
ratings_t =ratings[ratings$title %in% titles_na_critic,]
ratings_t

cat(black$bold$bgGreen("添加相似性"), '\n')
x = (setDT(data.frame(sim_users[,6]),keep.rownames = TRUE)[])
names(x) = c('critic','similarity')
x
cat(black$bold$bgGreen("合并SQL记录和相似性"), '\n')
ratings_t =  merge(x = ratings_t, y = x, by = "critic", all.x = TRUE)
ratings_t