# coding: utf-8
import MeCab
import sys
import re
import csv
import os
from blog import Text_input

#ファイルパス.ここだけ自分のパスに変更してください.
path = "C:/Users/Mizuki/biziri/blog/"

class TextTrans:

    def __init__(self, input_text):
        Ti = Text_input.Text_check(input_text) #入力文の整形
        self.input_text = Ti.input_check1()
        self.mecab_list = mecab_wakati(self.input_text) #形態素解析

    def set_pointer(self,index):
        index = int(index)
        self.s_index = index

    #return:変換候補リスト
    def verb31_trans(self,atr,word_v):
        w = self.mecab_list[self.s_index]
        if atr == 1: #尊敬の場合の変換
            v_list = verb_conv(word_v,atr)
            if v_list == False: #尊敬.特殊型に該当しない.一般型
                s = "verb_nonspec/error"
                nonspe_list =[] #一般型動詞候補リスト
                s1 = "お"+ verb_form("連用形",w[6]) +"に"
                conv_v1 = "なる"
                nonspe_list.append(s1+conv_v1) #候補1
                s2 = ""
                conv_v2 = ""
                if w[4].startswith('五段'):
                    s2 = verb_form("未然形",w[6])
                    conv_v2 = "れる" #「れる」五段、サ変動詞の未然形に接続
                elif w[4].startswith('サ変'):
                    s2 = verb_form_henkaku(w[4],"未然形",w[6])
                    conv_v2 = "れる" #「れる」
                else: #「られる」上一段・下一段・カ変動詞の未然形に接続
                    s2 = verb_form("未然形",w[6])
                    conv_v2 = "られる"
                nonspe_list.append(s2+conv_v2) #候補2
                return nonspe_list
            else: return v_list

        elif atr == 2: #謙譲の場合の変換
            v_list = verb_conv(word_v,atr)
            if v_list == False:   #謙譲.特殊型に該当しない.一般型
                s = "verb_nonspec/error"
                nonspe_list =[] #一般型動詞候補リスト
                s1 = "お"+ verb_form("連用形",w[6])
                conv_v1 = "いたす"
                nonspe_list.append(s1+conv_v1) #候補1
                s2 = "お"+verb_form("連用形",w[6])
                conv_v2 = "する"
                nonspe_list.append(s2+conv_v2) #候補2
                s3 = ""
                conv_v3 = w[6]
                nonspe_list.append(s3+conv_v3) #候補3
                return nonspe_list
            else: return v_list

        else: #丁寧の場合
            v_list = [word_v] #元の基本形
            return v_list

    def not_change(self, word):
        #変換を行わない例外動詞の処理
        index = self.s_index
        list = self.mecab_list
        if list[index+1][1] == 32 and list[index+1][6] == "れる": #受け身、尊敬、可能、自発
            return True
        if list[index+1][1] == 32 and list[index+1][6] == "られる": #受け身、尊敬、可能、自発
            return True
        if list[index+1][1] == 32 and list[index+1][6] == "せる": #使役
            if w[1] == 31 and w[0] == "さ" and w[4] == "サ変・スル": #させるで1セット
                return True
        return False

    #return:output_text(出力文)
    #引数:trans_wlist 変換敬語動詞のリスト(対象以外は空文字)
    def text_trans(self, trans_wlist):
        print(self.input_text)
        list = self.mecab_list
        print(list)
        output_text = ""
        index = 0

        for w in list:
            if w[1] == 31:#品詞：自立動詞の変換
                print(w[0],w[1],w[4],w[8])
                conv_v = w[6] #その語の基本形.「行く」など
                text = ""

                #変換を行わない例外動詞の処理
                if list[index+1][1] == 32 and list[index+1][6] == "れる": #受け身、尊敬、可能、自発
                    output_text += w[0]
                    index += 1
                    continue
                if list[index+1][1] == 32 and list[index+1][6] == "られる": #受け身、尊敬、可能、自発
                    output_text += w[0]
                    index += 1
                    continue
                if list[index+1][1] == 32 and list[index+1][6] == "せる": #使役
                    if w[1] == 31 and w[0] == "さ" and w[4] == "サ変・スル": #させるで1セット
                        output_text += w[0]
                        index += 1
                        continue

                conv_v = trans_wlist[index]
                minlist = mecab_wakati(conv_v)
                if len(minlist) != 1: #さらに分解できる語.拝読する.お待ちになるなど
                        for m in minlist:
                            if m[0] == minlist[-1][0]:
                                conv_v = m[0]
                                break
                            else:
                                text += m[0]
                else: pass

                print("変換語尾:"+conv_v) #変換語尾の確認
                print("listの長さ:"+str(len(list)))

                #語尾の処理
                if w[5]=="基本形" and list[index+1][8] != "名詞" : #後ろが名詞(＝動詞が連体形)でないときは”ます”つける
                    if w[4].startswith('サ変') or w[4].startswith('カ変'):
                        s = verb_form_henkaku(w[4],"連用形",conv_v) + "ます"
                    elif conv_v == "する":
                        s = verb_form_henkaku("サ変・スル","連用形",conv_v) + "ます"
                    else:
                        s = verb_form("連用形",conv_v) + "ます"
                    text += s

                else: #基本形以外は元の活用に戻す
                    #後ろの形態素が「だ。」「た。」だったら、「連用形」
                    if ((list[index+1][6] == "た") and (list[index+1][1] == 25) and (list[index+1][4] == "特殊・タ")) or \
                    ((list[index+1][6] == "だ") and (list[index+1][1] == 25) and (list[index+1][4] == "特殊・タ")):
                        if list[index+2][0] == "。": #文末
                            s = verb_form("連用形",conv_v) + auxil_form("連用形","ます")
                        #elif w[4].startswith('サ変') or w[4].startswith('カ変'):
                            #s = verb_form_henkaku(w[4],"連用形",conv_v) + auxil_form("連用形","ます")
                        elif conv_v == "する":
                            s = verb_form_henkaku("サ変・スル","連用形",conv_v) + auxil_form("連用形","ます")
                        elif td_verb(conv_v) == True:
                            s = verb_form("連用タ接続",conv_v)
                        else:
                            s = verb_form("連用形",conv_v)
                        text +=s

                    #後ろの形態素が「て」「で」だったら、「連用タ接続」
                    elif ((list[index+1][0] == "て") and (list[index+1][1] == 18)) or \
                    ((list[index+1][0] == "で") and (list[index+1][1] == 18)):
                        if conv_v == "する":
                            s = verb_form_henkaku("サ変・スル","連用形",conv_v) #=元の文のまま
                            text += s
                        elif td_verb(conv_v) == True:
                            text += verb_form("連用タ接続",conv_v)
                        else: #連用タ接続がない動詞
                            if w[5] == "連用タ接続": #変換前が連用タ接続の動詞.かつ変換後に連用タ接続がない場合.
                                text += verb_form("連用形",conv_v)
                            else: text += verb_form(w[5],conv_v)

                    #後ろの形態素が助動詞「ない」「動詞(連用形)＋ませ＋ん」
                    elif list[index+1][1] == 25 and list[index+1][6] == "ない" and list[index+2][8] != "名詞":
                        text += verb_form("連用形",conv_v)
                    else:
                        if conv_v == "する":
                            if w[5] == "未然形": #未然形「し」「さ」「せ」の3パターンの場合わけ
                                if (list[index+1][6] == "ない" and list[index+1][1] == 25):
                                    s = verb_form_henkaku("サ変・スル",w[5],conv_v)
                                elif list[index+1][6] == "せる" or list[index+1][6] == "れる":
                                    s = verb_form_henkaku("サ変・スル","未然レル接続",conv_v)
                                else:
                                    s = verb_form_henkaku("サ変・スル","未然ヌ接続",conv_v)
                            else:
                                s = verb_form_henkaku("サ変・スル",w[5],conv_v)
                            text += s
                        else: text += verb_form(w[5],conv_v)

                output_text += text #動詞変換完了

            elif w[1] == 32 or w[1] == 33: #非自立動詞の変換
                conv_v = w[6] #その語の基本形.
                text = ""
                if w[5]=="基本形" and list[index+1][8] != "名詞" : #後ろが名詞(＝動詞が連体形)でないときは”ます”つける
                    if (w[4].startswith('サ変') or w[4].startswith('カ変')):
                        text += verb_form_henkaku(w[4],"連用形",conv_v) + "ます"
                    elif w[1] == 32 and w[6] == "せる":
                        text += verb_form_henkaku(w[4],"連用形",conv_v) + "ます"
                    else:
                        text += verb_form("連用形",conv_v) + "ます"

                else: #基本形以外は元の活用に戻す
                    #print("次のわかち:"+list[index+1][0],list[index+1][1],index)

                    #後ろの形態素が完了・過去「だ」「た」だったら、「連用形」
                    if (list[index+1][0] == "た" and list[index+1][1] == 25) or \
                    (list[index+1][0] == "だ" and list[index+1][1] == 25):
                        if (w[4].startswith('サ変') or w[4].startswith('カ変')):
                            text += verb_form_henkaku(w[4],"連用形",conv_v) + auxil_form("連用形","ます")
                        elif w[1] == 32 and w[6] == "せる":
                            text += verb_form_henkaku(w[4],"連用形",conv_v) + auxil_form("連用形","ます")
                        else:
                            text += verb_form("連用形",conv_v) + auxil_form("連用形","ます")

                    #後ろの形態素が「て」「で」
                    elif ((list[index+1][0] == "て") and (list[index+1][1] == 18)) or \
                    ((list[index+1][0] == "で") and (list[index+1][1] == 18)):
                        if td_verb(conv_v) == True:
                            text += verb_form(w[5],conv_v) #非自立動詞は連用タ接続しないのでは.→もとの活用でよい
                        elif w[1] == 32 and w[6] == "せる":
                            text += verb_form_henkaku(w[4],"連用形",conv_v)
                        else: text += verb_form(w[5],conv_v)

                    #後ろの形態素が助動詞「ない」「動詞(連用形)＋ませ＋ん」
                    elif list[index+1][1] == 25 and list[index+1][6] == "ない" and list[index+2][8] != "名詞":
                        text += verb_form("連用形",conv_V)

                    else: text += verb_form(w[5],conv_v)

                output_text += text #非自立動詞変換完了

            elif w[1] == 25: #品詞：助動詞の変換 (list[index-1][1] != 31 or list[index-1][1] != 32 or list[index-1][1] != 33)
                if w[0] == "だ":
                    if list[index-1][5][:2] == "連用": #過去、完了、存続、自発の「だ」の場合
                        if list[index+1][0] == "。": #文末「まし＋た」
                            output_text += "た"
                        else: output_text += "だ"
                    else: #断定の助動詞の「だ」の場合
                        output_text += "です"

                elif w[0] == "ない" and list[index+1][8] != "名詞": #動詞の否定
                    output_text += (auxil_form("未然形","ます") + "ん")
                else:
                    output_text += w[0]

            elif w[1] == 10 or w[1] == 11 or w[1] == 12: #品詞：形容詞が語尾の場合→　＋「です」を付与
                if list[index+1][0] == "。": #ID=7「句点（。）」
                    output_text += (w[0]+"です")
                else:
                    output_text += w[0]

            elif w[1] == 59 or w[1] == 38 or w[1] == 36: #品詞：名詞の変換
                output_text += w[0]
                """n_word = noun_conv(w[6],2)
                if n_word != False:
                    i = 3
                    print(w[0]+":","客先もしくは上司の"+w[0]+"ですか？ (Yes/No)")
                    u_answer = input(">>>>>")
                    if u_answer == "Yes": #尊敬語
                        i = 1
                    else:
                        print(w[0]+":","自分もしくは自社の"+w[0]+"ですか？　(Yes/No)")
                        u_answer = input(">>>>>")
                        if u_answer == "Yes": #謙譲語
                            i = 2
                        else: #丁寧語
                            i = 3
                    n_word = noun_conv(w[6],i)
                    output_text +=  n_word
                else: #keigo2、keigo3にデータなし.特殊変換がない名詞の場合
                    n_word = noun_bikago(w[0],input_text)
                    if n_word != False:
                        output_text += n_word
                    else: #Falseの場合
                        output_text += w[0]"""

            else: # 動詞(自立、非自立)、名詞、助動詞以外
                output_text += w[0]

            index += 1

        #forループ終了
        return output_text

