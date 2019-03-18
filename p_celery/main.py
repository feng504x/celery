from celery_app import app

if __name__ == '__main__':
    app.start(argv=['celery', 'worker', '-l', 'info',
                    '-P', 'eventlet', '-c', '4', '-n', 'worker1@%h'
                    ])

    # 4.0版本需加上此参数'-P', 'eventlet'  --pool=solo
    # - Q 指定特定的队列  '-Q', 'download_queue',
    #  '-f', 'logs/celery.log', 保存日志

    # 开启多个celery的命令
    # celery multi start 10 -A proj -l info -Q:1-3 images, video -Q:4, 5 data -Q default -L:4,5 debug