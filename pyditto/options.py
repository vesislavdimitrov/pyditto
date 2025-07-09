from typing import List

class DittoOption:
    def __init__(self, flag_logic, archive_only=False):
        self.flag_logic = flag_logic
        self.archive_only = archive_only
        self.private_name = None

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

    def to_flag(self, value):
        if callable(self.flag_logic):
            return self.flag_logic(value)
        elif isinstance(self.flag_logic, dict):
            flag = self.flag_logic.get(value)
            return [flag] if flag else []
        return []

class DittoOptions:
    preserve_rsrc = DittoOption({True: "--rsrc", False: "--norsrc"})
    extattr = DittoOption({True: "--extattr", False: "--noextattr"})
    qtn = DittoOption({True: "--qtn", False: "--noqtn"})
    acl = DittoOption({True: "--acl", False: "--noacl"})
    nocache = DittoOption({True: "--nocache"})
    hfs_compression = DittoOption({True: "--hfsCompression", False: "--nohfsCompression"})
    preserve_hfs_compression = DittoOption({True: "--preserveHFSCompression", False: "--nopreserveHFSCompression"})
    arch = DittoOption(lambda v: ["--arch", v] if v else [])
    bom = DittoOption(lambda v: ["--bom", v] if v else [])
    verbose = DittoOption({True: "-V"})
    zlib_compression_level = DittoOption(lambda v: ["--zlibCompressionLevel", str(v)] if v is not None else [])
    password = DittoOption(lambda v: ["--password", v] if v else [])
    keep_parent = DittoOption({True: "--keepParent"}, archive_only=True)
    sequester_rsrc = DittoOption({True: "--sequesterRsrc"}, archive_only=True)
    zip_format = DittoOption({True: "-k"})

    def __init__(self, **kwargs):
        for name in self.option_names():
            setattr(self, name, kwargs.get(name, None))

    @classmethod
    def option_names(cls):
        return [k for k, v in cls.__dict__.items() if isinstance(v, DittoOption)]

    def to_flags(self, for_mode: str = "copy") -> List[str]:
        flags: List[str] = []
        for name in self.option_names():
            opt: DittoOption = getattr(self.__class__, name)
            value = getattr(self, name)
            if opt.archive_only and for_mode != "archive":
                continue
            flags.extend(opt.to_flag(value))
        return flags
        