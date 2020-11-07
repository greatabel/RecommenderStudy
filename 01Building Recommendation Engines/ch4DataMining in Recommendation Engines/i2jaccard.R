library(crayon)
library(clusteval)


cat(black$bold$bgCyan("计算jaccard"), '\n')

vec1 = c( 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ) 
vec2 = c( 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0 )

vec1
vec2

cluster_similarity(vec1, vec2, similarity = "jaccard")

