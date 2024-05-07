# File Finder

This command-line tool searches for files using specific criteria within a given directory.

## Installation

Before using the tool, make sure you have Python installed. Then, install the required dependencies:

```bash
pip install ffinder
```

## Usage

```bash
ffinder --help
```

- `[PATH]`: (optional) Path to the directory to search in. If not provided, the current directory will be used.
- `-k, --key`: **Required**. Define a search key.
- `-v, --value`: **Required**. Define a search value.
- `-r, --recursive`: (optional) Perform a recursive search within subdirectories. Default is non-recursive.
- `-s, --save`: (optional) Save a report in the current directory.
- `-c, --copy-to`: (optional) Copy found files to the specified directory.

## Example

```bash
ffinder -k ext -v .zip -r -s -c /zips
```

This command will search for all files named "example.txt" recursively starting from the current directory. It will save a report in the current directory and copy the found files to `/path/to/copy`.

## Supported Search Keys

- `name`: Search files by name.
- `extension`: Search files by extension.
- `date modified`: Search files by last modified date.

## Notes

- If no path is provided, the tool will search in the current directory.
- If multiple files with the same name are found during copy operation, the tool will append a timestamp to the copied file's name to avoid overwriting.

## Credits

This tool uses `click` for command-line interface, `tabulate` for tabular data formatting, and `pathlib` for file operations.