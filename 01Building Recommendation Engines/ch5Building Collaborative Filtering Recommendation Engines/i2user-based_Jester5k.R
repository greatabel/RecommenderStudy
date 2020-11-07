library(crayon)
library(methods)
library(recommenderlab)

data(Jester5k)

cat(black$bold$bgCyan("user-based collaborative model"), '\n')
set.seed(1)
which_train <- sample(x = c(TRUE, FALSE),
                      size = nrow(Jester5k),
                      replace = TRUE,
                      prob = c(0.8, 0.2))
head(which_train)

rec_data_train <- Jester5k[which_train, ]
rec_data_test  <- Jester5k[!which_train, ]

dim(rec_data_train)
dim(rec_data_test)

#Creating user based collaborative model
recommender_models <- recommenderRegistry$get_entries(
                        dataType = "realRatingMatrix")
# recommender_models

# the following code to build a user-based collaborative filtering model
recc_model <- Recommender(data = rec_data_train, method = "UBCF")
recc_model

cat(black$bold$bgCyan("------"), '\n')
n_recommended <- 10
recc_predicted <- predict(object = recc_model,
                          newdata = rec_data_test,
                          n = n_recommended)
recc_predicted

rec_list <- sapply(recc_predicted@items, function(x){
  colnames(Jester5k)[x]
})
class(rec_list)
rec_list[1:2]

number_of_items = sort(unlist(lapply(rec_list, length)),decreasing = TRUE)
table(number_of_items)

#Analyzing the dataset
table(rowCounts(Jester5k))

model_data = Jester5k[rowCounts(Jester5k) < 80]
dim(model_data)
# boxplot(model_data)

# boxplot(rowMeans(model_data [rowMeans(model_data)>=-5 & rowMeans(model_data)<= 7]))

model_data = model_data [rowMeans(model_data)>=-5 & rowMeans(model_data)<= 7]
dim(model_data)
image(model_data, main = "Rating distribution of 100 users")

#Evaluating the recommendation model using k-cross validation
items_to_keep <- 30
rating_threshold <- 3
n_fold <- 5 # 5-fold 
eval_sets <- evaluationScheme(data = model_data, method = "cross-validation",train = percentage_training, given = items_to_keep, goodRating = rating_threshold, k = n_fold)

size_sets <- sapply(eval_sets@runsTrain, length)
 size_sets

model_to_evaluate <- "UBCF"
model_parameters <- NULL
eval_recommender <- Recommender(data = getData(eval_sets, "train"),method = model_to_evaluate, parameter = model_parameters)
eval_recommender
items_to_recommend <- 10

#prediction
eval_prediction <- predict(object = eval_recommender, newdata =getData(eval_sets, "known"), n = items_to_recommend, type = "ratings")
eval_prediction

eval_accuracy <- calcPredictionAccuracy(  x = eval_prediction, data = getData(eval_sets, "unknown"), byUser = TRUE)
head(eval_accuracy)

apply(eval_accuracy,2,mean)
eval_accuracy <- calcPredictionAccuracy(  x = eval_prediction, data = getData(eval_sets, "unknown"), byUser = FALSE)
eval_accuracy

results <- evaluate(x = eval_sets, method = model_to_evaluate, n = seq(10, 100, 10))
head(getConfusionMatrix(results)[[1]])

columns_to_sum <- c("TP", "FP", "FN", "TN")
indices_summed <- Reduce("+", getConfusionMatrix(results))[, columns_to_sum]
head(indices_summed)
plot(results, annotate = TRUE, main = "ROC curve")
