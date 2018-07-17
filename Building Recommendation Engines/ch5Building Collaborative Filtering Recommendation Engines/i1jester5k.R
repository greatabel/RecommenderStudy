library(crayon)

library(recommenderlab)

# help(package = "recommenderlab")
cat(black$bold$bgCyan("Jester5k"), '\n')

data(Jester5k)

nratings(Jester5k)

class(Jester5k)

'dim(Jester5k) =>'
dim(Jester5k)
