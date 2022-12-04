from pathlib import Path

from core.managers import FileManager
from scrapers.items import MatchDetail, MatchUrl


class MatchPipeline:

    directory_mapping_by_class = {
        MatchUrl: Path("/data/match_url"),
        MatchDetail: Path("/data/match_detail"),
    }

    async def get_directory_path(self, item, join_element=None):
        mapping_element = self.directory_mapping_by_class.get(item.__class__)
        if join_element is None:
            return mapping_element
        return mapping_element.joinpath(join_element)

    async def process_item(self, item, spider):
        unfetched_directory_path = await self.get_directory_path(
            item, join_element="unfetched"
        )
        await FileManager.write_to_pickle_file(
            directory_path=unfetched_directory_path,
            file_name=item.file_name,
            data=item,
        )
