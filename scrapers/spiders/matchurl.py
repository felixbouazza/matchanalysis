import scrapy

from core.managers import DateManager
from match.models.enum import MatchStatus
from scrapers.items import MatchUrl


class MatchurlsSpider(scrapy.Spider):
    name = "matchurl"
    allowed_domains = ["matchendirect.fr"]
    base_url = "https://www.matchendirect.fr/resultat-foot-"

    def start_requests(self):
        # This two arguments have to be passed to crawl command with -a argument
        # Exemple: scrapy crawl matchurls -a start_date="01-08-2021" -a end_date="01-08-2022"
        start_date = getattr(self, "start_date", None)
        end_date = getattr(self, "end_date", None)

        if not start_date or not end_date:
            raise ValueError(
                "Missing one or two of this command arguments: start_date / end_date"
            )

        dates_to_crawl = DateManager.generate_date_between_two_dates(
            start_date=start_date, end_date=end_date
        )

        for date in dates_to_crawl:
            yield scrapy.Request(
                f"{self.base_url}{date}/",
                self.parse,
                cb_kwargs={"match_date": date},
            )

    async def parse(self, response, match_date):
        file_name = f"{match_date}.pickle"
        championship_divs = response.xpath('//div[@class="panel panel-info"]')
        for championship_div in championship_divs:

            match_trs = championship_div.xpath(".//tr")
            for match_tr in match_trs:

                match_status = match_tr.xpath('.//td[@class="lm2 lm2_0"]//text()')[
                    1
                ].get()

                if match_status in MatchStatus.get_unplayed_status():
                    continue

                match_id = match_tr.xpath(".//@data-matchid").get()
                match_url = match_tr.xpath('.//td[@class="lm3"]//a/@href').get()

                yield MatchUrl(
                    file_name=file_name,
                    match_id=match_id,
                    match_url=match_url,
                    match_status=match_status,
                )
