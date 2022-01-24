import random

import numpy as np
import matplotlib.pyplot as plt

from i0content_based_recommend import recommend_songs
# saved results
# i0 和 i1的实验结果和预设值
# content_r = [
#     "Sick",
#     "Eat It",
#     "I Cain't Say No",
#     "Poppies",
#     "Older Gods",
#     "Most Of Us",
#     "I Don't Wanna Work",
#     "Sifting",
#     "The Tin Man",
#     "I Don't Know Why",
# ]
content_r = recommend_songs
# print(content_r, '@'*10, type(content_r))

cf_r = [
    "Nine Million Bicycles",
    "If You Were A Sailboat",
    "Shy Boy",
    "I Cried For You",
    "Spider's Web",
    "Piece By Piece",
    "On The Road Again",
    "Blues In The Night",
    "Blue Shoes",
    "Thank You Stars",
]
# print(cf_r, type(cf_r))
content_target = [
    "Sick",
    "Eat It",
    "I Cain't Say No",
    "Poppies",
    "Older Gods",
    "Most Of Us",
    "I Don't Wanna Work",
    "Sifting",
    "Yesterday Once More",
    "Love Story",
]
cf_target = [
    "Thank U, Next",
    "If You Were A Sailboat",
    "Shy Boy",
    "I Cried For You",
    "Spider's Web",
    "Piece By Piece",
    "On The Road Again",
    "Blues In The Night",
    "Blue Shoes",
    "Thank You Stars",
]


r1 = 0
for item in content_r:
    if item in content_target:
        r1 += 1
accuracy11 = r1 / len(content_r)
print(accuracy11)


r2 = 0
for item in cf_r:
    if item in cf_target:
        r2 += 1
accuracy22 = r2 / len(content_r)
print(accuracy22)


weights = [x * 0.1 for x in range(0, 10)]
print("weights=\n", weights)

# my distribute weight between content recommend and collaborate filter

combines_accuracy = [
    accuracy11 * ((w - 0.5) ** 2) + accuracy22 * (1 - (w - 0.5) ** 2) for w in weights
]
print("combines_accuracy=\n", combines_accuracy)


plt.scatter(weights, combines_accuracy)
plt.plot(weights, combines_accuracy)

plt.xlabel("weights of distribute of content and collabfilter")
plt.ylabel("accuracy")

plt.show()

# get the final recommend reuslts
print("#" * 30)
numbers = list(range(0, 9))
# print('numbers=', numbers)
results = []

for i in range(5):
    choice = random.choice(numbers)
    print(choice)
    c = content_r[choice]
    if c not in results:
        results.append(c)

for i in range(5):
    choice = random.choice(numbers)
    print(choice)
    c = cf_r[choice]
    if c not in results:
        results.append(c)

print("final recommend results=", results)
