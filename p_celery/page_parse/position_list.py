# coding=utf-8
from .load_response import load_response
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def extract_position_list(response):
    html = load_response(response)
    div_list = html.xpath("//div[@id='listContent']//div[@class='contentpile__content__wrapper__item clearfix']")
    position_list = []
    for div in div_list:
        item = dict()
        item["position_title"] = div.xpath("./a[1]//div[contains(@class,'jobName')]/span[1]/text()")[0] if len(div.xpath("./a[1]//div[contains(@class,'jobName')]/span[1]/text()"))>0 else None
        item["position_href"] = div.xpath("./a[1]/@href")[0] if len(div.xpath("./a[1]/@href"))>0 else None
        item["company_name"] = div.xpath("./a[1]//div[contains(@class,'commpanyName')]/a[1]/@title")[0] if len(div.xpath("./a[1]//div[contains(@class,'commpanyName')]/a[1]/@title"))>0 else None
        item["city"] = div.xpath("./a[1]//ul[@class='contentpile__content__wrapper__item__info__box__job__demand']/li[1]/text()")[0] if len(div.xpath("./a[1]//ul[@class='contentpile__content__wrapper__item__info__box__job__demand']/li[1]/text()"))>0 else None
        item["pay"] = div.xpath("./a[1]//p[@class='contentpile__content__wrapper__item__info__box__job__saray']/text()")[0] if len(div.xpath("./a[1]//p[@class='contentpile__content__wrapper__item__info__box__job__saray']/text()")) > 0 else None
        position_list.append(item)
        logger.info(str(item))
    # 下一页
    next_url = html.xpath("//a[@class='next-page']/@href")
    next_url = next_url[0] if len(next_url) > 0 else None
    logger.info(next_url)
    return position_list, next_url
