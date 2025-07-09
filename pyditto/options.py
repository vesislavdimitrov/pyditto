from typing import Optional, List, Dict, Any

class DittoOptions:
    # Options matching ditto manual page
    def __init__(
        self,
        preserve_rsrc: Optional[bool] = None,
        extattr: Optional[bool] = None,
        qtn: Optional[bool] = None,
        acl: Optional[bool] = None,
        nocache: Optional[bool] = None,
        hfs_compression: Optional[bool] = None,
        preserve_hfs_compression: Optional[bool] = None,
        arch: Optional[str] = None,
        bom: Optional[str] = None,
        verbose: Optional[bool] = None,
        zlib_compression_level: Optional[int] = None,
        password: Optional[str] = None,
        keep_parent: Optional[bool] = None,
        sequester_rsrc: Optional[bool] = None,
        zip_format: Optional[bool] = None
    ):
        self.preserve_rsrc = preserve_rsrc
        self.extattr = extattr
        self.qtn = qtn
        self.acl = acl
        self.nocache = nocache
        self.hfs_compression = hfs_compression
        self.preserve_hfs_compression = preserve_hfs_compression
        self.arch = arch
        self.bom = bom
        self.verbose = verbose
        self.zlib_compression_level = zlib_compression_level
        self.password = password
        self.keep_parent = keep_parent
        self.sequester_rsrc = sequester_rsrc
        self.zip_format = zip_format

    def to_flags(self, for_mode: str = "copy") -> List[str]:
        flags: List[str] = []
        for key, value in self.__dict__.items():
            if key in ("keep_parent", "sequester_rsrc"):
                flags.extend(self._archive_only_flag(key, value, for_mode))
            else:
                flags.extend(self._generic_flag(key, value))
        if self.verbose:
            flags.append("-V")
        return flags

    def _archive_only_flag(self, key: str, value: Any, for_mode: str) -> list:
        archive_only_flags = {
            "keep_parent": {True: "--keepParent"},
            "sequester_rsrc": {True: "--sequesterRsrc"}
        }
        if key in archive_only_flags and for_mode == "archive":
            flag = archive_only_flags[key].get(value)
            return [flag] if flag else []
        return []

    def _generic_flag(self, key: str, value: Any) -> list:
        flag_map = {
            "preserve_rsrc": {True: "--rsrc", False: "--norsrc"},
            "extattr": {True: "--extattr", False: "--noextattr"},
            "qtn": {True: "--qtn", False: "--noqtn"},
            "acl": {True: "--acl", False: "--noacl"},
            "nocache": {True: "--nocache"},
            "hfs_compression": {True: "--hfsCompression", False: "--nohfsCompression"},
            "preserve_hfs_compression": {True: "--preserveHFSCompression", False: "--nopreserveHFSCompression"},
            "arch": lambda v: ["--arch", v] if v else [],
            "bom": lambda v: ["--bom", v] if v else [],
            "zlib_compression_level": lambda v: ["--zlibCompressionLevel", str(v)] if v is not None else [],
            "password": lambda v: ["--password", v] if v else [],
            "zip_format": {True: "-k"}
        }
        if key in ("arch", "bom", "zlib_compression_level", "password"):
            return flag_map[key](value)
        flag_entry = flag_map.get(key)
        if isinstance(flag_entry, dict):
            flag = flag_entry.get(value)
            return [flag] if flag else []
        return []