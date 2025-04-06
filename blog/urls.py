from django.urls import path
from blog.views import index, about, add_post

app_name = 'blog'
urlpatterns = [
    path('about', about, name='about'),
    path('post/', add_post, name='add_post'),
    path('', index, name='index'),
]
