from __future__ import print_function
import pandas as pd
import warnings
import sys
import requests
import progressbar
from bs4 import BeautifulSoup
import scrapy
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class ApkgrabberSpider(scrapy.Spider):
    name = 'apkgrabber'
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

    def parse(self, response):
        for app_link in response.xpath("//a[@class='dd']/@href").getall():
            app_name = app_link.split('/')[-1]
            self.get_apk(app_name)

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
