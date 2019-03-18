# coding=utf-8
from celery_app import app
from downloader import parse_url
from page_parse import extract_position_detial_info, extract_position_list
from db import save_item


@app.task(ignore_result=True)
def download(url, meta, flag="list"):
    response = parse_url(url)
    if response is not None:
        if flag == "detail":
            app.send_task("celery_app.tasks.parse_page_detail", args=(response, meta),queue="page_detail",routing_key="for_page_detail")
        elif flag == "list":
            app.send_task("celery_app.tasks.parse_page_list", args=(response, meta),queue="page_list",routing_key="for_page_list")


@app.task(ignore_result=True)
def parse_page_list(response, meta):
    position_list, next_url = extract_position_list(response)
    if next_url is not None:
        app.send_task("celery_app.tasks.download",args=(next_url,meta),queue="download",routing_key="for_download")

    for position in position_list:
        meta["item"] = position
        app.send_task("celery_app.tasks.download",args=(position["position_href"],meta,"detail"),queue="download",routing_key="for_download")


@app.task(ignore_result=True)
def parse_page_detail(response,meta):
    item = meta.get("item",None)
    item = extract_position_detial_info(response,item)
    app.send_task("tasks.downloader.process_item",args=(item,),queue="item",routing_key="for_save")


@app.task(ignore_result=True)
def process_item(item):
    save_item(item)


# if __name__ == '__main__':
#     url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python'
#     response = parse_url(url)
#     parse_page_list(response, meta={})

