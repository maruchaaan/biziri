import MeCab


mt = MeCab.Tagger("mecabrc")
str_in="公園を歩く"
res = mt.parseToNode(str_in)
 
dousi=[]
while res:
    arr = res.feature.split(",")
   
    if (arr[0] == "動詞"):
        #動詞の原型を取り出す
        dousi.append(arr[6])
        
    res = res.next
 
result="動詞 ： {}".format(dousi)
print(result)

