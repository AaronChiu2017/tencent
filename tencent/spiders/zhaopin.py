# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent.items import TencentItem
from scrapy_redis.spiders import RedisCrawlSpider as CrawlSpider

class ZhaopinSpider(CrawlSpider):

    # 爬虫名称
    name = 'zhaopin'

    # 允许域名
    allowed_domains = ['tencent.com']

    # 启动url
    start_urls = ['https://hr.tencent.com/position.php?keywords=&tid=0&start=']


    redis_key = "tencent:zhaopin:strat_url"

    count = 0

    '''
    rules 提取连接规则列表
    
    Rule 提取规则对象
    link_extractor,         【重要】LinkExtractor 连接提取对象（按照这个连接的规则去提取）
    callback=None,          【重要】数据获取后回调处理函数
    follow=None,            【重要】是否跟进，表示是否继续提取连接访问页面
    cb_kwargs=None,         多值参数
    process_links=None,      提取连接之前进行对链接的加工处理
    process_request=identity 跟进链接之前对请求进行再次处理
    
    LinkExtractor 连接提取对象
    
    LinkExtractor(allow=r'position.php') => 提取 a 和 area 的 href 属性 里面包含 position.php
    
    allow=(),               提取的内容中包含的内容（正则表达式）
    deny=(),                决绝包含的内容（优先于包含）
    allow_domains=(),       允许的域名
    deny_domains=(),        拒绝的域名（优先）
    restrict_xpaths=(),     通过xpath提取连接
    tags=('a', 'area'),     按照标签提取 默认 a 标签和 area 标签
    attrs=('href',),        按照标签的属性 默认是 href
    restrict_css=(),        通过 css 选择器提取
    strip=True              把内容去掉两边空格
    '''

    '''
    通过 restrict_xpaths 提取内容
    '''
    # 也可以使用 xpath 进行连接提取
    # le = LinkExtractor(
    #     restrict_xpaths=('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]//a[@class="a-link-normal s-ref-text-link"]')
    # )


    rules = (
        # 列表页只提取连接地址继续跟进
        Rule(LinkExtractor(allow=r'position.php\?keywords=&tid=0&start='), follow=True,callback='parse_list'),
        # 详情页解析
        Rule(LinkExtractor(allow=r'position_detail.php'),callback='parse_detail',follow=False)
    )


    def parse_list(self, response):
        print(response.url)
        self.count += 1
        print(self.count)

    # def parse_item(self, response):
    #     print(response.url)
    #
    #     self.count += 1
    #     print(self.count)

    def parse_detail(self,response):
        item = TencentItem()

        # 处理详情页
        item["name"] = response.xpath('//td[@id="sharetitle"]/text()').extract_first()

        yield item

