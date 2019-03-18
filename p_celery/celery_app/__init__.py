from celery import Celery
app = Celery('jianli_spider')                                # 创建 Celery 实例
app.config_from_object('celery_app.celeryconfig')   # 通过 Celery 实例加载配置模块

# 针对from ... import *
# __all__ = ['app', 'task1', 'task2']