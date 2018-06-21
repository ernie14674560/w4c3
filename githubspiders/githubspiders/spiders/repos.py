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
        for repo in response.css('.source'):
            repo_url = response.urljoin(repo.css('.source .mb-1 a::attr(href)').extract_first())
            request = scrapy.Request(repo_url, callback=self.cbr_parse)  # CBR = Commit, Branch, Release
            item = GithubspidersItem()
            item['name'] = repo.css('a::text').extract_first().strip()
            item['update_time'] = repo.css('relative-time::attr(datetime)').extract_first()
            request.meta['item'] = item
            yield request

    def cbr_parse(self, response):
        item = response.meta['item']
        item['commits'] = response.css('.commits span::text').extract_first().strip()
        item['branches'] = response.css('.commits+ li span::text').extract_first().strip()
        item['releases'] = response.css('li:nth-child(3) span::text').extract_first().strip()
        yield item

# 在迭帶 response.css('.source')為 repo 中
# 各個倉庫(repo)的url : response.urljoin(repo.css('.source .mb-1 a::attr(href)').extract_first())

# 在各個倉庫頁面中:
# commit num : response.css('.commits span::text').extract_first().strip()
# branch num : response.css('.commits+ li span::text').extract_first().strip()
# release num : response.css('li:nth-child(3) span::text').extract_first().strip()
