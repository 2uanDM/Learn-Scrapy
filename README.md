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

After you run this, you should see the Scrapy shell. We can try to extract using CSS selector and XPATH following this format

```bash
>>> response.css("div.quote")
```

Each of the selectors returned by the query above allows us to run further queries on them. For example, to extract the quote text and author from the first quote on the page, we can run:

```bash
>>> quote = response.css("div.quote")[0]
>>> text = quote.css("span.text::text").get()
>>> author = quote.css("small.author::text").get()
>>> tags = quote.css("div.tags a.tag::text").getall()
```

Given that tags are a list of strings, we can use `.getall()` method to get all of them:

```bash
>>> tags = quote.css("div.tags a.tag::text").getall()
```

## 5. Following links

Instead of just scraping the stuff from the first two pages from quotes.toscrape.com, we can also follow the links to the detail pages and scrape the data from there.

For example, we see that when starting from the first page, we have the next button at the bottom:

```html
<ul class="pager">
  <li class="next">
    <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
  </li>
</ul>
```

This allow us to recursively follow the links to the next pages untils we reach the end.

Let's use the scrapy shell to test this:

```bash
>>> response.css("li.next a").get()
```

Then we can extract the link from the anchor tag:

```bash
>>> response.css("li.next a::attr(href)").get()
```

We can use the `response.follow` method to generate a new request to the next page, and pass the response to the `parse` method recursively:

```python
from pathlib import Path
from typing import Any

import scrapy
import os
from scrapy.http import Request

class QuotesSpider(scrapy.Spider):
    name = "quotes" # The name of the spider (unique within the project)

    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def __init__(self, name: str | None = None, **kwargs = Any):
        super().__init__(name, **kwargs)

    def parse(self, response):
        print(f'Current page: {response.url}')
        for quote in response.css('div.quote'):
            data = {
                'text' : qoute.css('span.text::text').get(),
                'author' : quote.css('small.author::text').get(),
                'tags' : qoute.css('div.tags a.tag::text').getall()
            }
            yield data

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.Request(next_page, callback = self.parse)

```

### A shortcut for creating Requests

As a shortcut for creating Request object you can use `response.follow`

We can also pass a selector to `response.follow` instead of a string; this selector should extract necessary attributes:

```python
for href in response.css('ul.pager a'):
    yield response.follow(href, callback=self.parse)
```

To create multiple request from an iterable, you can use `response.follow_all` instead:

```python
anchors = response.css('ul.pager a')
yield from response.follow_all(anchors, callback = self.parse)
```

Shorter

```python
yield from response.follow_all(css='ul.pager a', callback = self.parse)
```

Another intersting thing this spider demonstrates is that, even if there are many quotes from the same author, we don't need to worry about visiting the same author page multiple times, because Scrapy filters out duplicate requests for us. This is because, by default, it filters out URLs already visited, and URLs already in the queue, to avoid scraping the same pages multiple times, or to avoid scraping different pages with URLs that only differ in some query parameters. This behavior can be configured by the `DUPEFILTER_CLASS` setting.

An example about configuring the dupefilter can be found [here](https://docs.scrapy.org/en/latest/topics/settings.html#dupefilter-class)
