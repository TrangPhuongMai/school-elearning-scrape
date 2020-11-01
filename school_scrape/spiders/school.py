# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import logging
import m3u8
import requests
import subprocess
from urllib.parse import urlparse


class SchoolSpider(scrapy.Spider):
    name = 'school'
    # allowed_domains = ['web']
    start_urls = ['https://elearning.thanglong.edu.vn/login/index.php']
    subject = ['MA111']

    # loging into elearning
    def parse(self, response):
        logging.info('=============================== (parse) ===============================')
        return (FormRequest.from_response(
            response, formdata={
                'username': 'A28565',
                'password': 'jimraynor98'}, callback=self.parse_searchpage)
        )

    # search the page for subject needed to be crawl
    def parse_searchpage(self, response):
        logging.info('=============================== (parse_searchpage) ===============================')
        logging.info(response.xpath('//h5//text()').extract())
        for s in self.subject:
            return (FormRequest.from_response(response=response, formdata={
                'q': str(s)}, callback=self.parse_page))

    def parse_page(self, response):
        logging.info('=============================== (parse_page) ===============================')
        logging.info(response.xpath('//h4//text()').extract())
        url = response.xpath("//h4[@class='result-title']/a[1]/@href").get()
        print(url)
        return Request(url=url, callback=self.parse_subject)

    def parse_subject(self, response):
        logging.info('=============================== (parse_subject) ===============================')

        m3u8_urls = response.xpath("//div//source/@src").getall()
        # print(m3u8_urls)
        # m3u8_urls = [
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan8_N2_CucTriKhongDK_LT_BT_DONE.m3u8',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan8_N2_DinhNghiaNguyenHam_CongThuc_LT_DONE2.m3u8',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan8_N2_CachTinhTichPhanPhuongPhapDoiBien_LT_DONE2.m3u8',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_CachTinhTichPhanHamLuongGiac_LT_DONE2.m3u8',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_CachTinhTichPhan_PhuongPhapTinhTichPhanTungPhan_LT_DONE2.m3u8',
        #             'https://media3.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_1_2_XayDungDinhNghiaViDuTPXD_DONE5.m3u8',
        #             'https://media3.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_3a_CacTinhChatCuaTichPhan_DONE5.m3u8',
        #             'https://media3.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_3b_UngDungTichPhan_DONE5.m3u8',
        #             'https://media3.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_4_HuongDanBaiTap_DONE5.m3u8',
        #             'https://media1.thanglong.edu.vn/videojs/index.php?id=2020/MA110_Tuan8_BaiToanVeCucTri',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_BT_NguyenHam_DONE11.m3u8',
        #             'https://media1.thanglong.edu.vn/courses/2020/MA110_Tuan9_N2_BT_TichPhan_DONE11.m3u8']

        # logging.info('=============================== {} ==============================='.format(()))
        for i,m3u8_url in enumerate(m3u8_urls):
            # logging.info('=============================== {} ==============================='.format(dir(m3u8_url)))
            try:
                r = m3u8.load(m3u8_url)
                print(r.base_uri)
                # break
                name = 'D:/gt3/video-{}.ts'.format(i)
                with open(name, 'wb') as f:
                    for l in range(len(r.data['segments'])):
                        s = r.data['segments'][l]['uri']
                        a = requests.get('{}{}'.format(r.base_uri,s))
                        f.write(a.content)
            except Exception as e:
                print(e)
        return

    # def parse_video(self,response):
