import re


def pattern_cause(data):
    "data.type: [文字]"
    data = str(data)

    patterns = []

    key_words = ["起火", "事故", "火灾"]
    pattern = re.compile(".*?(?:{0})原因(.*?)[,.?:;!，。？：；！]".format("|".join(key_words)))
    patterns.append(pattern)
    for c in patterns:
        print("事故原因：", c.search(data).group(1))


def pattern_lose(data):
    "data.type: [文字]"
    data = str(data)
    patterns = []

    key_words = ["伤亡", "损失"]
    pattern = re.compile(".*?(未造成.*?(?:{0}))[,.?:;!，。？：；]".format("|".join(key_words)))
    patterns.append(pattern)

    patterns.append(re.compile("(\d+人死亡)"))
    patterns.append(re.compile("(\d+人身亡)"))
    patterns.append(re.compile("(\d+人受伤)"))
    patterns.append(re.compile("(\d+人烧伤)"))
    patterns.append(re.compile("(\d+人坠楼身亡)"))
    patterns.append(re.compile("(\d+人遇难)"))
    for i in patterns:
        jieguo = i.search(data)
        if not jieguo:
            pass
        else:
            print("事故伤亡：", jieguo.group(1))


# 事故时间：
def pattern_time(data):
    data = "".join(test_data)  # data.type :str
    PATTERN = r"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上中下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?"
    pattern = re.compile(PATTERN)
    m = pattern.search(data)
    # "19年1月14日18时19分39秒上午"
    m1 = pattern.search("上午")
    year = m.group(1)  # 年
    month = m.group(2)  # 月
    day = m.group(3)  # 日
    am = m.group(4)  # 上午，中午，下午，早中晚
    hour = m.group(5)  # 时
    minutes = m.group(6)  # 分
    seconds = m.group(7)  # 秒
    print("事故时间: ", year, month, day, am, hour, minutes, seconds)


# 事件地点
def pattern_address(data):
    data = "".join(data)  # 转换格式
    p_string = data.split("，")  # 分句
    address = []
    for line in p_string:
        line = str(line)
        PATTERN1 = r"([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:镇)){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|街|街道)){0,1}([\d]{1,3}?(号)){0,1}"
        # \u4e00-\u9fa5 匹配任何中文
        # {2,5} 匹配2到5次
        # ? 前面可不匹配
        # (?:pattern) 如industr(?:y|ies) 就是一个比 'industry|industries' 更简略的表达式。意思就是说括号里面的内容是一个整体是以y或者ies结尾的单词
        pattern = re.compile(PATTERN1)
        p1 = ""
        p2 = ""
        p3 = ""
        p4 = ""
        p5 = ""
        p6 = ""
        m = pattern.search(line)
        if not m:
            continue
        else:
            address.append(m.group(0))
            # print('事件地点：',m.group(0))

    print("事件地点：", set(address))


def shijian(data):
    import jieba

    text = "".join(data)
    text = re.sub(r"[[0-9]*]", " ", text)  # 去除类似[1]，[2]
    text = re.sub(r"\s+", " ", text)  # 用单个空格替换了所有额外的空格
    sentences = re.split("(。|！|\!|\.|？|\?)", text)  # 分句

    # 加载停用词

    def stopwordslist(filepath):
        stopwords = [
            line.strip() for line in open(filepath, "r", encoding="utf-8").readlines()
        ]
        return stopwords

    stopwords = stopwordslist("light_version/cn_stopwords.txt")

    # 词频
    word2count = {}  # line 1
    for word in jieba.cut(text):  # 对整个文本分词
        if word not in stopwords:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())

    # 计算句子得分
    sent2score = {}
    for sentence in sentences:
        for word in jieba.cut(sentence):
            if word in word2count.keys():
                if len(sentence) < 300:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

    # 字典排序
    def dic_order_value_and_get_key(dicts, count):
        # by hellojesson
        # 字典根据value排序，并且获取value排名前几的key
        final_result = []
        # 先对字典排序
        sorted_dic = sorted([(k, v) for k, v in dicts.items()], reverse=True)
        tmp_set = set()  # 定义集合 会去重元素 --此处存在一个问题，成绩相同的会忽略，有待改进
        for item in sorted_dic:
            tmp_set.add(item[1])
        for list_item in sorted(tmp_set, reverse=True)[:count]:
            for dic_item in sorted_dic:
                if dic_item[1] == list_item:
                    final_result.append(dic_item[0])
        return final_result

    # 摘要输出
    final_resul = dic_order_value_and_get_key(sent2score, 5)
    print("事件主要意思：", final_resul)


def main(data):
    pattern_cause(data)
    pattern_lose(data)
    pattern_time(data)
    pattern_address(data)
    shijian(data)


if __name__ == "__main__":
    # 读取数据
    with open("data/bili_content_test2.txt", "r", encoding="utf-8") as f:
        test_data = f.readlines()
    main(test_data)
