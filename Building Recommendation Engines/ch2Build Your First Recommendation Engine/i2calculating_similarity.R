library(crayon)
library(reshape2)


cat(black$bold$bgCyan("计算相似性 similarity calculation"), '\n')

'使用cor()的"complete.obs" 属性, 来进行全观测'

ratings <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
movie_ratings = as.data.frame(
    acast(ratings, title~critic, value.var="rating"))
movie_ratings

cat(black$bold$bgCyan("sim_users"), '\n')
sim_users = cor(movie_ratings[,1:6],use="complete.obs")
sim_users