# coding: utf-8
import math

from django.core.cache import cache
from django.shortcuts import render, redirect


from post.models import Article, Comment
from post.helper import page_cache,record_click,get_top_n_articles,statistic

@page_cache(1)
def home(request):
    # 文章总数
    count = Article.objects.count()
    # 页面数ceil向上取整
    pages = math.ceil(count / 5)
    # 用户面前显示的是第一页为1
    page = int(request.GET.get('page',1))

    # 程序员面前显示的是第一页为0
    page = 0 if page < 1 or page >= (pages + 1) else (page - 1)
    # 第n页从第几篇文章开始显示
    start = page * 5
    # 从第几篇文章结束
    end = start + 5
    articles = Article.objects.all()[start:end]

    # 取出top10的文章
    top10 = get_top_n_articles(10)
    return render(request, 'home.html', {'articles': articles,'page':page,'pages':range(pages),'top10':top10})

@statistic
@page_cache(5)
def article(request):
    # 默认获取id=1的文章
    aid = int(request.GET.get('aid', 1))

    # key = 'article-%s' % aid
    # # 在缓存中获取文章
    # article = cache.get(key)
    # # 如果缓存中没有文章,去数据库中获取再在缓存区保存一下
    # if article is None:
    #     # 从数据库中获取文章
    #     article = Article.objects.get(id=aid)
    #     # 将文章保存到缓存中
    #     article = cache.set(key,article)

    # 获取到的文章的评论
    comments = Comment.objects.filter(aid=aid)
    return render(request, 'article.html', {'article': article,'comments': comments})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        return render(request, 'create.html')


def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article})


def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})


