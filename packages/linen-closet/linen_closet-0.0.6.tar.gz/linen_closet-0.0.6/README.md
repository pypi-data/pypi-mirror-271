# Linen Closet

This module is designed to provide a standalone CLI and Python package to bulk-download Google Sheets to a single JSON file.

#### Why would I use this?
- You have a large number of Google Sheets that you want to download and use in a single application
- You want to cache the data from Google Sheets to avoid hitting the Google Sheets API rate limits

#### Why wouldn't I use this?
- You don't have a large number of Google Sheets to download. You're probably better off using the Google Sheets API directly.
- You need more control over which data is pulled back from Google Sheets. This includes either filtering for only specific values, or dynamically pulling back a specific set of sheets based on some criteria.

## Installation

```bash
pip install linen-closet
```

## Usage

### Python Package

```python
from linen_closet import load_sheets, S3Configuration

load_sheets(
    credentials_file: str = "credentials.json",  # Likely a Google Service Account Credentials file in JSON format
    output_filename: str = "workbook.json",  # Where to write the JSON file
    max_download_concurrency: int = 10,  # How many concurrent downloads to run
    configuration_filename: str = "sheets.yaml",  # A YAML file containing the sheets to download (see example in repo root)
    cache_file: Optional[str] = None,  # An existing output file. If provided, will only download sheets that have changed since the last download. All sheet data will be included in the output file (cached data will be copied over)
    s3_configuration: Optional[S3Configuration] = None,  # If provided, and either `output_filename` or `cache_file` is an S3 URL, will perform actions against the S3 bucket specified here
)
```

### CLI

_Pre-built binaries are available on the [Releases](https://github.com/nvdnc/linen-closet/releases) page._    

__Help Text__

```
Usage: linen_closet [OPTIONS]

Options:
  -o, --output-filename <OUTPUT_FILENAME>
          Output file name [default: workbooks.json]
  -m, --max-download-concurrency <MAX_DOWNLOAD_CONCURRENCY>
          Max download concurrency [default: 50]
  -s, --sheet-configuration <SHEET_CONFIGURATION>
          Sheet configuration [default: sheets.yaml]
  -c, --credentials-file-path <CREDENTIALS_FILE_PATH>
          Credentials file path [default: credentials.json]
  -e, --existing-file <EXISTING_FILE>
          Existing file to read from
  -h, --help
          Print help
  -V, --version
          Print version
```

__Example__

```bash
linen_closet \
    --credentials-file-path credentials.json \
    --output-filename workbooks.json \
    --sheet-configuration sheets.yaml \
    --max-download-concurrency 50
```

## License

[Apache 2.0](LICENSE)
