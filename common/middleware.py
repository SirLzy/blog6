import time

from django.utils.deprecation import MiddlewareMixin

MAX_REQUEST_PER_SECOND = 2

class RequestBlockingMiddleware(MiddlewareMixin):
    # 限制用户的访问频率最大为每秒 2 次，超过 2 次时，等待至合理时间再返回
    def process_request(self,request):
        now = time.time()
        request_queue = request.session.get('request_queue',[])
        if len(request_queue) < MAX_REQUEST_PER_SECOND:
            request_queue.append(now)
            request.session['request_queue'] = request_queue
            print('放行')
        else:
            time0 = request_queue[0]
            if (now - time0) < 1:
                print('waitting---------------------', int(now))
                time.sleep(10)
                print('return-----------------------', int(time.time()))

            request_queue.append(time.time())
            request.session['request_queue'] = request_queue[1:]



