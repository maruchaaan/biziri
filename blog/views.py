# coding: utf-8
# from natto import MeCab

from django.shortcuts import render
from django.utils import timezone
from .models import Sentence
from .forms import SentenceForm
from django.shortcuts import redirect
import sys,os
import MeCab
import re
import csv
import sys
import json
from blog import mecab_test9
from blog import Text_input


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

from django.shortcuts import render, get_object_or_404
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#初期画面
def apphoge(request):
    return render(request,'blog/hogera.html')

##new1からもう一度敬語翻訳やる時
def write(request):
    request.session.clear()
    return render(request, 'blog/hoge2.html')

##data_sentence_output.txt:出力文一覧が入ってる

def result2(request):
    input_text = request.GET.get('user_input_text')

        #入力文エラー確認の際
        #Ti = Text_input.Text_check(self.input_text)
        #check = Ti.input_check2() #True or False
        #if check == True:
            #return redirect()
        #else:
            #error_message = "半角文字が含まれてます。全角で入力してください。")

    """if request.method == 'POST':
        if 's_index' in request.session and 'input_text' in request.session:
            s_index = request.session['s_index']
            s_index = int(s_index) + 1
            input_text = request.session['input_text']
            output_text = request.session['output_text']

            del request.session['s_index'] #セッション削除
            request.session['s_index'] = s_index

        else: #エラー初期画面へ
            return render(request,'blog/hogera.html')"""

    Trs = mecab_test9.TextTrans(input_text)
    print(mecab_test9.verb_count(Trs.mecab_list))

    if Sentence.objects.exists():
        #一番最近登録したobjのSentence_IDを取得
        lst = Sentence.objects.last()
        now_id = lst.sentence_id + 1
        print(now_id)
    else:
        now_id = 1

    s_index = -1 #Text_index.Pointer:初期値-1
    request.session['now_id'] = now_id #現在翻訳中の文のSentence_IDをセッションに保存

    a = 0
    for w in Trs.mecab_list: #DBに文情報を登録
        st = Sentence(sentence_id=now_id,text=input_text,word=w[6],
        word_id=w[1],Text_index=a)
        st.save()
        a += 1

    #自立動詞id=31かつs_index(Pointer)<text_indexのobjを取得
    query = Sentence.objects.filter(sentence_id=now_id,word_id=31,
    Text_index__gt=s_index).first()

    if query is None: #該当する動詞がない場合.
        query_set = Sentence.objects.filter(sentence_id=now_id)
        trans_wlist = []
        for q in query_set:
            if q.trans_word is None:
                trans_wlist.append("")
            else:
                trans_wlist.append(q.trans_word)
        print(trans_wlist)

        Trs = mecab_test9.TextTrans(input_text)
        output_text = Trs.text_trans(trans_wlist)

        with open('data_sentence_output.txt','a',encoding="utf-8") as f:
            f.write(output_text+'\n')

        return render(request,'blog/new1.html',{'comment2':output_text}) #翻訳文表示画面へ
    else: #動詞あり
        v_word = query.word
        print(query.Text_index)
        request.session['s_index'] = query.Text_index #Pointer
        word = Trs.mecab_list[query.Text_index][0]
        deta = {
        'input_text':input_text,
        'comment2':v_word,
        'word':word,
        }
        return render(request, 'blog/hoge3.html', deta) #主語を聞く画面(hoge3.html)へ

  ###############一覧を出す(new2.html)######################################
def end(request):
 if request.method =='POST':
    with open('data_sentence_output.txt','r',encoding="utf-8") as f:
        data3 = f.read()
    ##print("敬語翻訳した文一覧:"+"\n"+data3)
    return render(request, 'blog/new2.html',{'comment3':data3})#htmlに送る時、data3をcomment3とおく{{comment3}}

  ######追加　はじめる　ボタンで　一覧をリセットクリア#############
def delete2(request):
    request.session.clear()
    if request.method == 'POST':
        with open('data_sentence_output.txt','w',encoding="utf-8") as f:
            f.write("")
    return render(request, 'blog/hoge2.html')

    ###########主語を選んだ後#############
