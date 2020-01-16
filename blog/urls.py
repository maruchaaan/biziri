from django.urls import path 
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('apphoge',views.apphoge,name='apphoge'),
    #path('apphoge/new',views.new,name='new'),
    ##path('apphoge/new/speak',views.speak,name='speak'),
    ##↓追加(new1.htmlからもう一度ボタンを押すときのやつ)
    path('apphoge/write/vote',views.vote,name='vote'),
    path('apphoge/write',views.write,name='write'),
    path('apphoge/end',views.end,name='end'),
    path('apphoge/kouho',views.kouho,name='kouho'),
    #↑追加
    path('apphoge/speak',views.speak,name='speak'),
    path('apphoge/write/result2',views.result2,name='result2'),
    path('apphoge/write/delete2', views.delete2,name='delete2'),    

]
