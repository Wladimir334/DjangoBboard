from pydoc import describe

from django.db.models.expressions import result
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from .forms import PostForm, FilterForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    # (select * from blog_post order by created_at DESC) DESC - это минус, те выводятся сначала последние посты
    # получение всех постов, отсортированных по дате публикации
    # (select * from blog_post order by created_at DESC)
    posts = Post.objects.all().order_by('-created_at')
    count_posts = Post.objects.count()  # count_posts = len(posts)
    # показываем по 3 потса на стрнице
    paginator = Paginator(posts, 4)
    # получаем номер стр из URL
    page_number = request.GET.get('page')
    # получаем обхекты для текущей стр
    page_obj = paginator.get_page(page_number)
    filter_form = FilterForm()
    context = {"title": "Главная страница",
               "page_obj": page_obj,
               "count_posts": count_posts,
               "filter_form": filter_form
               }
    return render(request, template_name='blog/index.html', context=context)

def about(request):
    count_posts = Post.objects.count()
    context = {'title': "О сайте", "count_posts": count_posts}
    return render(request, template_name='blog/about.html', context=context)

@login_required
def add_post(request):
    if request.method == "GET":
        post_form = PostForm(author=request.user)
        context = {"title": "Добавить пост","form": post_form}
        return render(request, template_name='blog/post_add.html', context=context)

    if request.method == "POST":
        post_form = PostForm(data=request.POST, files=request.FILES, author=request.user)
        if post_form.is_valid():
            # post = Post()
            # post.title = post_form.cleaned_data['title']
            # post.text = post_form.cleaned_data['text']
            # post.author = post_form.cleaned_data['author']
            # post.image = post_form.cleaned_data['image']
            post_form.save()
            return index(request)

def read_post(request, slug):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, slug=slug)
    context = {"title": "Информация о посте", "post": post}
    return render(request, template_name="blog/post_detail.html", context=context)
@login_required
def update_post(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post_form = PostForm(data=request.POST,
                             files=request.FILES,
                             instance=post,
                             initial={'author': post.author})
        if post_form.is_valid():
            # post.title = post_form.cleaned_data['title']
            # post.text = post_form.cleaned_data['text']
            # post.author = post_form.cleaned_data['author']
            # post.image = post_form.cleaned_data['image']
            # post.price = post_form.cleaned_data['price']
            post_form.save()
            return redirect('blog:read_post', slug=post.slug)
    else:
        post_form = PostForm(initial={
            "title": post.title,
            "author": post.author,
            "text": post.text,
            # "price": post.price,
            "image": post.image

        })
        return render(request, template_name="blog/post_edit.html", context={"form": post_form})

@login_required
def delete_post(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    context = {"post": post}
    if request.method == "POST":
        post.delete()
        return redirect('blog:index')
    return render(request, template_name="blog/post_delete.html", context=context)

def user_posts(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # posts = user.posts.all()
    posts = Post.objects.filter(author=user).select_related('author')
    context = {"user": user, "posts": posts}
    return render(request, template_name='blog/user_posts.html', context=context)

def user_info(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=user).select_related('author')
    context = {"user": user, "posts":posts}
    return render(request, template_name='blog/user_info.html', context=context)

def page_not_found(request, exception):
    return render(request, template_name="blog/404.html", context={'title': '404'})

def forbidden(request, exception):
    return render(request, template_name="blog/403.html", context={'title': '403'})

def server_error(request):
    return render(request, template_name="blog/500.html", context={'title': '500'})

def search_post(request):
    query = request.GET.get('query')
    query_text = Q(title__icontains=query) | Q(text__icontains=query)
    results = Post.objects.filter(query_text)
    paginator = Paginator(results, 3)
    # получаем номер стр из URL
    page_number = request.GET.get('page')
    # получаем обхекты для текущей стр
    page_obj = paginator.get_page(page_number)
    count_posts = results.count()
    context = {"title": "Главная страница",
               "page_obj": page_obj,
               "count_posts": count_posts
               }
    return render(request, template_name='blog/index.html', context=context)

def filter_post(request):
    author_id = request.GET.get('author')
    if not author_id:
        results = Post.objects.all()
    else:
        author = User.objects.get(pk=author_id)
        query_text = Q(author__exact=author)
        results = Post.objects.filter(query_text)

    paginator = Paginator(results, 3)
    # получаем номер стр из URL
    page_number = request.GET.get('page')
    # получаем обхекты для текущей стр
    page_obj = paginator.get_page(page_number)
    count_posts = results.count()
    filter_form = FilterForm()
    context = {"title": "Главная страница",
               "page_obj": page_obj,
               "count_posts": count_posts,
               "filter_form": filter_form
               }
    return render(request, template_name='blog/index.html', context=context)