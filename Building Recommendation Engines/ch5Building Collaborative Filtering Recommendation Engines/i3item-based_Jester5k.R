library(crayon)
library(methods)
library(recommenderlab)

data(Jester5k)

cat(black$bold$bgCyan("item-based collaborative model"), '\n')

library(recommenderlab)
data("Jester5k")
model_data = Jester5k[rowCounts(Jester5k) < 80]
model_data
# boxplot(rowMeans(model_data))
 dim(model_data[rowMeans(model_data) < -5])
 dim(model_data[rowMeans(model_data) > 7])
 
model_data = model_data [rowMeans(model_data)>=-5 & rowMeans(model_data)<= 7]
model_data

which_train <- sample(x = c(TRUE, FALSE), size = nrow(model_data),
 replace = TRUE, prob = c(0.8, 0.2))
class(which_train)
head(which_train)

 model_data_train <- model_data[which_train, ]
dim(model_data_train)

 model_data_test <- model_data[!which_train, ]
 dim(model_data_test)

 
model_to_evaluate <- "IBCF"
model_parameters <- list(k = 30)

model_recommender <- Recommender(data = model_data_train,method = model_to_evaluate, parameter = model_parameters)
model_recommender

model_details = getModel(model_recommender)
str(model_details)

items_to_recommend <- 10
model_prediction <- predict(object = model_recommender, newdata = model_data_test, n = items_to_recommend)

model_prediction
print(class(model_prediction))

slotNames(model_prediction)

model_prediction@items[[1]]
 recc_user_1  = model_prediction@items[[1]]
  jokes_user_1 <- model_prediction@itemLabels[recc_user_1]
   jokes_user_1

#evalutation   
n_fold <- 4
items_to_keep <- 15
rating_threshold <- 3
eval_sets <- evaluationScheme(data = model_data, method = "cross-validation",k = n_fold, given = items_to_keep, goodRating =rating_threshold)
size_sets <- sapply(eval_sets@runsTrain, length)
size_sets

model_to_evaluate <- "IBCF"
model_parameters <- NULL

getData(eval_sets,'train')

eval_recommender <- Recommender(data = getData(eval_sets, "train"),method = model_to_evaluate, parameter = model_parameters)
#setting the number of items to be set for recommendations
items_to_recommend <- 10

eval_prediction <- predict(object = eval_recommender, newdata = getData(eval_sets, "known"), n = items_to_recommend, type = "ratings")
class(eval_prediction)

#metrics
eval_accuracy <- calcPredictionAccuracy(x = eval_prediction, data = getData(eval_sets, "unknown"), byUser = TRUE)
head(eval_accuracy) 
apply(eval_accuracy,2,mean) 

eval_accuracy <- calcPredictionAccuracy(x = eval_prediction, data = getData(eval_sets, "unknown"), byUser = FALSE) 
eval_accuracy

results <- evaluate(x = eval_sets, method = model_to_evaluate, n = seq(10,100,10))
results@results[1] 

 columns_to_sum <- c("TP", "FP", "FN", "TN","precision","recall")
indices_summed <- Reduce("+", getConfusionMatrix(results))[, columns_to_sum] 
head(indices_summed) 

plot(results, annotate = TRUE, main = "ROC curve")
plot(results, "prec/rec", annotate = TRUE, main = "Precision-recall") 

vector_k <- c(5, 10, 20, 30, 40) 
model1 <- lapply(vector_k, function(k,l){   list(name = "IBCF", param = list(method = "cosine", k = k)) }) 

names(model1) <- paste0("IBCF_cos_k_", vector_k)  
 names(model1) 
 
model2 <- lapply(vector_k, function(k,l){   list(name = "IBCF", param = list(method = "pearson", k = k))
}) 

names(model2) <- paste0("IBCF_pea_k_", vector_k)
names(model2) 

models = append(model1,model2) 
n_recommendations <- c(1, 5, seq(10, 100, 10)) 

list_results <- evaluate(x = eval_sets, method = models, n= n_recommendations) 

plot(list_results, annotate = c(1,2), legend = "topleft")
# title("ROC curve")
plot(list_results, "prec/rec", annotate = 1, legend = "bottomright")
# title("Precision-recall")
