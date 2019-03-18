import time
from celery_app import task1
from celery_app import task2
from celery.result import AsyncResult
from celery_app import app


# t1 = task1.add.apply_async(args=[2, 8])        # 也可用 task1.add.delay(2, 8)
# t2 = task2.multiply.apply_async(args=[3, 7])   # 也可用 task2.multiply.delay(3, 7)

# 根据task_id获取结果
# print(AsyncResult('e15b6891-2e56-432f-9763-d0f63793f8c5').get())


# send_task精确到方法名

# app.send_task('celery_app.task2.multiply', (3, 9))

#
# for i in range(20):
#     app.send_task('celery_app.task1.add', (3, i))

if __name__ == '__main__':
    meta = {}
    start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python"
    meta["start_url"] = start_url
    app.send_task("celery_app.tasks.download", args=(start_url, meta),
                  queue="download", routing_key="for_download")
