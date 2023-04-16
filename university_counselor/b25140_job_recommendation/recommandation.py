import os
import csv

import pandas as pd


"""
1.读取数据：从CSV文件中读取用户对职位描述的评价数据，并转换为适合使用的数据结构。
2.计算相似度矩阵：基于职位描述评分数据计算职位描述之间的相似度，以便为每个用户生成个性化的推荐列表。
3. 为指定用户生成推荐列表：对于指定用户，找到该用户未评分的职位描述，并为这些职位描述计算推荐得分。
4. 然后，过滤掉得分低于该用户已评分职位描述平均分的职位描述，并将得分高的职位描述加入推荐列表。
5. 输出推荐列表：将生成的推荐列表输出到控制台或文件中，以便用户查看推荐结果。
6. 提供用户界面：为用户提供一个界面，以便输入用户信息并查看推荐结果。这可能涉及到编写Web flask前端。
"""


def recommend(demo, ratings, pivot_ratings):

    missing_films = list(pivot_ratings[pivot_ratings[demo].isnull()].index)
    print(missing_films)

    mean_score = pivot_ratings[demo].mean()
    print("mean_score=", mean_score)

    remain_films = ratings[ratings["title"].isin(missing_films)]
    remain_films.is_copy = False
    remain_films["similarity"] = remain_films["critic"].map(sm[demo].get)
    remain_films["sim_rating"] = remain_films.similarity * remain_films.rating

    print(remain_films)

    rec = remain_films.groupby("title").apply(
        lambda s: s.sim_rating.sum() / s.similarity.sum()
    )

    print(rec)
    rec = rec[rec >= mean_score]
    print("该用户我推荐：", list(rec.index))


def main(demo="Abel"):
    print("main", demo)
    data_path = os.path.join("app", "home")

    mypath = "data/jobs_rating.csv"
    print(mypath)
    ratings = pd.read_csv(mypath)

    pivot_ratings = ratings.pivot_table(
        columns="critic", index="title", values="rating"
    )

    print(pivot_ratings.to_string())

    sm = pivot_ratings.corr()
    print(sm.to_string())
    # 协同过滤推荐
    # demo = "Abel"
    # print(colored('1. 找出该用户为打分的职位描述 =>', 'red', attrs=['reverse', 'blink']))
    missing_films = list(pivot_ratings[pivot_ratings[demo].isnull()].index)
    print(missing_films)
    # print(colored('2. 找出该用户已打分的平均分=>', 'red', attrs=['reverse', 'blink']))

    mean_score = pivot_ratings[demo].mean()
    print("mean_score=", mean_score)
    # print(colored('3. 处理原始表，加上相似性列，筛选出未打分 =>',
    #               'red', attrs=['reverse', 'blink']))
    remain_films = ratings[ratings["title"].isin(missing_films)]
    remain_films.is_copy = False
    remain_films["similarity"] = remain_films["critic"].map(sm[demo].get)
    remain_films["sim_rating"] = remain_films.similarity * remain_films.rating

    print(remain_films)
    # print(colored('4. 汇总算出职位描述平均相似值 =>',
    #               'red', attrs=['reverse', 'blink']))
    rec = remain_films.groupby("title").apply(
        lambda s: s.sim_rating.sum() / s.similarity.sum()
    )

    print(rec)
    rec = rec[rec >= mean_score]
    print("该用户我推荐：", list(rec.index))
    return list(rec.index)


if __name__ == "__main__":
    main()
