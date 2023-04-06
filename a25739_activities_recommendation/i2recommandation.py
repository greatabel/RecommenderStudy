import os
import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt


def recommend(user, ratings, pivot_ratings):
    missing_activities = list(pivot_ratings[pivot_ratings[user].isnull()].index)
    mean_score = pivot_ratings[user].mean()

    remain_activities = ratings[ratings["title"].isin(missing_activities)]
    remain_activities.is_copy = False
    remain_activities["similarity"] = remain_activities["critic"].map(
        pivot_ratings.corr()[user].get
    )
    remain_activities["sim_rating"] = remain_activities.similarity * remain_activities.rating

    rec = remain_activities.groupby("title").apply(
        lambda s: s.sim_rating.sum() / s.similarity.sum()
    )

    recommended_activities = list(rec[rec >= mean_score].index)

    if not recommended_activities:
        # fallback option: recommend activities with the highest overall ratings
        recommended_activities = list(
            ratings.groupby("title")["rating"]
            .mean()
            .sort_values(ascending=False)
            .head()
            .index
        )
        print(
            colored(
                f"No suitable activities found for {user}. Recommending popular activities instead.",
                "yellow",
            )
        )

    return recommended_activities


def plot_ratings_distribution(ratings):
    ratings.hist(bins=10, figsize=(8, 6))
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Distribution of activities ratings")
    plt.show()


def plot_similarity_matrix(pivot_ratings):
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(pivot_ratings.corr(), cmap="coolwarm")
    ax.set_xticks(range(len(pivot_ratings.columns)))
    ax.set_yticks(range(len(pivot_ratings.columns)))
    ax.set_xticklabels(pivot_ratings.columns, fontsize=12)
    ax.set_yticklabels(pivot_ratings.columns, fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.set_title("Similarity matrix for activities ratings")
    fig.colorbar(im)
    plt.show()


def main(user="Abel"):
    data_path = os.path.join("app", "home")
    mypath = "data/activities_rating.csv"
    ratings = pd.read_csv(mypath)
    plot_ratings_distribution(ratings)
    pivot_ratings = ratings.pivot_table(
        columns="critic", index="title", values="rating"
    )
    plot_similarity_matrix(pivot_ratings)
    recommended_activities = recommend(user, ratings, pivot_ratings)
    if recommended_activities:
        print(colored(f"Recommended activities for {user}: {recommended_activities}", "green"))
    else:
        print(colored(f"No recommendations found for {user}", "red"))
    return recommended_activities


if __name__ == "__main__":
    main()
