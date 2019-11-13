import MeCab

def extractKeyword(text):
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)
    keywords = []
    while node:
        if node.feature.split(",")[0] == u"名詞":
            keywords.append(node.surface)
        elif node.feature.split(",")[0] == u"形容詞":
             keywords.append(node.surface)
        elif node.feature.split(",")[0] == u"動詞":
             keywords.append(node.surface)
        node = node.next
    return keywords
text = "pythonでMeCabを使って形態素解析を行う。"
extractKeyword(text)

print(keywords)
