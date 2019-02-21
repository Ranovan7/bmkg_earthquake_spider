import scrapy
from earthquake.items import EarthquakeItem
from datetime import datetime, timedelta


class EarthquakeSpider(scrapy.Spider):
    name = "earthquake"

    start_urls = [
        'https://www.bmkg.go.id/gempabumi/gempabumi-dirasakan.bmkg'
    ]

    def parse(self, response):
        curfew = datetime.now() - timedelta(days=1)
        for record in response.xpath("//table/tbody/tr"):
            # record the time of the earthquake
            recorded_time = ' '.join(record.xpath("./td[2]/text()").extract())[:-4]
            recorded_time = datetime.strptime(recorded_time, "%d/%m/%Y %H:%M:%S")

            if recorded_time < curfew:
                # meaning it has been recorded
                continue

            item = EarthquakeItem()

            item['time_occured'] = recorded_time

            # record the coordinate
            coordinate = record.xpath("./td[3]/text()").extract_first()
            coordinate = coordinate.split()
            if coordinate[1] == 'LS':
                item['latitude'] = '-' + coordinate[0]
            else:
                item['latitude'] = coordinate[0]
            if coordinate[3] == 'BT':
                item['longitude'] = coordinate[2]
            else:
                item['longitude'] = '-' + coordinate[2]

            # record the magnitude, depth, and location
            item['magnitude'] = record.xpath("./td[4]/text()").extract_first()
            item['depth'] = record.xpath("./td[5]/text()").extract_first()[:-3]
            item['location'] = record.xpath("./td[6]/a/text()").extract_first()

            yield item
