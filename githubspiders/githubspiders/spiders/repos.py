# -*- coding: utf-8 -*-
import scrapy
from githubspiders.items import GithubspidersItem


class ReposSpider(scrapy.Spider):
    name = 'repos'
    @property
    def start_urls(self):
        url_templ = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_templ.format(i) for i in range(1, 5))
        return urls

    def parse(self, response):
        for repo in response.css('li.col-12'):
            item = GithubspidersItem({
                'name': repo.css('a::text').extract_first().strip(),
                'update_time': repo.css('relative-time::attr(datetime)').extract_first()
            })
            yield item
