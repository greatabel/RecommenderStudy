library(crayon)
library(clusteval)


cat(black$bold$bgCyan("计算pearson"), '\n')

DF <- data.frame(temp = rnorm(10), gdd=rnorm(10), ai=rnorm(10), precip=rnorm(10))

DF

'cor(as.matrix(DF)) =>'
cor(as.matrix(DF), method='pearson')



