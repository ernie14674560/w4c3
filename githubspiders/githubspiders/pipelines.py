# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from githubspiders.models import Repository, engine
import dateutil.parser



class GithubspidersPipeline(object):

    def process_item(self, item, spider):
        item['update_time'] = dateutil.parser.parse(item['update_time'])
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        """ when the spider is open, create database session
        """
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        """ when the spider is close, submit session and close session
        """
        self.session.commit()
        self.session.close()
