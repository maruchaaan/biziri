import MeCab
def result2(request):
    d={
        'comment2': request.GET.get('comment2')
        }


mt = MeCab.Tagger("mecabrc")
str_in=d
res = mt.parseToNode(str_in)
 
dousi=[]
while res:
    arr = res.feature.split(",")
   
    if (arr[0] == "動詞"):
        #動詞の原型を取り出す
        dousi.append(arr[6])
        
    res = res.next

    result2="動詞 ： {}".format(dousi)

  return render(request, 'blog/hoge2.html',result2)
