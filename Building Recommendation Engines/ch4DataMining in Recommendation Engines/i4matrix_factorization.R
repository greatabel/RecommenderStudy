library(crayon)
library(recommenderlab)
library(methods)
library(NMF)

data("MovieLense")
dim(MovieLense)


# image(MovieLense[1:100,1:100])


# head(MovieLense, n=5)
mat  = as(MovieLense,"matrix")
mat[is.na(mat)] = 0

res = nmf(mat, 10)

cat(black$bold$bgCyan("res=>"), '\n')
res

#fitted values
r.hat <- fitted(res)
dim(r.hat)

p <- basis(res)
dim(p)
q <- coef(res)
dim(q)
