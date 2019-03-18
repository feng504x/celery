from datetime import timedelta
from celery.schedules import crontab
from kombu import Queue
from kombu import Exchange

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/8'

# 指定时区，默认是 UTC
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_TIMEZONE='UTC'

CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'pickle'

# 指定导入的任务模块, worker
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2',
    'celery_app.tasks',
)


# 为Celery设定多个队列，CELERY_QUEUES是个tuple，每个tuple的元素都是由一个Queue的实例组成
# 创建Queue的实例时，传入name和routing_key，name即队列名称
# 像Redis或SQS这样的非AMQP后端不支持交换，
# 因此它们要求交换具有与队列相同的名称。使用此设计可确保它也适用于它们。
CELERY_QUEUES = (
    # {'add_queue':{'exchange': 'add_queue', 'exchange_type': 'direct', 'routing_key': 'add_router'}}
    Queue(name='add', routing_key='add_router', exchange=Exchange('add', type='direct')),
    Queue(name='multiply', routing_key='multiply_router', exchange=Exchange('multiply', type='direct')),
    Queue('page_list',
          exchange=Exchange('page_list', type='direct'),
          routing_key='for_page_list'),

    Queue('page_detail',
          exchange=Exchange('page_detail', type='direct'),
          routing_key='for_page_detail'),

    Queue('download',
          exchange=Exchange('download', type='direct'),
          routing_key='for_download'),
    Queue('item', exchange=Exchange('item', type='direct'),
          routing_key='for_save'),
)

# 最后，为不同的task指派不同的队列
# 将所有的task组成dict，key为task的名称，即task所在的模块，及函数名
# 每个task的value值也是为dict，设定需要指派的队列name，及对应的routing_key
# 这里的name和routing_key需要和CELERY_QUEUES设定的完全一致
CELERY_ROUTES = {
    'celery_app.task1.add': {
        'queue': 'add',
        'routing_key': 'add_router',
    },
    'celery_app.task2.multiply': {
        'queue': 'multiply',
        'routing_key': 'multiply_router',
    },
}





# schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
#          'args': (5, 8)                           # 任务函数参数
#     },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task2.multiply',
#         'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
#         'args': (3, 7)                            # 任务函数参数
#     }
# }