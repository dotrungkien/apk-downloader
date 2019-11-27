from __future__ import print_function
import pandas as pd
import warnings
import sys
import requests
import progressbar
from bs4 import BeautifulSoup
import scrapy
import multiprocessing

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class ApkdownloaderSpider(scrapy.Spider):
    name = 'apkdownloader'
    base_url = 'https://m.apkpure.com'
    start_urls = ['https://m.apkpure.com/developer/Ketchapp?page=1']

    def parse(self, response):
        app_names = []
        for app_link in response.xpath("//a[@class='dd']/@href").getall():
            app_name = app_link.split('/')[-1]
            app_names.append(app_name)
            # self.get_apk(app_name)
        total_page = len(response.xpath(
            "//div[@class='paging']/ul/li").getall())
        current_page = int(response.xpath(
            "//div[@class='paging']/ul/li[@class='active']/a/text()").get())
        print(
            "current page {0} total page {1}".format(current_page, total_page))
        next_page = self.base_url + \
            response.xpath(
                "//div[@class='paging']/ul/li[@class='active']/a/@href").get()[:-1] + str(current_page + 1)
        print(next_page)
        print('\n'.join(app_names))
        if (current_page < total_page):
            yield response.follow(next_page, callback=self.parse)

    def get_apk(self, app_name):
        print("{+} getting download link for %s" % (app_name))
        site = "https://apkpure.com"
        url = "https://apkpure.com/search?q=%s" % (app_name)
        html = requests.get(url)
        parse = BeautifulSoup(html.text)
        for i in parse.find("p"):
            a_url = i["href"]
            app_url = site + a_url + "/download?from=details"
            html2 = requests.get(app_url)
            parse2 = BeautifulSoup(html2.text)
            for link in parse2.find_all("a", id="download_link"):
                download_link = link["href"]
            self.download_apk(app_name, download_link)

    def make_progress_bar(self):
        return progressbar.ProgressBar(
            redirect_stdout=True,
            redirect_stderr=True,
            widgets=[
                progressbar.Percentage(),
                progressbar.Bar(),
                ' (',
                progressbar.AdaptiveTransferSpeed(),
                ' ',
                progressbar.ETA(),
                ') ',
            ])

    def download_apk(self, app_name, download_link):
        print("{+} downloading %s" % (app_name))
        output_file = "apks/" + app_name + ".apk"
        r = requests.get(url=download_link, stream=True)
        with open(output_file, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            bar = self.make_progress_bar()
            bar.start(total_length)
            readsofar = 0
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    readsofar += len(chunk)
                    bar.update(readsofar)
                    f.write(chunk)
                    f.flush()
            bar.finish()
        print("{+} done. file saved to %s" % (output_file))
