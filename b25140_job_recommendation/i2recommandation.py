import os
import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt


def recommend(user, ratings, pivot_ratings):
    missing_jobs = list(pivot_ratings[pivot_ratings[user].isnull()].index)
    mean_score = pivot_ratings[user].mean()

    remain_jobs = ratings[ratings["title"].isin(missing_jobs)]
    remain_jobs.is_copy = False
    remain_jobs["similarity"] = remain_jobs["critic"].map(pivot_ratings.corr()[user].get)
    remain_jobs["sim_rating"] = remain_jobs.similarity * remain_jobs.rating

    rec = remain_jobs.groupby("title").apply(
        lambda s: s.sim_rating.sum() / s.similarity.sum()
    )

    recommended_jobs = list(rec[rec >= mean_score].index)

    if not recommended_jobs:
        # fallback option: recommend jobs with the highest overall ratings
        recommended_jobs = list(ratings.groupby('title')['rating'].mean().sort_values(ascending=False).head().index)
        print(colored(f"No suitable jobs found for {user}. Recommending popular jobs instead.", "yellow"))

    return recommended_jobs


def plot_ratings_distribution(ratings):
    ratings.hist(bins=10, figsize=(8,6))
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('Distribution of job ratings')
    plt.show()


def plot_similarity_matrix(pivot_ratings):
    fig, ax = plt.subplots(figsize=(10,10))
    im = ax.imshow(pivot_ratings.corr(), cmap='coolwarm')
    ax.set_xticks(range(len(pivot_ratings.columns)))
    ax.set_yticks(range(len(pivot_ratings.columns)))
    ax.set_xticklabels(pivot_ratings.columns, fontsize=12)
    ax.set_yticklabels(pivot_ratings.columns, fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.set_title('Similarity matrix for job ratings')
    fig.colorbar(im)
    plt.show()


def main(user='Abel'):
    data_path = os.path.join("app", "home")
    ratings = pd.read_csv("data/jobs_rating.csv")
    plot_ratings_distribution(ratings)
    pivot_ratings = ratings.pivot_table(columns="critic", index="title", values="rating")
    plot_similarity_matrix(pivot_ratings)
    recommended_jobs = recommend(user, ratings, pivot_ratings)
    if recommended_jobs:
        print(colored(f"Recommended jobs for {user}: {recommended_jobs}", "green"))
    else:
        print(colored(f"No recommendations found for {user}", "red"))


if __name__ == "__main__":
    main()
