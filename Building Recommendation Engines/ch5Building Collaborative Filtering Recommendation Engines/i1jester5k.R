library(crayon)
library(methods)

library(recommenderlab)

# help(package = "recommenderlab")
cat(black$bold$bgCyan("Jester5k"), '\n')

data(Jester5k)

nratings(Jester5k)

class(Jester5k)

'dim(Jester5k) =>'
dim(Jester5k)

# hist(getRatings(Jester5k), main="Distribution of ratings")
# head(Jester5k)
head(as(Jester5k,"matrix")[,1:10])