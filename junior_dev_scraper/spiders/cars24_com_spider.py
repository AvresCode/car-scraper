import scrapy
import json
import re
# from benedict import benedict
from benedict import BeneDict  # Updated import
from w3lib.url import add_or_replace_parameter

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/']
    

    def parse(self, response):
        for car in response.css('div._3IIl_._1xLfH'):

       
            car_data = {
                "Brand": car.css('h3.RZ4T7::text').get(),
                "Year": car.css('p._1i1E6::text').get(),
                "Link": car.css('a._1Lu5u::attr(href)').get(),
                "Price": car.css('span._7yds2::text').get(),
                "Mileage": car.css('ul._3ZoHn li:nth-child(2)::text').get(),
                "Engine Size": car.css('ul._3ZoHn li:nth-child(3)::text').get(),
            }
            car_url = car_data["Link"]
            yield response.follow(car_url, self.parse_detail, meta={"car_data": car_data})

    def parse_detail(self, response):
        fuel = response.css('div._148U_._3oj4O div._2y04X:nth-child(6) p.v2mgh::text').get()
        car_data = response.meta.get("car_data", {})

        yield {
            **car_data,  # Include main page data
            "Fuel": fuel,
        }

        {'Brand': 'JEEP WRANGLER', 'Year': '2020 | SAHARA', 'Link': 'https://www.cars24.com/ae/buy-used-jeep-wrangler-2020-cars-dubai-9714825119/', 'Price': '170,222', 'Mileage': '81,538 km', 'Engine Size': '6cyl 3.6L ', 'Fuel': '3.6L'}
