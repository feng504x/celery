## celery爬虫

#### 简介
- celery是一个`任务队列`,同时也`支持任务调度`，强大的生产者消费者模型
- 附上最新celery文档http://docs.celeryproject.org/en/latest/
- 整个爬虫程序将请求页面, 下载页面, 解释页面分成3个队列, 耦合度较低,
  并可以定制化不同程序对应不同worker,资源合理分配worker的数量
- main.py中实现用python脚本打开celery服务
- 在celery_app/tasks定义的任务
- celery实例通过配置文件celeryconfig.py配置


#### 注意
- 启动worker的时候如果需要使用celerybeat的定时功能，需要加上`-B`的参数
- 启动一个 download_queue,-A app的位置,-Q 指定启动的队列,worker 消费者,-c 4个并发,-B 启动该队列的celerybeaet，-n 节点名字为downloader，-l log等级为info
`celery -A tasks.workers -Q download_queue worker -B -l info -c 4 -n downloader`
- 在app.conf.update(`'CELERYBEAT_SCHEDULE'`)中能够实现celerybeat的定时任务功能，如果是定时执行，比如某天的某小时，可以使用crontab的方式来完成
- log中使用dictConfig的方式添加日志，格式比较清晰，后续可以使用该方式来设置日志
- 实例化celery的app的时候，使，能够让celery自动的从`celery_app.tasks`中寻找tasks，方便用include的方式
- 在tasks中传递了resposne对象，不能使用json的序列化方式，选择`pickle`的方式
- 在task中，都是用`app.send_task("**task", args=(response,),queue="parse_page_list",routing_key="for_page_list")
`来把结果交给一个task去完成，同时使用queue和routing_key的方式来，能够把当前任务队列中的内容传递到另一个任务队列，celery能够自动的寻找queue和routing_key匹配的队列去接收任务

#### 本代码可以加强的地方
- 数据库存入时候的去重
- 请求的时候对cookie，headers的处理，refer的处理，代理ip的处理


#### 使用体会
- 使用celery能够轻松的帮助我们完成一个大型的分布式爬虫，但是如果和scrapy或者是scrapy_redis相比的话，整个程序会变得很凌乱
- 后续的框架，可以使用celery来完成一些细节功能的异步调用，但是目前感觉不能纯粹的依靠celery来完成一个分布式的爬虫, 而是要把celery用在他正确的用途上, 例如注册后发送验证邮件..等等

#### 项目图片
![初始调用种子url的方法](https://i.imgur.com/mVaQQSl.jpg)

![配置文件1](https://i.imgur.com/J3Y3iyM.jpg)

![配置文件2](https://i.imgur.com/wg3BmWf.jpg)

![配置文件3](https://i.imgur.com/SACSwL0.jpg)

![tasks任务](https://i.imgur.com/2vFnl9P.jpg)