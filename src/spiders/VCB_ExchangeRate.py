import scrapy
import xmltodict
from scrapy.http import Request


class VCB_ExchangeRate(scrapy.Spider):
    name = 'VCB_ExchangeRate'
    start_urls = ['https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx']
    output = {
        'status': None,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, errback=self.handle_error)

    def parse(self, response):
        try:
            # Get the response page source
            page_source = response.text

            # Parsing the xml to dict
            data = xmltodict.parse(page_source)

            output = {
                'status': 'success',
                'message': 'Get exchange rate from VCB successfully',
                'data': data
            }

            yield output
        except Exception as e:
            self.output['status'] = 'error'
            self.output['message'] = 'An error occurs when parsing the exchange rate xml file: ' + str(e)
            self.output['data'] = None
            yield self.output

    def handle_error(self, failure):
        self.output['status'] = 'error'
        self.output['message'] = repr(failure)
        self.output['data'] = None
        yield self.output
