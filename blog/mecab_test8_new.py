# coding: utf-8
import MeCab
import sys
import re
import csv
from blog import Text_input

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
            try:
                word_class.append([word,word_id,wclass[2],wclass[3],wclass[4],wclass[5],wclass[6],wclass[7],wclass[0]])
            except IndexError as e:
                word_class.append([word,word_id,'＊','＊','＊','＊','＊','＊',wclass[0]])
               ## print(e)
               ## print(word,"誤字である可能性が高いです。")

        node = node.next
    return word_class

def sub_request(list):
    #自立動詞の数だけ動作主をリクエストする
    v_count = 0 #動詞カウント
    index = 0
    sub_list = {} #主語属性のリスト[key(index):value(1 or  2 or 3)]
    for w in list:
        if w[1] == 31:
            v_count += 1
            ##print(w[0],"この動詞の主語は客先や上司ですか？ (Yes/No)")

            u_answer = input(">>>>>")
            if u_answer == "Yes": #尊敬語
                sub_list[index] = 1
            else:
                ##print(w[0],"この動詞の主語は自分もしくは自社ですか？　(Yes/No)")
                u_answer = input(">>>>>")
                if u_answer == "Yes": #謙譲語
                    sub_list[index] = 2
                else: #丁寧語
                    sub_list[index] = 3
        else:
            index += 1
            continue

        index += 1
    #forループ終了
    return sub_list


