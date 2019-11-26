import pandas as pd
import scrapy
import urllib.request


class ApkgrabberSpider(scrapy.Spider):
    name = 'apkgrabber'
    base_url = 'https://m.apkpure.com'
    start_urls = ['https://m.apkpure.com/developer/Ketchapp?page=1',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=2',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=3',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=4',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=5',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=6',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=7',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=8',
                  #   'https://m.apkpure.com/developer/Ketchapp?page=9',
                  ]
    links = []

    def parse(self, response):
        for app_link in response.xpath("//a[@class='dd']/@href").getall():
            url = self.base_url + app_link
            print("Start downloading ", url)
            app_name = app_link.split('/')[-1]
            urllib.request.urlretrieve(url, "data/" + app_name + ".apk")

        # print("links: ", self.links)
