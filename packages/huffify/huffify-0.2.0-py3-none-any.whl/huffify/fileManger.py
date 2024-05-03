import pickle
from pathlib import Path

from huffify.abstract import IPersistenceManager
from huffify.annotations import FinalDataSet


class PickleFileManager:
    def __init__(
        self,
        input_path: str | Path = "input.txt",
        output_path: str | Path = "output.txt",
        encoding: str = "utf-8",
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.encoding = encoding

    def save(self, encoded_data: FinalDataSet) -> None:
        with open(self.output_path, "wb", encoding=self.encoding) as f:
            pickle.dump(encoded_data, f)

    def load(self) -> FinalDataSet:
        with open(self.output_path, "rb", encoding=self.encoding) as f:
            data: FinalDataSet = pickle.load(f)
        return data


class Picklefier(IPersistenceManager):
    @staticmethod
    def save(path: str | Path, encoded_data: FinalDataSet) -> None:
        with open(path, "wb") as f:
            pickle.dump(encoded_data, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path: str | Path) -> FinalDataSet:
        with open(path, "rb") as f:
            data: FinalDataSet = pickle.load(f)
        return data
