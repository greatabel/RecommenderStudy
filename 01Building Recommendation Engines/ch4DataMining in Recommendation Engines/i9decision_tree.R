library(crayon)

cat(black$bold$bgCyan("计算decision tree"), '\n')

library(tree) 
data(iris) 
sample = iris[sample(nrow(iris)),] 
train = sample[1:105,] 
test = sample[106:150,] 
model = tree(Species~.,train) 
summary(model)
plot(model)
text(model)