import heapq
from collections import Counter
from pathlib import Path
from typing import Type

from huffify.abstract import IEncoder, INode, IPersistenceManager
from huffify.annotations import FinalDataSet
from huffify.encoders import MVPEncoder
from huffify.fileManger import Picklefier
from huffify.heapNodes import Node


class HuffmanCodec:
    def __init__(
        self,
        node: Type[INode] = Node,
        encoder: Type[IEncoder] = MVPEncoder,
    ) -> None:
        self.__HeapNode = node
        self.encoder: IEncoder = encoder()

    @staticmethod
    def __define_char_frequency(message: str) -> Counter[str]:
        return Counter(message)

    def print_encoding_table(self, message: str, reverse: bool = False) -> None:
        # TODO add sys.stout
        encoding_table = self._get_encoding_table(message)
        encoding_table = dict(
            sorted(encoding_table.items(), key=lambda x: (len(x[1]), x[1]), reverse=reverse)
        )
        [print(_) for _ in HuffmanCodec.__format(encoding_table)]

    @staticmethod
    def __format(encoding_table: dict[str, str]) -> list[str]:
        if not encoding_table:
            return []
        lines: list[str] = []
        for char, code in encoding_table.items():
            lines.append(f'"{char}" {code}')
        return lines

    def _get_encoding_table(self, message: str) -> dict[str, str]:
        if len(message) == 1:
            return {char: "1" for char in message}
        chars_frequency = HuffmanCodec.__define_char_frequency(message)
        heap = [self.__HeapNode(key, chars_frequency[key]) for key in chars_frequency]
        heapq.heapify(heap)
        encoding_table = {char: "" for char in message}
        while len(heap) > 1:
            low = heapq.heappop(heap)
            hight = heapq.heappop(heap)
            for i in hight.char:
                encoding_table[i] += "0"
            for i in low.char:
                encoding_table[i] += "1"
            hight += low
            heapq.heappush(heap, hight)
        encoding_table = {char: encoding_table[char][::-1] for char in encoding_table}
        return encoding_table

    def encode(self, message: str) -> FinalDataSet:
        encoding_table = self._get_encoding_table(message)
        encoded_message = self.encoder.encode_string(encoding_table, message)
        final_data_set = FinalDataSet(
            table=encoding_table,
            message=encoded_message,
        )
        return final_data_set

    def decode(self, encoded_data: FinalDataSet) -> str:
        encoding_table, encoded_message = encoded_data.get("table"), encoded_data.get(
            "message"
        )
        decoded_message = self.encoder.decode_string(encoding_table, encoded_message)
        return decoded_message


class Huffify(HuffmanCodec):
    def __init__(
        self,
        node: Type[INode] = Node,
        encoder: Type[IEncoder] = MVPEncoder,
        file_manager: Type[IPersistenceManager] = Picklefier,
    ) -> None:
        super().__init__(node, encoder)
        self.file_manager: IPersistenceManager = file_manager()

    def save(self, path: str | Path, message: str) -> None:
        encoded_dataset = self.encode(message)
        self.file_manager.save(path, encoded_dataset)

    def load(self, path: str | Path) -> str:
        encoded_dataset = self.file_manager.load(path)
        decoded_message = self.decode(encoded_dataset)
        return decoded_message