#主語があるとき、主語で尊敬語か謙譲語か丁寧語か判断する
#subject: string 特定された主語
#返り値 (1=尊敬語、2=謙譲語)もしくはfalse
def sub_search(subject):
    csvfile='blog/keigo4.csv'
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
# 動詞は主語の属性に応じた変換を行う.特殊変換
#conv_v:敬語変換後の動詞
#word_class_v:変換したい動詞(単語,品詞情報など含む)
#変更点(11/21) i:主語の属性 1=尊敬語、2=謙譲語、その他は3=丁寧語
def verb_conv(word_class_v,i):
    v_candidate = []
    csvfile = 'blog/keigo1.csv'
    with open(csvfile,"r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            dic = line.split(',')
            if dic[0]==word_class_v[6]: #一致するデータあり
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
    csvfile = 'blog/Verb.csv'
    #print(v_form,v_str)
    with open(csvfile,"r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== v_str and dic[9]== v_form):
                result = dic[0]
                break
    if(result == "verb_form/error"): #活用変換が辞書にないとき
        #v = v_form[:2] + "形"
        #result = verb_form(v,v_str)
        ##print(v_form,v_str,result)
        result == v_str
    return result

#変格活用のときの変換（サ変、カ変)
#v_spe:活用形の種類
#v_form:変更後の活用形 連用形など
#v_str:変換前動詞.基本形テキスト
def verb_form_henkaku(v_spe,v_form,v_str):
    result = "verb_form_henkaku:error"
    csvfile = 'blog/Verb.csv'
    with open(csvfile,"r",encoding="utf-8") as f:
        for line in f:
            dic = line.split(',')
            if (dic[10]== v_str and dic[9]== v_form and dic[8]==v_spe):
                result = dic[0]
                break
    return result

#動詞に活用形「連用タ接続」があるか.どうか.
#verb:調べたい動詞
def td_verb(verb):
    csvfile = 'blog/Verb.csv'
    f = open(csvfile,"r",encoding="utf-8")
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
    csvfile = 'blog/Auxil.csv'
    with open(csvfile,"r",encoding="utf-8") as f:
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
    csvfile = 'blog/keigo2.csv'
    f = open(csvfile,"r", encoding="utf-8")
    header = next(f)
    for line in f:
        dic = line.split(',')
        if(dic[0]==n_word): #一致するデータあり
            return dic[i].rstrip('\n')
    else: f.close()
    csvfile = 'blog/keigo3.csv'
    f = open(csvfile,"r",encoding="utf-8")
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
    ##print(n_word)
    list = mecab_wakati(input_text)
    csvfile = 'blog/keigo-bikago.csv'
    f1 = open(csvfile,"r", encoding="utf-8")
    header = next(f1)
    for line in f1:
        dic1 = line.split(',')
        if dic1[0]==n_word: #一致するデータあり
           ##print("ok")
           for w in list:
               if list[index-1][0]=="の":#美化語の前に"の"がついているならば
                     f2 = open("blog/keigo4.csv","r", encoding="utf-8")
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

#input_text:入力
def mecab(input_text):

    ##print(input_text)
    Ti = Text_input.Text_check(input_text) #文の整形
    input_text = Ti.input_check1()
    list = mecab_wakati(input_text)

    #output_text:出力
    output_text = ""

    sub_atr = sub_request(list) #[key(index):value]
    #sub_atr=sub_hit(list)  #主語の属性値(1,2,3)リスト

    index = 0
    for w in list:
        ##print(w[1])
        if w[1] == 31:#品詞：自立動詞の変換
        #############追加(入力動詞抽出)##
            f=open("data_sentence2.txt","a",encoding="utf-8")
            f.write(w[0]+"\n")
            f.close()
       ############################
            ##print(w[0],w[1],w[4],w[8])
            conv_v = w[6] #その語の基本形.「行く」など
            #i = sub_atr.pop()
            ##print(w[0],"i="+str(sub_atr.get(index,3)))
            i = int(sub_atr.get(index,3))
            i = int(i)

            verb_flag = False #特殊変換をしたか否か
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

            if i == 1: #尊敬の場合の変換
                v_list = verb_conv(w,i)
                if v_list != False: #尊敬.特殊型変換に該当
                    if len(v_list) > 1: #候補が２つ以上のとき
                        ##print("候補が"+str(len(v_list))+"個あります。")
                        g=open("data_kouho_num.txt","a",encoding="utf-8")##追加　候補数
                        g.write(str(len(v_list)))##追加
                        g.close()##追加
                        for p in range(len(v_list)):
                            select_num = p + 1
                           ##print(str(select_num) +": "+ str(v_list[p]))
                            ####################################
                            h=open("data_kouho.txt","a",encoding="utf-8")##追加　候補
                            h.write(str(select_num) +": "+ str(v_list[p]))##追加
                            h.close()##追加

       ############################

                        u_answer = input("数字(半角で入力)>>>>>")
                        for p in range(len(v_list)):
                            if int(u_answer) == (p+1):
                                conv_v = v_list[p]
                                break
                            else: continue
                    else:
                        conv_v = v_list[0]

                    verb_flag = True
                    ##print("i=1",conv_v)
                    minlist = mecab_wakati(conv_v)
                    if len(minlist) != 1: #さらに分解できる語.拝読する.お待ちするなど
                        for m in minlist:
                            if m[0] == minlist[-1][0]:
                                conv_v = m[0]
                                break
                            else:
                                text += m[0]
                else: #特殊型変換に該当しない場合.尊敬「お～になる」or「～れる」「～られる」v_list==False
                    s = "verb_nonspec/error"

                    ##print("候補が2個あります。")
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

                    for p in range(len(nonspe_list)): #選択肢表示
                        select_num = p + 1
                        ##print(str(select_num) +": "+ str(nonspe_list[p]))

                    u_answer = input("数字(半角で入力)>>>>>")
                    if u_answer=="1":
                        s = s1
                        conv_v = conv_v1
                    if u_answer=="2":
                        s = s2
                        conv_v = conv_v2

                    text += s

            elif i==2: #謙譲語(i=2)の場合の変換
                v_list = verb_conv(w,i)
                if v_list != False:  #謙譲.特殊型変換に該当
                    if len(v_list) > 1: #候補が2つ以上あるとき
                        ##print("候補が"+str(len(v_list))+"個あります。")
                        for p in range(len(v_list)):
                            select_num = p + 1
                           ## print(str(select_num) +": "+ str(v_list[p]))
                        u_answer = input("数字(半角で入力)>>>>>")
                        for p in range(len(v_list)):
                            if int(u_answer) == (p+1):
                                conv_v = v_list[p]
                                break
                            else: continue
                    else:
                        conv_v = v_list[0]

                    verb_flag = True
                    ##print("i=2",conv_v)
                    minlist = mecab_wakati(conv_v)

                    if len(minlist) != 1: #さらに分解できる語.拝読する.お待ちするなど
                        s = ""
                        for m in minlist:
                            if m[0] == minlist[-1][0]:
                                conv_v = m[0]
                                break
                            else:
                                text += m[0]
                else: #謙譲.特殊変換に該当しない場合.一般型「お～いたす」？「お(ご)～する」？
                    s = "verb_nonspec/error"

                   ## print("候補が3個あります。")
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

                    for p in range(len(nonspe_list)): #選択肢表示
                        select_num = p + 1
                        ##print(str(select_num) +": "+ str(nonspe_list[p]))

                    u_answer = input("数字(半角で入力)>>>>>")
                    if u_answer=="1":
                        s = s1
                        conv_v = conv_v1
                    if u_answer=="2":
                        s = s2
                        conv_v = conv_v2
                    if u_answer=="3":
                        s = s3
                        conv_v = conv_v3

                    text += s
            else: #丁寧語（i=3）の場合は、処理しない
                pass

            #語尾の処理
            if w[5]=="基本形" and list[index+1][8] != "名詞" : #後ろが名詞(＝動詞が連体形)でないときは”ます”つける
                if verb_flag ==False and (w[4].startswith('サ変') or w[4].startswith('カ変')):
                    s = verb_form_henkaku(w[4],"連用形",conv_v) + "ます"
                elif conv_v == "する": #verb_flag == True and
                    s = verb_form_henkaku("サ変・スル","連用形",conv_v) + "ます"
                else:
                    s = verb_form("連用形",conv_v) + "ます"
                text += s

            else: #基本形以外は元の活用に戻す
                #後ろの形態素が「だ。」「た。」だったら、「連用形」
                if ((list[index+1][0] == "た") and (list[index+1][1] == 25)) or \
                ((list[index+1][0] == "だ") and (list[index+1][1] == 25)):
                    if verb_flag ==False and (w[4].startswith('サ変') or w[4].startswith('カ変')):
                        s = verb_form_henkaku(w[4],"連用形",conv_v) + auxil_form("連用形","ます")
                    elif conv_v == "する": #verb_flag == True and
                        s = verb_form_henkaku("サ変・スル","連用形",conv_v) + auxil_form("連用形","ます")
                    else:
                        s = verb_form("連用形",conv_v) + auxil_form("連用形","ます")
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
                else:
                    if conv_v == "する":
                        if(w[5] == "未然形"): #未然形「し」「せ」「さ」
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
            #print(w[0],w[1],w[4],w[8])
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
                else: text += verb_form(w[5],conv_v)

            output_text += text #非自立動詞変換完了

        elif w[1] == 25: #品詞：助動詞の変換 (list[index-1][1] != 31 or list[index-1][1] != 32 or list[index-1][1] != 33)
            if w[0] == "だ":
                if list[index-1][5][:2] == "連用": #過去、完了、存続、自発の「だ」の場合
                    output_text += "た"
                else: #断定の助動詞の「だ」の場合
                    output_text += "です"
            else:
                output_text += w[0]

        elif w[1] == 10 or w[1] == 11 or w[1] == 12: #品詞：形容詞が語尾の場合→　＋「です」を付与
            if list[index+1][1] == 7: #ID=7「句点（。）」
                output_text += (w[0]+"です")
            else:
                output_text += w[0] #そのまま

        elif w[1] == 59 or w[1] == 38 or w[1] == 36: #品詞：名詞の変換

            n_word = noun_conv(w[6],2)
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
                    output_text += w[0]

        else: # 動詞(自立、非自立)、名詞、助動詞以外
            output_text += w[0]

        index += 1

    #forループ終了
    return output_text
