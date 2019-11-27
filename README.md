<h1 align="center">Welcome to apk-downloader 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> simple way to download apks from apkpure.com

## Install

```sh
pip install -r requirement.txt
```

## Usage

Change the apks url inside `/apkdownloader/spiders/apkdownloader`, for example:

```python
start_urls = ['https://m.apkpure.com/developer/Ketchapp?page=1']
```

then start crawling:

```sh
scrapy crawl apkdownloader
```

## Author

👤 **Do Trung Kien**

- Website: kiendt.me
- Github: [@dotrungkien](https://github.com/dotrungkien)

## Show your support

Give a ⭐️ if this project helped you!
