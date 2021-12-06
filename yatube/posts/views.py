from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Group, User
from posts.forms import PostForm
import datetime
from django.views.decorators.csrf import csrf_exempt


def index(request):
    posts = Post.objects.all()[:10]
    title = 'Последние обновления на сайте'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_list(request):
    template = 'posts/group_list.html'
    title = 'Список групп'
    text = 'Информация о группах проекта Yatube'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'text': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    num_of_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user,
        'page_obj': page_obj,
        'num_of_posts': num_of_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    pub_date = (Post.objects.get(pk=post_id)).pub_date
    post_count = post.author.posts.count()
    context = {
        'post': post,
        'author': author,
        'pub_date': pub_date,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(False)
            form.author = request.user
            form.pub_date = datetime.datetime.now()
            form.save()
            return redirect('posts:profile', username=form.author)
        else:
            context = {'form': form}
            return render(request, template, context)
    else:
        form = PostForm()
        context = {
            'form': form,
            'new_post': 'Новый пост'
        }
        return render(request, template, context)


@login_required
@csrf_exempt
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    template2 = 'posts:post_detail'
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        is_edit = True
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post1 = form.save(commit=False)
                post1.author = request.user
                post1.save()
                return redirect(template2, post_id)
            else:
                return render(
                    request,
                    template,
                    {
                        'post_id': post_id,
                        'form': form,
                        'is_edit': is_edit
                    }
                )
        form = PostForm(instance=post)
        return render(
            request,
            template,
            {
                'post_id': post_id,
                'form': form,
                'is_edit': is_edit
            }
        )
    else:
        return redirect(template2, post_id)
