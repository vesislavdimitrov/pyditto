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

    def _add_prefix(self, flag):
        if not flag or not isinstance(flag, str):
            return flag
        if flag.startswith('-'):
            return flag
        return f'-{flag}' if len(flag) == 1 else f'--{flag}'

    def to_flag(self, value):
        if callable(self.flag_logic):
            flags = self.flag_logic(value)
            if isinstance(flags, list):
                return [self._add_prefix(f) if i == 0 else f for i, f in enumerate(flags)]
            return []

        if isinstance(self.flag_logic, dict):
            flag = self.flag_logic.get(value)
            return [self._add_prefix(flag)] if flag else []
        return []

class DittoOptions:
    preserve_rsrc = DittoOption({True: 'rsrc', False: 'norsrc'})
    extattr = DittoOption({True: 'extattr', False: 'noextattr'})
    qtn = DittoOption({True: 'qtn', False: 'noqtn'})
    acl = DittoOption({True: 'acl', False: 'noacl'})
    nocache = DittoOption({True: 'nocache'})
    hfs_compression = DittoOption({True: 'hfsCompression', False: 'nohfsCompression'})
    preserve_hfs_compression = DittoOption({True: 'preserveHFSCompression', False: 'nopreserveHFSCompression'})
    arch = DittoOption(lambda v: ['arch', v] if v else [])
    bom = DittoOption(lambda v: ['bom', v] if v else [])
    verbose = DittoOption({True: 'V'})
    zlib_compression_level = DittoOption(lambda v: ['zlibCompressionLevel', str(v)] if v is not None else [])
    keep_parent = DittoOption({True: 'keepParent'}, archive_only=True)
    sequester_rsrc = DittoOption({True: 'sequesterRsrc'}, archive_only=True)
    zip_format = DittoOption({True: 'k'})

    def __init__(self, **args):
        for name in self.option_names():
            setattr(self, name, args.get(name, None))

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