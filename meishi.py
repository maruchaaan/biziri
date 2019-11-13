import MeCab
import sys
import re
from collections import Counter


# パース
mecab = MeCab.Tagger()
parse = mecab.parse("私の好きな食べ物はハンバーグです。母の名前は花子です。")
lines = parse.split('\n')
items = (re.split('[\t,]', line) for line in lines)



# 名詞をリストに格納
words = [item[0]
         for item in items
         if (item[0] not in ('EOS', '', 't', 'ー') and
             item[1] == '名詞' and item[2] == '一般')]

# 頻度順に出力
counter = Counter(words)
for word, count in counter.most_common():
    print(f"{word}: {count}")

    
