import time
from celery_app import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# 当使用bind = True后，函数的参数发生变化，
# 多出了参数self（第一个参数），
# 相当于把add变成了一个已绑定的方法，
# 通过self可以获得任务的上下文。
@app.task(bind=True)
def add(self, x, y):
    logger.info(self)
    time.sleep(15)
    return x+y