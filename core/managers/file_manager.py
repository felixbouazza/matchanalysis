import pickle
from pathlib import Path


class FileManager:
    @classmethod
    async def write_to_pickle_file(cls, directory_path, file_name, data):
        directory_path = Path(directory_path)
        directory_path.mkdir(parents=True, exist_ok=True)
        file_full_path = directory_path.joinpath(file_name)

        with open(file_full_path, "ab") as file:
            pickle.dump(data, file)
