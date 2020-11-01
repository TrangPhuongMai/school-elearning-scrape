# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import FormRequest, Request

class ProSpider(scrapy.Spider):
    name = 'pro'
    start_urls = ['https://dangkyhoc.thanglong.edu.vn/']

    def parse(self, response):
        logging.info('=============================== (parse) ===============================')
        return (FormRequest.from_response(
            response, formdata={
                'tbUserName': 'A28565',
                'tbPassword': 'htpftsat2015'}, callback=self.parse_timetable)
        )
    def parse_timetable(self,response):
        # url = response.xpath('//a[@href="/ToanTruong/LichThiLaiToanTruong.aspx"]')
        for i in self.start_urls:
            print(i+'ToanTruong/LichThiLaiToanTruong.aspx')
            return (Request(
                url= i + '/ToanTruong/LichThiLaiToanTruong.aspx',
                callback=self.parse_table
            ))

    def parse_table(self,response):
        logging.info('=============================== (parse) ===============================')
        print(response.xpath('//form[@name="aspnetForm"]//text()').extract())