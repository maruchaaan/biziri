import MeCab

mt = MeCab.Tagger("mecabrc")
data="私の好きな食べ物はハンバーグです。今朝、犬と散歩をした。楽しかった。"
str_in=data
res = mt.parseToNode(str_in)
 
dousi=[]
while res:
    arr = res.feature.split(",")
   
    if (arr[0] == "動詞"):
        #動詞の原型を取り出す
        dousi.append(arr[6])
        
    res = res.next
 

print("動詞 ： {}".format(dousi))