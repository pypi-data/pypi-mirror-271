# Huffify
![PyPI - Version](https://img.shields.io/pypi/v/huffify?style=for-the-badge&color=green)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![PyPI - Format](https://img.shields.io/pypi/format/huffify?style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/munwriter/Huffify/test-lint.yml?style=for-the-badge)


## Description
Huffify allows you to compress text using Huffman algorithm. Huffify focus on flexibility - you can choose various encoders, huffman tree nodes and file managers to rich the best compressing quality
> Historical note: The Huffman algorithm was developed by David A. Huffman in 1952. [Read more about David and his algorithm](https://ru.wikipedia.org/wiki/Код_Хаффмана)

## Usage
Basic usage
```python
from huffify import HuffmanCodec
from huffify.heapNodes import Node, LexicographicNode
from huffify.encoders import MVPEncoder

# You can use LexicographicNode that provide idempotent result and another encoder.
# Now this node and encoder set as default attributes 
codec = HuffmanCodec(node=Node, encoder=MVPEncoder)
message = "The sun shines bright today."

# Here is the "FinalDataSet", which can be saved as file
encoded_message = codec.encode(message)

# Also you can decode this "FinalDataSet" to get original message
decoded_message = codec.decode(encoded_message)
```
Advanced usage
```python
from huffify import Huffify
from huffify.fileManager import Picklefier

# You can pass preferred writing into file strategy
# It's only one yet and it thrown into Huffify as default strategy
file_compressor = Huffify(file_manager=Picklefier)

# You can save your compressed message into file
file_compressor.save(path="output", message="The sun shines bright today.")

# And also load and decompress it
decoded_message = file_compressor.load(path="output")

```
Watch encoding table
```python
from huffify import HuffmanCodec

codec = HuffmanCodec()
message = "The sun shines bright today."

# If you want get encoding table as dict
encoding_table = codec._get_encoding_table(message)

# Also you can print the encoding at representative view
codec.print_encoding_table(message)

```

## Installation
Using pip
```
pip install huffify
```
Using poetry
```
poetry add huffify
```
