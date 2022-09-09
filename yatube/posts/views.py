from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

POSTS_PER_PAGE = 10


def context_pagination(queryset, request):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}


@cache_page(20, key_prefix='index_page')
def index(request: HttpRequest):
    template: str = 'posts/index.html'
    post_list = Post.objects.all()
    context = context_pagination(post_list, request)
    return render(request, template, context)


def group_posts(request: HttpRequest, slug: str):
    group = (get_object_or_404(Group.objects.prefetch_related('posts'),
             slug=slug))
    post_list = group.posts.all()
    template: str = 'posts/group_list.html'
    context = {'group': group}
    context.update(context_pagination(post_list, request))
    return render(request, template, context)


def profile(request: HttpRequest, username):
    author = (get_object_or_404(User,
              username=username))
    following = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(user=request.user,
                                       author=author).exists()
        if follow is True:
            following = True
    user_posts = author.posts.select_related('author')
    template: str = 'posts/profile.html'
    context = {'author': author,
               'following': following}
    context.update(context_pagination(user_posts, request))
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id):
    template: str = 'posts/post_detail.html'
    post = (get_object_or_404(Post,
            pk=post_id))
    form = CommentForm(request.POST or None)
    comments = post.comments.select_related()
    context = {'post': post,
               'form': form,
               'comments': comments}
    return render(request, template, context)


@login_required
def post_create(request):
    template: str = 'posts/create_post.html'
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if request.method == 'POST' and form.is_valid():
        post_form = form.save(commit=False)
        post_form.author = request.user
        post_form.save()
        return redirect('posts:profile', username=request.user)
    context = {'form': form}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template: str = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post.pk)
    is_edit = True
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form = form.save()
        return redirect('posts:post_detail', post.pk)

    context = {'form': form,
               'is_edit': is_edit,
               'post': post}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    context = context_pagination(post_list, request)
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
