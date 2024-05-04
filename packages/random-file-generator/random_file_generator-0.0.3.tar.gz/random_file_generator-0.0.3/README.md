# Random File Generator

This Python package allows you to generate multiple random text files concurrently.

## Installation

You can install the package using pip:

```bash
pip install random-file-generator

## generate_files_parallel

Generates random text files concurrently using multiprocessing.

### Parameters

- `number_of_files`: Number of files to generate.
- `output_folder`: Output folder path.
- `min_file_size`: Minimum size of the files (in bytes).
- `max_file_size`: Maximum size of the files (in bytes).

## Example

```python
import random_file_generator

number_of_files = 5
output_folder = 'random_files'
min_file_size = 1024  # 1 KB
max_file_size = 1048576  # 1 MB

# Generate random files concurrently
random_file_generator.generate_files_parallel(number_of_files, output_folder, min_file_size, max_file_size)