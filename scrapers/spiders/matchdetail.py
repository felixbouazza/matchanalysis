import logging
import pickle
from decimal import Decimal
from pathlib import Path

import dateparser
import scrapy

from core.managers import FileManager
from scrapers.items import MatchDetail

logger = logging.getLogger(__name__)


class MatchdetailSpider(scrapy.Spider):
    name = "matchdetail"
    allowed_domains = ["matchendirect.fr"]
    base_url = "https://www.matchendirect.fr"
    unfetched_directory_path = "/data/match_url/unfetched"

    def start_requests(self):
        directory_path = Path(self.unfetched_directory_path)
        for match_url_file_path in directory_path.iterdir():
            with open(match_url_file_path, "rb") as match_url_file:
                try:
                    while match := pickle.load(match_url_file):
                        match_url = f"{self.base_url}{match.match_url}"
                        yield scrapy.Request(
                            match_url,
                            self.parse,
                            meta={"playwright": True, "playwright_include_page": True},
                            cb_kwargs={"match": match},
                            errback=self.close_page,
                        )
                except EOFError:
                    logger.info(f"File {match_url_file_path} finished...")
            FileManager.move_file(
                old_file_path=match_url_file_path,
                new_directory="/data/match_url/fetched",
            )

    async def close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    async def get_match_datetime(self, match_detail):
        match_date_div = match_detail.xpath('.//div[@class="info1"]//text()')
        match_date = match_date_div.get()
        match_hour = match_date_div[1].get()
        return dateparser.parse(f"{match_date}{match_hour}")

    async def get_match_teams(self, match_detail):
        team_rows = match_detail.xpath(
            './/div[@class="row team-logo"]//div[@class="col-xs-4 text-center"]//@title'
        ).getall()
        return team_rows[0], team_rows[1]

    async def get_match_scores(self, match_detail):
        scores = match_detail.xpath('.//span[@class="score"]//text()').getall()
        return scores[0], scores[1]

    async def get_match_championship_and_country(self, match_menu_haut):
        country_name = match_menu_haut.xpath(".//li[2]//a//text()").get()
        championship_name = match_menu_haut.xpath(".//li[3]//a//text()").get()
        return country_name, championship_name

    async def get_comment_number(self, page):
        comment_number_locator = page.locator('//div[@id="bloc_nb_commenaire"]//a')
        comment_number = await comment_number_locator.text_content()
        if "Publier" in comment_number:
            return 0
        return int(comment_number.replace("commentaires", "").replace(" ", ""))

    async def get_match_ratings(self, page):
        cotes = page.locator('//div[@id="myTabMatchContent"]//span[@class="c2"]')

        if not await cotes.count():
            return False, None, None, None

        text_cotes = await cotes.all_text_contents()
        return (
            True,
            Decimal(text_cotes[0]),
            Decimal(text_cotes[1]),
            Decimal(text_cotes[2]),
        )

    async def parse(self, response, match):

        ############
        # RESPONSE #
        ############

        match_detail = response.xpath('//div[@class="jumbotron"]')

        match_datetime = await self.get_match_datetime(match_detail=match_detail)

        home_team, outside_team = await self.get_match_teams(match_detail=match_detail)

        home_team_score, outside_team_score = await self.get_match_scores(
            match_detail=match_detail
        )

        match_menu_haut = response.xpath('//ol[@class="breadcrumb"]')
        country_name, championship_name = await self.get_match_championship_and_country(
            match_menu_haut=match_menu_haut
        )

        # ########## #
        # PLAYWRIGHT #
        # ########## #

        page = response.meta["playwright_page"]

        comment_number = await self.get_comment_number(page=page)

        (
            has_rating,
            home_team_rating,
            draw_rating,
            outside_team_rating,
        ) = await self.get_match_ratings(page=page)

        await page.close()

        yield MatchDetail(
            file_name=match.file_name,
            match_id=match.match_id,
            match_url=match.match_url,
            match_status=match.match_status,
            match_datetime=match_datetime,
            home_team=home_team,
            outside_team=outside_team,
            home_team_score=home_team_score,
            outside_team_score=outside_team_score,
            has_rating=has_rating,
            home_team_rating=home_team_rating,
            draw_rating=draw_rating,
            outside_team_rating=outside_team_rating,
            championship_name=championship_name,
            country_name=country_name,
            comment_number=comment_number,
        )
