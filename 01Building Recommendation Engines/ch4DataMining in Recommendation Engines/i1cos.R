library(crayon)
library(lsa)

cat(black$bold$bgCyan("计算cosine distance"), '\n')
vec1 = c(1, 1, 1, 0, 0, 1)
vec2 = c(0, 1, 0, 1, 1, 1)

vec1
vec2

'cosine=>'
cosine(vec1, vec2)