library(crayon)
library(reshape2)


cat(black$bold$bgCyan("转换数据为矩阵形式
      使用 reshape2包 的acast()"), '\n')

'The cast function takes the ratings dataset as input, title as row attribute, 
critic as column attribute, and rating as value.'

ratings <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
movie_ratings = as.data.frame(
    acast(ratings, title~critic, value.var="rating"))

movie_ratings
# View(movie_ratings)
# tableHTML(movie_ratings, rownames = FALSE)