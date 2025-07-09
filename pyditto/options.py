from typing import Optional, List, Dict, Any

class DittoOptions:
    # Options matching ditto manual page
    def __init__(
        self,
        preserve_rsrc: Optional[bool] = None,
        extattr: Optional[bool] = None,
        qtn: Optional[bool] = None,
        acl: Optional[bool] = None,
        nocache: bool = False,
        hfs_compression: Optional[bool] = None,
        preserve_hfs_compression: Optional[bool] = None,
        arch: Optional[str] = None,
        bom: Optional[str] = None,
        verbose: bool = False,
        zlib_compression_level: Optional[int] = None,
        password: Optional[str] = None,
        keep_parent: bool = True,
        sequester_rsrc: bool = True,
        zip_format: bool = True
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
        flag_map: Dict[str, Any] = {
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
            "keep_parent": {True: "--keepParent"},
            "sequester_rsrc": {True: "--sequesterRsrc"},
            "zip_format": {True: "-k"}
        }
        flags: List[str] = []
        for key, value in self.__dict__.items():
            if key in ("arch", "bom", "zlib_compression_level", "password"):
                flags.extend(flag_map[key](value))
                continue
            flag_entry = flag_map.get(key)
            if isinstance(flag_entry, dict):
                flag = flag_entry.get(value)
                flag and flags.append(flag)
        if self.verbose:
            flags.append("-V")
        return flags
