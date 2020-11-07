library(crayon)

cat(black$bold$bgCyan("欧几里得距离"), '\n')
x1 <- rnorm(30)
x2 <- rnorm(30)

x1
x2

'Euc_dist=>'
Euc_dist = dist(rbind(x1, x2), method='euclidean')
Euc_dist