def vote(request):
    if request.method =='GET':
        q1 = request.GET.get('q1')
        print(q1)
    s_index = request.session['s_index']#Pointer取得
    now_id = request.session['now_id']

    #データベースに属性値登録
    query = Sentence.objects.filter(sentence_id=now_id,word_id=31,
    Text_index=s_index).first()
    q1 = int(q1)
    query.atr = q1
    query.save()

    #候補だし
    Trs = mecab_test9.TextTrans(query.text)
    Trs.set_pointer(s_index)
    v_candidate_list = Trs.verb31_trans(q1,query.word)
    print(v_candidate_list)
    request.session['v_candidate_list'] = v_candidate_list
    word = Trs.mecab_list[s_index][0]
    print("word="+word)

    if len(v_candidate_list) > 1: #複数候補
        json.dumps(v_candidate_list)
        deta = {
        'input_text':query.text,
        'v_list':v_candidate_list,
        'word': word,
        'word_kihon': query.word
        }
        return render(request, 'blog/hoge4.html',deta) #候補選択画面へ

    else: #候補1つのみだったら、次の動詞探索
        query.trans_word = v_candidate_list[0]
        query.save() #DBに決定した敬語動詞を保存

        query2 = Sentence.objects.filter(sentence_id=now_id,word_id=31,
        Text_index__gt=s_index).first()
        if query2 is None: #該当する動詞がない場合.
            query_set = Sentence.objects.filter(sentence_id=now_id)
            trans_wlist = []
            for q in query_set:
                if q.trans_word is None:
                    trans_wlist.append("")
                else:
                    trans_wlist.append(q.trans_word)
            print(trans_wlist)

            Trs = mecab_test9.TextTrans(query.text)
            output_text = Trs.text_trans(trans_wlist)

            with open('data_sentence_output.txt','a',encoding="utf-8") as f:
                f.write(output_text+'\n')

            return render(request,'blog/new1.html',{'comment2':output_text}) #翻訳文表示画面へ

        else: #他に動詞あり
            v_word = query2.word
            request.session['s_index'] = query2.Text_index #Pointer
            word = Trs.mecab_list[query2.Text_index][0]

            deta = {
            'input_text':query2.text,
            'comment2':v_word,
            'word':word,
            }
            return render(request, 'blog/hoge3.html', deta) #主語を聞く画面(hoge3.html)へ

def kouho(request):
    if request.method =='GET':
        kouhoname = request.GET.get('kouhoname') #数字データ(選択肢)受け取り

    s_index = request.session['s_index']#Pointer取得
    now_id = request.session['now_id']
    v_candidate_list = request.session['v_candidate_list'] #候補取得
    del request.session['v_candidate_list']

    #変換敬語動詞決定.
    query = Sentence.objects.filter(sentence_id=now_id,word_id=31,
    Text_index=s_index).first()
    kouhoname = int(kouhoname)
    query.trans_word = v_candidate_list[kouhoname-1]
    query.save() #DBに決定した敬語動詞を保存

    #自立動詞id=31かつs_index(Pointer)<text_indexのobjを取得
    query2 = Sentence.objects.filter(sentence_id=now_id,word_id=31,
    Text_index__gt=s_index).first()
    if query2 is None: #該当する動詞がない場合.
        query_set = Sentence.objects.filter(sentence_id=now_id)
        trans_wlist = []
        for q in query_set:
            if q.trans_word is None:
                trans_wlist.append("")
            else:
                trans_wlist.append(q.trans_word)
        print(trans_wlist)

        Trs = mecab_test9.TextTrans(query.text)
        output_text = Trs.text_trans(trans_wlist)

        with open('data_sentence_output.txt','a',encoding="utf-8") as f:
            f.write(output_text+'\n')

        return render(request,'blog/new1.html',{'comment2':output_text}) #翻訳文表示画面へ

    else: #動詞あり #主語を聞く画面(hoge3.html)へ
        v_word = query2.word
        request.session['s_index'] = query2.Text_index #Pointer
        Trs = mecab_test9.TextTrans(query2.text)
        word = Trs.mecab_list[query2.Text_index][0]

        deta = {
        'input_text':query2.text,
        'comment2':v_word,
        'word':word
        }
        return render(request, 'blog/hoge3.html', deta)
