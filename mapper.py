#!/home/clementime/bin/python
import sys
import jieba

for line in sys.stdin:
    l = line.strip()
    words = jieba.cut(l)
    for word in words:
        print(word)

