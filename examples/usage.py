from pyditto import copy, archive, extract, DittoOptions, PyDitto

# Functional usage: Copy a directory with all metadata
copy('source_folder', 'destination_folder', DittoOptions(preserve_rsrc=True, extattr=True, qtn=True, acl=True, verbose=True))

# Functional usage: Copy without resource forks or metadata
copy('source_folder', 'destination_folder2', DittoOptions(preserve_rsrc=False, extattr=False, qtn=False, acl=False, verbose=True))

# Functional usage: Create a zip archive with max compression
archive('source_folder', 'archive.zip', DittoOptions(zip_format=True, keep_parent=True, sequester_rsrc=True, verbose=True, zlib_compression_level=9))

# Functional usage: Extract a zip archive
extract('archive.zip', 'extracted_folder', DittoOptions(zip_format=True, verbose=True))

# OOP usage: Using PyDitto directly
options = DittoOptions(preserve_rsrc=True, verbose=True)
PyDitto.copy('src', 'dst', options)
