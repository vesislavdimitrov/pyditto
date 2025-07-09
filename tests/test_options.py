import unittest
from pyditto.options import DittoOptions

class TestDittoOptions(unittest.TestCase):
    def test_default_flags(self):
        opts = DittoOptions()
        self.assertEqual(opts.to_flags(), [])

    def test_preserve_rsrc(self):
        opts = DittoOptions(preserve_rsrc=True)
        self.assertEqual(opts.to_flags(), ['--rsrc'])
        opts = DittoOptions(preserve_rsrc=False)
        self.assertEqual(opts.to_flags(), ['--norsrc'])

    def test_extattr(self):
        opts = DittoOptions(extattr=True)
        self.assertEqual(opts.to_flags(), ['--extattr'])
        opts = DittoOptions(extattr=False)
        self.assertEqual(opts.to_flags(), ['--noextattr'])

    def test_qtn(self):
        opts = DittoOptions(qtn=True)
        self.assertEqual(opts.to_flags(), ['--qtn'])
        opts = DittoOptions(qtn=False)
        self.assertEqual(opts.to_flags(), ['--noqtn'])

    def test_acl(self):
        opts = DittoOptions(acl=True)
        self.assertEqual(opts.to_flags(), ['--acl'])
        opts = DittoOptions(acl=False)
        self.assertEqual(opts.to_flags(), ['--noacl'])

    def test_nocache(self):
        opts = DittoOptions(nocache=True)
        self.assertEqual(opts.to_flags(), ['--nocache'])

    def test_hfs_compression(self):
        opts = DittoOptions(hfs_compression=True)
        self.assertEqual(opts.to_flags(), ['--hfsCompression'])
        opts = DittoOptions(hfs_compression=False)
        self.assertEqual(opts.to_flags(), ['--nohfsCompression'])

    def test_preserve_hfs_compression(self):
        opts = DittoOptions(preserve_hfs_compression=True)
        self.assertEqual(opts.to_flags(), ['--preserveHFSCompression'])
        opts = DittoOptions(preserve_hfs_compression=False)
        self.assertEqual(opts.to_flags(), ['--nopreserveHFSCompression'])

    def test_arch(self):
        opts = DittoOptions(arch='x86_64')
        self.assertEqual(opts.to_flags(), ['--arch', 'x86_64'])

    def test_bom(self):
        opts = DittoOptions(bom='test.bom')
        self.assertEqual(opts.to_flags(), ['--bom', 'test.bom'])

    def test_verbose(self):
        opts = DittoOptions(verbose=True)
        self.assertEqual(opts.to_flags(), ['-V'])

    def test_zlib_compression_level(self):
        opts = DittoOptions(zlib_compression_level=9)
        self.assertEqual(opts.to_flags(), ['--zlibCompressionLevel', '9'])

    def test_keep_parent(self):
        opts = DittoOptions(keep_parent=True)
        self.assertEqual(opts.to_flags(for_mode="archive"), ['--keepParent'])
        self.assertNotIn('--keepParent', opts.to_flags(for_mode="copy"))
        self.assertNotIn('--keepParent', opts.to_flags(for_mode="extract"))

    def test_sequester_rsrc(self):
        opts = DittoOptions(sequester_rsrc=True)
        self.assertEqual(opts.to_flags(for_mode="archive"), ['--sequesterRsrc'])
        self.assertNotIn('--sequesterRsrc', opts.to_flags(for_mode="copy"))
        self.assertNotIn('--sequesterRsrc', opts.to_flags(for_mode="extract"))

    def test_zip_format(self):
        opts = DittoOptions(zip_format=True)
        self.assertEqual(opts.to_flags(), ['-k'])

if __name__ == '__main__':
    unittest.main()
