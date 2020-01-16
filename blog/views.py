# coding: utf-8
# from natto import MeCab

from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import sys,os
import MeCab
import re
import csv
import sys
from blog import mecab_test8_new




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

def apphoge(request):
    return render(request,'blog/hogera.html')

#def new(request):
    #return render(request, 'blog/new.html')

def speak(request):
    if request.method =='POST':
        f=open('data_sentence_input.txt','w',encoding="utf-8")
        f.write("")
        f.close()
        g=open('data_sentence_output.txt','w',encoding="utf-8")
        g.write("")
        g.close()
    return render(request, 'blog/hoge2.html')
    
    
##new1からもう一度敬語翻訳やる時?「はじめる」ボタンを押す時
def write(request):
    return render(request, 'blog/hoge2.html')

#def result(request):
    #d={
        #'comment':request.GET.get('comment')
   # }
    #print(d)
    #return render(request, 'blog/hoge.html',d)

##data_sentence_input.txt:入力文一覧が入ってる
##data_sentence_output.txt:出力文一覧が入ってる

def result2(request):
    d={
        'comment2':request.GET.get('comment2')
        }
    if(request.GET.get('comment2')=="形容詞"):
     return render(request, 'blog/new1.html') ##形容詞の時はすぐ翻訳した文を出す。

    ##print(request.GET.get('comment2')) 
    f=open('data_sentence_input.txt','a',encoding="utf-8")
    h=open('data_sentence_output.txt','a',encoding="utf-8")
    j=open('data_sentence2.txt','w',encoding="utf-8")##動詞を取り出すため
    g=open('one_data_sentence.txt','w',encoding="utf-8")
    f.write("入力文："+request.GET.get('comment2')+"\n")
    output_text=mecab_test8_new.mecab(request.GET.get('comment2'))
    h.write(output_text+"\n")
    f.close()
    h.close()
    f=open('data_sentence_input.txt','r',encoding="utf-8")
    h=open('data_sentence_output.txt','r',encoding="utf-8")
    j=open('data_sentence2.txt','r',encoding="utf-8")
    data=f.read()
    data1=h.read()
    data2=j.read()
    f.close()
    h.close()
    j.close()
    ##print(output_text)
###############追加　一文出すやつ(new1.htmlで使ってる)############################################
#g=open('one_data_sentence.txt','w',encoding="utf-8")
    g.write("(入力文："+request.GET.get('comment2')+")"+"\n")
    one_output_text=mecab_test8_new.mecab(request.GET.get('comment2'))
    g.write("出力文："+one_output_text+"\n")
    g.close()
    g=open('one_data_sentence.txt','r',encoding="utf-8")
    one_data=g.read()
    g.close()
    ##print(one_output_text)
    verb_output_text=mecab_test8_new.mecab(request.GET.get('comment2'))
    return render(request, 'blog/hoge3.html',{'comment2':data2})
    ##return render(request, 'blog/new1.html',{'comment2':one_data})  翻訳した一文をnew1に表示するようにする
    #################################################################
    ########################
def clear(request):
    if request.method =='POST':
        f=open('data_sentence_input.txt','w',encoding="utf-8")
        f.write("")
        f.close()
        g=open('data_sentence_output.txt','w',encoding="utf-8")
        g.write("")
        g.close()
        
    return render(request, 'blog/hoge2.html')
  ###############一覧を出す(new2.html)######################################    
def end(request):
 if request.method =='POST':
    f=open('data_sentence_output.txt','r',encoding="utf-8")
    data3=f.read()
    ##print("敬語翻訳した文一覧:"+"\n"+data3)
    return render(request, 'blog/new2.html',{'comment3':data3})#htmlに送る時、data3をcomment3とおく{{comment3}}
  ######追加　はじめる　ボタンで　一覧,動詞をリセットクリア############# 
def delete2(request):
    if request.method == 'POST':
        f=open('data_sentence_output.txt','w',encoding="utf-8")
        f.write("")
        f.close()
        g=open('data_sentence_input.txt','w',encoding="utf-8")
        g.write("")
        g.close()
        h=open('data_sentence2.txt','w',encoding="utf-8")
        h.write("")
        h.close()
        i=open('data_kouho.txt','w',encoding="utf-8")
        i.write("")
        i.close()
        j=open('data_kouho_num.txt','w',encoding="utf-8")
        j.write("")
        j.close()
        k=open('data_keigo_select.txt','w',encoding="utf-8")
        k.write("")
        k.close()
    return render(request, 'blog/hoge2.html')
    ###########主語を選んだ後#############
def vote(request):
    if request.method =='GET':
        d={
        'q1':request.GET.get('q1')
        }    
    f=open('data_keigo_select.txt','a',encoding="utf-8")##ラジオボタンで選択された敬語を保存
    f.write("敬語ラジオボタン："+request.GET.get('q1')+"\n")
    f.close()
    f=open('data_keigo_select.txt','r',encoding="utf-8")
    data=f.read()
    f.close()
    g=open('data_kouho_num.txt','a',encoding="utf-8")##候補数を保存
    g.write("候補数："+"\n")##入力した動詞を入れて、候補数を出したい。
    g.close()
    g=open('data_kouho_num.txt','r',encoding="utf-8")
    data1=g.read()
    g.close()
    h=open('data_kouho.txt','a',encoding="utf-8")##候補を保存
    h.write("候補："+"\n")##入力した動詞を入れて、候補を出したい
    h.close()
    h=open('data_kouho.txt','r',encoding="utf-8")
    data2=h.read()
    h.close()

    return render(request, 'blog/hoge4.html')
    
def kouho(request):
    if request.method =='GET':       
     return render(request, 'blog/new1.html')

    
    
    
    