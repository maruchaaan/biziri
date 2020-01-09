# coding: utf-8
import MeCab
import sys
import re
import csv


output_text=""


    

# Execute bunkai.形態素解析
#　input_text:解析したいテキスト
def mecab_wakati(input_text):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')
    node = mecab.parseToNode(input_text)
    word_class = []

    while node:
        #単語の取得
        word = node.surface
        #　品詞の取得
        wclass = node.feature.split(',')

        #品詞情報ID(動詞,自立など)
        word_id = node.posid

        if wclass[0] != u'BOS/EOS':
            word_class.append([word,word_id,wclass[2],wclass[3],wclass[4],wclass[5],wclass[6],wclass[7],wclass[8]])

        node = node.next
    return word_class

#主語があるとき、主語で尊敬語か謙譲語か丁寧語か判断する
#subject: string 特定された主語
#返り値 (1=尊敬語、2=謙譲語)もしくはfalse
def sub_search(subject):
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/keigo4.csv'
    f = open(csvfile,"r",encoding="utf-8")
    header = next(f)
    for line in f:
        dic = line.split(',')
        if dic[0]==subject: #一致するデータあり
            return dic[1] #1 or 2
    else: f.close()
    return False

#主語特定
#sub_list：主語属性のリスト
def sub_hit(list):
    sub_list = []
    index=0
    for w in list:
        if w[1] == 42 or w[1] == 43 or w[1] == 44 or w[1]==59 or w[1]==38 or w[1]==55:    #人名、代名詞、名詞接尾ならば主語の可能性
            if list[index+1][0] == "が" or list[index+1][0] == "は" or  list[index+1][0] == "も":
                #その次の形態素が「"は"」「"が"」「"も"」ならばそれが主語
                n_subject = sub_search(w[0]) #主語判定
                if w[1]==42 or w[1]==43 or w[1]==44: #人名のみは身内とみなし、謙譲とする。
                    n_subject = 2
                if n_subject != False:
                    sub_list.append(n_subject) #i=1ならば尊敬、i=2ならば謙譲
                else: #keigo4にデータがない場合はfalseが返ってくる。
                    sub_list.append(3) #i=3の丁寧語
        index += 1
    return sub_list

