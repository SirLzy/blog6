from django.core.cache import cache
from redis import Redis

from post.models import Article

rds = Redis(host='10.0.112.84',port=6379)

def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
            # request.get_full_path获取路径,url为统一资源定位符
            # 一切数据都可以通过url来获取
            key = 'PAGES-%s'% request.get_full_path()
            # 从缓存获取 response
            response = cache.get(key)
            # 如果有直接返回response,
            if response is not None:
                print('rerutn from cache')
                return response
            # 没有 -> 返回view视图函数
            else:
                print('return from view')
                response = view_func(request,*args,**kwargs)
                # 将结果添加到缓存
                cache.set(key,response,timeout)
            return response
        return wrap2
    return wrap1

def record_click(article_id,count=1):
    # 记录文章点击
    rds.zincrby('Article-click',article_id,count)

def get_top_n_articles(number):
    article_clicks = rds.zrevrange('Article-click',0,number,withscores=True)
    article_clicks = [[int(aid),int(click)] for aid , click in article_clicks]
    aid_list = [d[0] for d in article_clicks]
    articles = Article.objects.in_bulk(aid_list)

    for data in article_clicks:
        aid = data[0]
        data[0] = articles[aid]
    return article_clicks

import logging

logger = logging.getLogger('statistic')

def statistic(view_func):
    def wrap(request,*args,**kwargs):
        response = view_func(request,*args,**kwargs)
        if response.status_code == 200:
            ip = request.META['REMOTE_ADDR']
            aid = request.GET.get('aid')
            logger.info('%s %s'% (ip, aid))
        return response
    return wrap

