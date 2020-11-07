from textblob import TextBlob

print('-'*20, '英文版本')
text = "I am happy today. I feel sad today."
blob = TextBlob(text)
print(blob, 'sentences=', blob.sentences)
for s in blob.sentences:
    print(s.sentiment)
print(blob.sentiment)

print('-'*20, '中文版本')

from snownlp import SnowNLP
text = "我今天很快乐。我今天很愤怒。"
s = SnowNLP(text)
for sentence in s.sentences:
    print(sentence, SnowNLP(sentence).sentiments)
print(s.sentiments)