import unittest
from unittest.mock import patch
from pyditto.ditto import PyDitto, copy, archive, extract, DittoOptions

class TestPyDitto(unittest.TestCase):
    @patch('pyditto.ditto.run_ditto')
    def test_copy_default(self, mock_run):
        PyDitto.copy('src', 'dst')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        for expected in ['src', 'dst']:
            self.assertIn(expected, args)

    @patch('pyditto.ditto.run_ditto')
    def test_archive_default(self, mock_run):
        PyDitto.archive('src', 'archive.zip')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        for expected in ['-c', 'src', 'archive.zip']:
            self.assertIn(expected, args)

    @patch('pyditto.ditto.run_ditto')
    def test_extract_default(self, mock_run):
        PyDitto.extract('archive.zip', 'dst')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        for expected in ['-x', 'archive.zip', 'dst']:
            self.assertIn(expected, args)

    @patch('pyditto.ditto.run_ditto')
    def test_all_options_copy(self, mock_run):
        opts = DittoOptions(
            preserve_rsrc=True,
            extattr=True,
            qtn=True,
            acl=True,
            nocache=True,
            hfs_compression=True,
            preserve_hfs_compression=True,
            arch='x86_64',
            bom='test.bom',
            verbose=True,
            zlib_compression_level=9,
            password='secret',
            keep_parent=True,
            sequester_rsrc=True,
            zip_format=True
        )
        copy('src', 'dst', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_flags = [
            '--rsrc', '--extattr', '--qtn', '--acl', '--nocache', '--hfsCompression',
            '--preserveHFSCompression', '--arch', 'x86_64', '--bom', 'test.bom',
            '-V', '--zlibCompressionLevel', '9', '--password', 'secret',
            '--keepParent', '--sequesterRsrc', '-k'
        ]
        for flag in expected_flags:
            self.assertIn(flag, args)

    @patch('pyditto.ditto.run_ditto')
    def test_all_options_archive(self, mock_run):
        opts = DittoOptions(
            preserve_rsrc=False,
            extattr=False,
            qtn=False,
            acl=False,
            nocache=True,
            hfs_compression=False,
            preserve_hfs_compression=False,
            arch='arm64',
            bom='archive.bom',
            verbose=True,
            zlib_compression_level=5,
            password='pw',
            keep_parent=True,
            sequester_rsrc=True,
            zip_format=True
        )
        archive('src', 'archive.zip', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_flags = [
            '--norsrc', '--noextattr', '--noqtn', '--noacl', '--nocache', '--nohfsCompression',
            '--nopreserveHFSCompression', '--arch', 'arm64', '--bom', 'archive.bom',
            '-V', '--zlibCompressionLevel', '5', '--password', 'pw',
            '--keepParent', '--sequesterRsrc', '-k'
        ]
        for flag in expected_flags:
            self.assertIn(flag, args)

    @patch('pyditto.ditto.run_ditto')
    def test_all_options_extract(self, mock_run):
        opts = DittoOptions(
            zip_format=True,
            verbose=True,
            password='pw',
        )
        extract('archive.zip', 'dst', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_flags = ['-x', '-k', '-V', '--password', 'pw', 'archive.zip', 'dst']
        for flag in expected_flags:
            self.assertIn(flag, args)

    def test_missing_src_copy(self):
        with self.assertRaises(TypeError):
            copy()

    def test_missing_dst_copy(self):
        with self.assertRaises(TypeError):
            copy('src')

    def test_missing_src_archive(self):
        with self.assertRaises(TypeError):
            archive()

    def test_missing_archive_path(self):
        with self.assertRaises(TypeError):
            archive('src')

    def test_missing_archive_extract(self):
        with self.assertRaises(TypeError):
            extract()

    def test_missing_dst_extract(self):
        with self.assertRaises(TypeError):
            extract('archive.zip')

    @patch('pyditto.ditto.run_ditto', side_effect=Exception('ditto failed'))
    def test_run_ditto_failure(self, mock_run):
        opts = DittoOptions()
        with self.assertRaises(Exception) as ctx:
            copy('src', 'dst', opts)
        self.assertIn('ditto failed', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
