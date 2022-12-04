import asyncio
import pickle
import shutil
from pathlib import Path


class FileManager:
    @classmethod
    async def write_to_pickle_file(cls, directory_path, file_name, data):
        directory_path.mkdir(parents=True, exist_ok=True)
        file_full_path = directory_path.joinpath(file_name)

        with open(file_full_path, "ab") as pickle_file:
            pickle.dump(data, pickle_file)

    @classmethod
    async def move_file(cls, old_file_path, new_directory):
        new_directory_path = Path(new_directory)
        new_directory_path.mkdir(parents=True, exist_ok=True)
        new_file_path = new_directory_path.joinpath(old_file_path.name)
        shutil.move(old_file_path, new_file_path)


if __name__ == "__main__":
    asyncio.run(FileManager.move_file(Path("./data/file.js"), "./data/fetched"))
