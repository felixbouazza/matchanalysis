from core.managers import FileManager

UNFETCHED_MATCH_URL_DATA_PATH = "/data/match_url/unfetched"


class MatchUrlPipeline:
    async def process_item(self, item, spider):
        await FileManager.write_to_pickle_file(
            directory_path=UNFETCHED_MATCH_URL_DATA_PATH,
            file_name=item.file_name,
            data=item,
        )
