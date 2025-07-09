import unittest
from pyditto.options import DittoOptions

class TestDittoOptions(unittest.TestCase):
    def test_default_flags(self):
        opts = DittoOptions()
        self.assertEqual(
            set(opts.to_flags()),
            set()
        )

    def test_preserve_rsrc(self):
        opts = DittoOptions(preserve_rsrc=True)
        self.assertIn('--rsrc', opts.to_flags())
        opts = DittoOptions(preserve_rsrc=False)
        self.assertIn('--norsrc', opts.to_flags())

    def test_extattr(self):
        opts = DittoOptions(extattr=True)
        self.assertIn('--extattr', opts.to_flags())
        opts = DittoOptions(extattr=False)
        self.assertIn('--noextattr', opts.to_flags())

    def test_qtn(self):
        opts = DittoOptions(qtn=True)
        self.assertIn('--qtn', opts.to_flags())
        opts = DittoOptions(qtn=False)
        self.assertIn('--noqtn', opts.to_flags())

    def test_acl(self):
        opts = DittoOptions(acl=True)
        self.assertIn('--acl', opts.to_flags())
        opts = DittoOptions(acl=False)
        self.assertIn('--noacl', opts.to_flags())

    def test_nocache(self):
        opts = DittoOptions(nocache=True)
        self.assertIn('--nocache', opts.to_flags())

    def test_hfs_compression(self):
        opts = DittoOptions(hfs_compression=True)
        self.assertIn('--hfsCompression', opts.to_flags())
        opts = DittoOptions(hfs_compression=False)
        self.assertIn('--nohfsCompression', opts.to_flags())

    def test_preserve_hfs_compression(self):
        opts = DittoOptions(preserve_hfs_compression=True)
        self.assertIn('--preserveHFSCompression', opts.to_flags())
        opts = DittoOptions(preserve_hfs_compression=False)
        self.assertIn('--nopreserveHFSCompression', opts.to_flags())

    def test_arch(self):
        opts = DittoOptions(arch='x86_64')
        self.assertIn('--arch', opts.to_flags())
        self.assertIn('x86_64', opts.to_flags())

    def test_bom(self):
        opts = DittoOptions(bom='test.bom')
        self.assertIn('--bom', opts.to_flags())
        self.assertIn('test.bom', opts.to_flags())

    def test_verbose(self):
        opts = DittoOptions(verbose=True)
        self.assertIn('-V', opts.to_flags())

    def test_zlib_compression_level(self):
        opts = DittoOptions(zlib_compression_level=9)
        self.assertIn('--zlibCompressionLevel', opts.to_flags())
        self.assertIn('9', opts.to_flags())

    def test_keep_parent(self):
        opts = DittoOptions(keep_parent=True)
        self.assertIn('--keepParent', opts.to_flags(for_mode="archive"))
        self.assertNotIn('--keepParent', opts.to_flags(for_mode="copy"))
        self.assertNotIn('--keepParent', opts.to_flags(for_mode="extract"))

    def test_sequester_rsrc(self):
        opts = DittoOptions(sequester_rsrc=True)
        self.assertIn('--sequesterRsrc', opts.to_flags(for_mode="archive"))
        self.assertNotIn('--sequesterRsrc', opts.to_flags(for_mode="copy"))
        self.assertNotIn('--sequesterRsrc', opts.to_flags(for_mode="extract"))

    def test_zip_format(self):
        opts = DittoOptions(zip_format=True)
        self.assertIn('-k', opts.to_flags())

if __name__ == '__main__':
    unittest.main()
