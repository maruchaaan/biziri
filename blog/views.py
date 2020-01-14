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
from blog import mecab_test8
#from flask import Flask, render_template
#app=Flask(__name__)
#app.debug=True





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

#def speak(request):
    #return render(request, 'blog/hoge.html')

def write(request):
    return render(request, 'blog/hoge2.html')

#def result(request):
    #d={
        #'comment':request.GET.get('comment')
   # }
    #print(d)
    #return render(request, 'blog/hoge.html',d)

def result2(request):
    d={
        'comment2':request.GET.get('comment2')
        }
    
    print(request.GET.get('comment2'))
    f=open('data_sentence.txt','a',encoding="utf-8")
    f.write("入力文："+request.GET.get('comment2')+"\n")#入力文はテキストファイルに保存
    f.close()
    f=open("data_sentence2.txt",'r',encoding="utf-8")
    data=f.read()
    f.close()
    output_text=mecab_test8.mecab(request.GET.get('comment2'))
    return render(request, 'blog/hoge3.html',{'comment2':data})
  
    
    
    f.write("出力文："+output_text+"\n")
    f.close()
    f=open('data_sentence.txt','r',encoding="utf-8")
    data=f.read()
    f.close()

    
    print(output_text)
   
    return render(request, 'blog/hoge2.html',{'comment2':data})





def delete2(request):
    if request.method == 'POST':
        f=open('data_sentence.txt','w',encoding="utf-8")
        f.write("")
        f.close()
    return render(request, 'blog/hoge2.html')



