import csv
import random

# 生成20条随机数据
activities = ["学习Python编程", "学习机器学习", "健身", "游泳", "瑜伽", "爬山", "看电影", "逛街", "打游戏", "唱歌", "跳舞", "看书", "画画", "旅游", "摄影", "钓鱼", "骑行", "DIY手工", "烹饪", "品茶"]
users = ["Jack Matthews", "Mick LaSalle", "Claudia Puig", "Lisa Rose", "Abel",
        "guest_test","Gene Seymour,"]
data = []
for user in users:
    user_activities = random.sample(activities, random.randint(1, len(activities)))
    for activity in user_activities:
        rating = random.randint(1, 5)
        data.append([user, activity, rating])

# 将数据写入 CSV 文件
with open("data/activities_rating.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["critic", "title", "rating"])
    writer.writerows(data)

