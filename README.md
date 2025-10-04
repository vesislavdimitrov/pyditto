# pyditto

A Python library for programmatic access to the macOS [`ditto`](https://ss64.com/mac/ditto.html) tool.

Copy directory hierarchies, create and extract archives. Ditto can preserve ownership / permissions, HFS resource forks and file / folder metadata. Ditto will automatically create the destination folder if it doesn’t yet exist, if the destination does exist and contains files, then ditto will merge them.

## Features
- Copy files and directories with advanced metadata and options
- Create and extract ZIP/CPIO archives
- Control resource fork, extended attributes, ACLs, HFS+ compression, and more

## Example Usage
```python
from pyditto import copy, archive, extract

# Copy with all metadata
copy('src', 'dst', preserve_rsrc=True, extattr=True, qtn=True, acl=True)

# Copy without resource forks or metadata
copy('src', 'dst2', preserve_rsrc=False, extattr=False, qtn=False, acl=False)

# Create a zip archive with max compression
archive('src', 'archive.zip', zip_format=True, zlib_compression_level=9)

# Extract a zip archive
extract('archive.zip', 'dst')
```

## Options
- `preserve_rsrc`: Preserve resource forks and HFS meta-data
- `extattr`: Preserve extended attributes
- `qtn`: Preserve quarantine information
- `acl`: Preserve Access Control Lists
- `hfs_compression`: Use HFS+ compression (system files)
- `preserve_hfs_compression`: Preserve HFS+ compression
- `nocache`: Do not use the unified buffer cache
- `arch`: Thin universal binaries to the specified architecture
- `bom`: Copy only files present in the specified BOM
- `zlib_compression_level`: Set ZIP compression level (0-9)

*Note: This is not an exhaustive list of all possible `ditto` arguments. More options may be added in the future. If you need a specific flag, feel free to open a PR*

## Requirements
- macOS with `ditto` available in $PATH
- Python 3.7+

## Author
Vesislav Dimitrov