# coding=utf-8
from pymongo import MongoClient


class Singleton(object):
    """
    单例模式
    """
    instance = None

    def __new__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kw)
        return cls.instance


class MYMongoclient(Singleton):
    def __init__(self):
        client = MongoClient()
        self.collection = client["job"]["zhilian"]

    def save_item(self, item):
        if isinstance(item, dict):
            self.collection.insert(item)


_mongo_client = MYMongoclient()
save_item = _mongo_client.save_item

if __name__ == '__main__':
    _mongo_client1 = MYMongoclient()
    _mongo_client2 = MYMongoclient()
    print(_mongo_client1)
    print(_mongo_client2)