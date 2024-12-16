# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapyItem(scrapy.Item):
    team_a = scrapy.Field()
    team_b = scrapy.Field()
    score_a = scrapy.Field()
    score_b = scrapy.Field()
    status = scrapy.Field()

    class config:
        team_a = "team_a"
        team_b = "team_b"
        score_a = "score_a"
        score_b = "score_b"
        status = "status"
