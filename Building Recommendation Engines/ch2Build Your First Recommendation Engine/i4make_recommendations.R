library(crayon)
library(reshape2)
library(data.table)
library(dplyr)
cat(black$bold$bgCyan("推荐"), '\n')

ratings <- read.csv(file="../data/movie_rating.csv", header=TRUE, sep=",")
movie_ratings = as.data.frame(
    acast(ratings, title~critic, value.var="rating"))
sim_users = cor(movie_ratings[,1:6],use="complete.obs")


#function to make recommendations 
generateRecommendations <- function(userId){
  rating_critic  = setDT(movie_ratings[colnames(movie_ratings)[userId]],keep.rownames = TRUE)[]
  names(rating_critic) = c('title','rating')
  titles_na_critic = rating_critic$title[is.na(rating_critic$rating)]
  ratings_t =ratings[ratings$title %in% titles_na_critic,]
  #add similarity values for each user as new variable
  x = (setDT(data.frame(sim_users[,userId]),keep.rownames = TRUE)[])
  names(x) = c('critic','similarity')
  ratings_t =  merge(x = ratings_t, y = x, by = "critic", all.x = TRUE)
  #mutiply rating with similarity values
  ratings_t$sim_rating = ratings_t$rating*ratings_t$similarity
  #predicting the non rated titles
  result = ratings_t %>% group_by(title) %>% summarise(sum(sim_rating)/sum(similarity))
  return(result)
}

for (i in 1:6){
  print( generateRecommendations(i) )
}