# 動詞を敬語動詞に　行く→伺う、行く→いらっしゃる
# 動詞は主語の属性に応じた変換を行う
#conv_v:敬語変換後の動詞
#word_class_v:変換したい動詞(単語,品詞情報など含む)
#変更点(11/21) i:主語の属性 1=尊敬語、2=謙譲語、その他は3=丁寧語
def verb_conv(word_class_v,i):
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/keigo1.csv'
    with open(csvfile,"r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            dic = line.split(',')
            if dic[0]==word_class_v[6]: #一致するデータあり
                return dic[i]
        else: f.close()
    return False

#動詞活用形の変換 いらっしゃる→いらっしゃり
#v_form:変更後の活用形 連用形など
#v_str:変換前動詞.基本形テキスト
#result:返り値.変更後テキスト
def verb_form(v_form,v_str):
    #print(v_form,v_str)
    result = "verb_form/error"
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/Verb.csv'
    with open(csvfile,"r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== v_str and dic[9]== v_form):
                result = dic[0]
                break
        else: f.close()
    return result

#動詞に活用形「連用タ接続」があるか.どうか.
#verb:調べたい動詞
def td_verb(verb):
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/Verb.csv'
    f = open(csvfile,"r",encoding="utf-8")
    for line in f:
        dic = line.split(',')
        if(dic[10] == verb and dic[9] == "連用タ接続" ):
            return True
    else: f.close()
    return False

#名詞変換
#n_word:変換したい名詞テキスト
#i: 主語の属性 1=尊敬語、2=謙譲語、その他は3=丁寧語
def noun_conv(n_word,i):
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/keigo2.csv'
    f = open(csvfile,"r", encoding="utf-8")
    header = next(f)
    for line in f:
        dic = line.split(',')
        if(dic[0]==n_word): #一致するデータあり
            return dic[i].rstrip('\n')
    else: f.close()
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/keigo3.csv'
    f = open(csvfile,"r",encoding="utf-8")
    for line in f:
        dic = line.split(',')
        if(dic[0]==n_word): #一致するデータあり
            return dic[i].rstrip('\n')
    else: f.close()
    
    return False



#*********以下追加***************************
#美化語の名詞かどうか。美化語の前の所有格で判断する。
#「私の鞄」→「私の鞄」
#「社長の鞄」→「社長のお鞄」
#「鞄」→「（お）鞄」
def noun_bikago(n_word,input_text):
    index=0
    #print(n_word)
    list = mecab_wakati(input_text)
    csvfile = '/Users/k20160322k/Desktop/djangogirls/blog/keigo-bikago.csv'
    f1 = open(csvfile,"r", encoding="utf-8")
    header = next(f1)
    for line in f1:
        dic1 = line.split(',')
        if dic1[0]==n_word: #一致するデータあり
           #print("ok")
           for w in list:
               if list[index-1][0]=="の":#美化語の前に"の"がついているならば
                     f2 = open("keigo4.csv","r", encoding="utf-8")
                     header = next(f2)
                     for line in f2:
                        dic2 = line.split(',')
                        if dic2[0]==list[index-2][0]:#「の」の前がkeigo4.csvに登録されている人名ならば
                            i=dic2[1]
                            i=int(i)
                            return dic1[i].rstrip('\n')#i=1→「お鞄」i=2→「鞄
                     else: f2.close()
                        
               index+=1
           return dic1[3].rstrip('\n')#美化語の前に「〜の」が無ければ「（お）鞄」を返す
    else:f1.close()     
    return False
#*******ここまで********************************
                            

    
               

        
    



def mecab(input_text):
    #input_text:入力
    #input_text="これからすぐ行くね。"
    
    
    list = mecab_wakati(input_text)
    #print(list)

    #output_text:出力
    output_text = ""
    
    sub_atr=sub_hit(list)  #主語の属性値(1,2,3)リスト
    
    index = 0
    for w in list:
        if w[1] == 31 or w[1] == 32 or w[1] == 33: #品詞：動詞の変換
            #print(w[0],w[1])
            conv_v = w[1]
            if not sub_atr: #主語属性リストが空になってしまった場合
                #print("主語属性リストは空になりました\r")
                #print("丁寧語属性を付与します\r")
                sub_atr.append(3)
            i = sub_atr.pop()
            i = int(i)
            if i == 1 or i == 2: #尊敬、謙譲の場合の変換
                v = verb_conv(w,i)
                if v != False: #特殊型変換に該当
                    conv_v = v
                    #print("1")
                    #print(conv_v)
                    minlist = mecab_wakati(conv_v)
                    if len(minlist) != 1: #さらに分解できる語.拝読する.お待ちするなど
                        #print(minlist[-1])
                        s = ""
                        for m in minlist:
                            if m[0] == minlist[-1][0]:
                                #print("3",m[0])
                                conv_v = m[0]
                                break
                            else:
                                #print("4",m[0])
                                output_text += m[0]
                    if w[5]=="基本形":
                        s = verb_form("連用形",conv_v) + "ます"
                        output_text += s
                    else: #基本形以外は元の活用に戻す
                        #後ろの形態素が「た」「て」「だ」「で」だったら、「連用タ接続」
                        if index != (len(list)-1):
                            if ((list[index+1][0] == "た") and (list[index+1][1] == 25)) or \
                            ((list[index+1][0] == "て") and (list[index+1][1] == 18)) or \
                            ((list[index+1][0] == "だ") and (list[index+1][1] == 25)) or \
                            ((list[index+1][0] == "で") and (list[index+1][1] == 18)):
                                #print("ok")
                                if td_verb(conv_v) == True:
                                    output_text += verb_form("連用タ接続",conv_v)
                                else: output_text += verb_form(w[5],conv_v)
                            else: output_text += verb_form(w[5],conv_v)
                        else: output_text += verb_form(w[5],conv_v)
                else: #特殊型変換に該当しない場合.尊敬「お～になる」.謙譲「お（ご）～する」など
                    s = "verb_nonspec/error"
                    if i == 1: #主語属性が尊敬の場合
                        s = "お"+ verb_form("連用形",w[6]) +"に"+ verb_form(w[5],"なる")
                    else:#i=2(謙譲)のとき. #本当は「お(ご)～する」にしたい.今は、ます調にしてるだけ
                        if w[5]=="基本形":
                            s = verb_form("連用形",w[6]) + "ます"
                        else:
                            s = w[0]
                    output_text += s
            else: #i=3で丁寧語の場合
                if w[5] == "基本形":
                    s = verb_form("連用形",w[6]) + "ます"
                    output_text += s
                else: output_text += w[0]
        elif w[1] == 59 or w[1] == 38 or w[1] == 40 or w[1] == 36: #品詞：名詞の変換
            n_word = noun_conv(w[6],2)
            n_bikago = noun_bikago(w[6],input_text)
            #print(n_bikago)
            if n_word != False:
                output_text += n_word
            if n_bikago != False:   #追加
                output_text += n_bikago #追加
                
            else:
                output_text += w[0]

        else: # 動詞、名詞以外
            output_text += w[0]

        index += 1
    #forループ終了
    print(output_text) #出力
    #return output_text
    return output_text
    
    

    




