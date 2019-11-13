from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from Python.MeCab import MeCab


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

def new(request):
    return render(request, 'blog/new.html')

def speak(request):
    return render(request, 'blog/hoge.html')

def write(request):
    return render(request, 'blog/hoge2.html')

def result(request):
    d={
        'comment': request.GET.get('comment')
    }
    return render(request, 'blog/hoge.html',d)

def result3(request):
    d={
        'comment2': request.GET.get('comment2')
    }
    return render(request, 'blog/hoge2.html',d)

def result2(request):
    d={
        'comment2': request.GET.get('comment2')
    }
    mt = MeCab("-Owakati")
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
