import csv
import random


template_condition = [
    ("不是", "而是"),
    ("一旦", "就"),
    ("虽然", "但是"),
    ("如果", "那么"),
    ("尽管", "但"),
    ("或", "或"),
    ("不仅", "也"),
    ("既", "也"),
]

template_event = [
    ("人类都资源是不是太多了呢", "也许恰恰相反, 或许是太少"),
    ("小幅提涨", "成交不多"),
    ("多了", "少了"),
    ("缓慢", "步伐坚定"),
    ("目的", "手段"),
    ("觉得有点坑", "毫无办法"),
    ("速缓", "质更优"),
    ("封闭的", "开放包容的"),
    ("起步稍晚", "热度不减"),
    ("世界经济在动荡", "我们努力稳定就业"),
    ("国家大范围严打", "很多歹徒落网"),
    ("警察破获了一起案件", "嫌疑人被抓"),
    ("世界经济进一步进入全球化结单", "我们的经济所以进一步发展，因为外部因素在改善"),
    ("世界经济需求在下降", "我们同时也被影响到，所以我们要采取更多刺激措施"),
]


def main():

    rows = []
    turn = 3
    for t in range(turn):
        for i in range(len(template_condition)):
            for j in range(len(template_event)):
                condition = template_condition[i]
                event = template_event[j]
                row = condition[0] + event[0] + condition[1] + event[1]
                print(condition, "#" * 5, event, "->" * 5, row)
                rows.append([row])

    print("len(rows)=", len(rows))

    with open("data/event_data.csv", "w") as myfile:

        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        for r in rows:
            wr.writerow(r)

    # with open("data/event_data.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(rows)

    # with open("output.csv", "wb") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(a)

    return rows


if __name__ == "__main__":
    main()
