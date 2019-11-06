from django.urls import path 
from . import views
from . import kaiseki


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('apphoge',views.apphoge,name='apphoge'),
    path('apphoge/new',views.new,name='new'),
    path('apphoge/new/speak',views.speak,name='speak'),
    path('apphoge/new/write',views.write,name='write'),
    path('apphoge/new/write/result',kaiseki.result,name='result'),
]
