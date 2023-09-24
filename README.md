# Learn Scrapy

## 1. Creating a project

```bash
scrapy startproject tutorial
```

This will create a tutorial directory with the following contents:

```bash
tutorial/
    scrapy.cfg            # deploy configuration file
    tutorial/             # project's Python module, you'll import your code from here
        __init__.py
        items.py          # project items definition file
        middlewares.py    # project middlewares file
        pipelines.py      # project pipelines file
        settings.py       # project settings file
        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

What is middleware? [Middleware](https://docs.scrapy.org/en/latest/topics/spider-middleware.html)

## 2. Creating a spider

Spiders are classes that you define and that Scrapy uses to scrape information from a website (or a group of websites). They must subclass `Spiler` and define the initial requests to make, optionally how to follow links in the pages, and how to parse the downloaded page content to extract data.

The code for our example is in `tutorial/spiders/quotes_spider.py`.

```python
from pathlib import Path
from typing import Iterable

import scrapy
from scrapy.http import Request

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self) -> Iterable[Request]:
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = f'quotes-{page}.html'

        Path(filename).write_bytes(response.body)

        self.log(f'Saved file {filename}')
```

Some attributes:

- `name`: identifies the Spider. It must be unique within a project, that is, you can’t set the same name for different Spiders.
- `start_requests()`: must return an iterable of Requests (you can return a list of requests or write a generator function) which the Spider will begin to crawl from. Subsequent requests will be generated successively from these initial requests.
- `parse()`: a method that will be called to handle the response downloaded for each of the requests made. The response parameter is an instance of `TextResponse` that holds the page content and has further helpful methods to handle it.

The `parse()` method usually parses the response, extracting the scraped data as dicts and also finding new URLs to follow and creating new requests (Request) from them.

## 3. Running the spider

Normally, we need to cd to the project’s top level directory (where the `scrapy.cfg` file is) and run:

```bash
scrapy crawl quotes
```

but we can also can run it without explicitly creating a project, by using the main.py

```python
import subprocess

commands = ["cd","src","&&","scrapy","crawl","quotes"]

options = ["--nolog", "--o", "../results/quotes.json"]

subprocess.run(commands + options, shell=True)
```

The `--nolog` option is used to disable logging, and the `--o` option is used to save the output to a file (overwriting the file if it already exists)

## 4. Extracting data

When testing, you can use scrapy shell to fetch a single page and try out some Selectors on it:

For example, to fetch the first page of quotes from quotes.toscrape.com:

```bash
scrapy shell 'http://quotes.toscrape.com/page/1/'
```
