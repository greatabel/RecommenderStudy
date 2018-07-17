library(crayon)

library(recommenderlab)

# help(package = "recommenderlab")
cat(black$bold$bgCyan("recommenderlab"), '\n')
data_package <- data(package = "recommenderlab")
data_package$results[,c("Item","Title")]