#形態素解析
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
            try:
                word_class.append([word,word_id,wclass[2],wclass[3],wclass[4],wclass[5],wclass[6],wclass[7],wclass[0]])
            except IndexError as e:
                word_class.append([word,word_id,'＊','＊','＊','＊','＊','＊',wclass[0]])
                print(e)
                print(word,"誤字である可能性が高いです。")

        node = node.next
    return word_class

# 動詞を敬語動詞に　行く→伺う、行く→いらっしゃる
# 動詞は主語の属性に応じた変換を行う.特殊変換
#conv_v:敬語変換後の動詞
#word_v:変換したい動詞(基本形)
#変更点(11/21) i:主語の属性 1=尊敬語、2=謙譲語
#return Folse or list
def verb_conv(word_v,i):
    v_candidate = []
    with open(path+"keigo1.csv","r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            dic = line.split(',')
            if dic[0]==word_v: #一致するデータあり
                vc_flag = False
                for v in v_candidate:
                    if v == dic[i]:
                        vc_flag = True #既出の敬語
                    else: continue
                if vc_flag == False: #被ってなかった場合、追加
                    v_candidate.append(dic[i])
    if not v_candidate: #データがなかった場合
        return False
    else:
        return v_candidate

#動詞活用形の変換 いらっしゃる→いらっしゃり
#v_form:変更後の活用形 連用形など
#v_str:変換前動詞.基本形テキスト
#result:返り値.変更後テキスト
def verb_form(v_form,v_str):
    result = "verb_form/error"
    #print(v_form,v_str)
    with open(path+"Verb.csv","r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== v_str and dic[9]== v_form):
                result = dic[0]
                break
    if(result == "verb_form/error"): #活用変換が辞書にないとき
        #v = v_form[:2] + "形"
        #result = verb_form(v,v_str)
        print(v_form,v_str,result)
        result == v_str
    return result

#変格活用のときの変換（サ変、カ変)
#v_spe:活用形の種類
#v_form:変更後の活用形 連用形など
#v_str:変換前動詞.基本形テキスト
def verb_form_henkaku(v_spe,v_form,v_str):
    result = "verb_form_henkaku:error"
    with open(path+"Verb.csv","r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== v_str and dic[9]== v_form and dic[8]==v_spe):
                result = dic[0]
                break
    
    if (result == "verb_form_henkaku:error"):
        with open(path+"Verb.csv","r",encoding="utf-8") as f:
            for line in f:
                dic = line.split(',')
                if (dic[10]== v_str and dic[9]== v_form):
                    result = dic[0]
                    break
    return result

#動詞に活用形「連用タ接続」があるか.どうか.
#verb:調べたい動詞
def td_verb(verb):
    f = open(path+"Verb.csv","r",encoding="utf-8")
    for line in f:
        dic = line.split(',')
        if(dic[10] == verb and dic[9] == "連用タ接続" ):
            return True
    else: f.close()
    return False

#助動詞活用形の変換 基本形ます→連用形まし
#a_form:変更後の活用形 連用形など
#a_str:変換前動詞.基本形テキスト
#result:返り値.変更後テキスト
def auxil_form(a_form,a_str):
    result = "a_form/error"
    with open(path+"Auxil.csv","r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== a_str and dic[9]== a_form):
                result = dic[0]
                break
    return result

#名詞変換
#n_word:変換したい名詞テキスト
#i: 主語の属性 1=尊敬語、2=謙譲語、その他は3=丁寧語
def noun_conv(n_word,i):
    f = open(path+"keigo2.csv","r", encoding="utf-8")
    header = next(f)
    for line in f:
        dic = line.split(',')
        if(dic[0]==n_word): #一致するデータあり
            return dic[i].rstrip('\n')
    else: f.close()
    f = open(path+"keigo3.csv","r",encoding="utf-8")
    for line in f:
        dic = line.split(',')
        if(dic[0]==n_word): #一致するデータあり
            return dic[i].rstrip('\n')
    else: f.close()
    return False

#美化語の名詞かどうか。美化語の前の所有格で判断する。
#「私の鞄」→「私の鞄」
#「社長の鞄」→「社長のお鞄」
#「鞄」→「（お）鞄」
def noun_bikago(n_word,input_text):
    index=0
    print(n_word)
    list = mecab_wakati(input_text)
    f1 = open(path+"keigo-bikago.csv","r", encoding="utf-8")
    header = next(f1)
    for line in f1:
        dic1 = line.split(',')
        if dic1[0]==n_word: #一致するデータあり
           print("ok")
           for w in list:
               if list[index-1][0]=="の":#美化語の前に"の"がついているならば
                     f2 = open(path+"keigo4.csv","r", encoding="utf-8")
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

def verb_count(list):
    vcount = 0
    for w in list:
        if w[1] == 31:
            vcount += 1
        else: pass
    return vcount

def main():
    input_text=input("敬語に変換したい文章＞＞")
    TT = TextTrans(input_text)
    output_text = TT.text_trans()
    print("出力文："+output_text)

if __name__ == '__main__':
    main()
