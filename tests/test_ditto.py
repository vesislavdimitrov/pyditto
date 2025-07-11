import unittest
from unittest.mock import patch
from pyditto.ditto import PyDitto, copy, archive, extract, DittoOptions

class TestPyDitto(unittest.TestCase):
    @patch('shutil.which', return_value=None)
    def test_missing_ditto_command(self, mock_which):
        from pyditto.ditto import MISSING_DITTO_ERROR
        with self.assertRaises(FileNotFoundError) as ctx:
            PyDitto.copy('src', 'dst')
        self.assertIn(MISSING_DITTO_ERROR, str(ctx.exception))

    @patch('pyditto.ditto.run_ditto')
    def test_copy_default(self, mock_run):
        PyDitto.copy('src', 'dst')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ['src', 'dst'])

    @patch('pyditto.ditto.run_ditto')
    def test_archive_default(self, mock_run):
        PyDitto.archive('src', 'archive.zip')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ['-c', 'src', 'archive.zip'])

    @patch('pyditto.ditto.run_ditto')
    def test_extract_default(self, mock_run):
        PyDitto.extract('archive.zip', 'dst')
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ['-x', 'archive.zip', 'dst'])

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
            keep_parent=True,
            sequester_rsrc=True,
            zip_format=True
        )
        copy('src', 'dst', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_args = [
            '--rsrc', '--extattr', '--qtn', '--acl', '--nocache', '-V', '-k', '--hfsCompression', '--preserveHFSCompression', '--arch', 'x86_64', '--bom', 'test.bom', '--zlibCompressionLevel', '9', 'src', 'dst'
        ]
        self.assertEqual(args, expected_args)

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
            keep_parent=True,
            sequester_rsrc=True,
            zip_format=True
        )
        archive('src', 'archive.zip', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_args = [
            '-c', '--norsrc', '--noextattr', '--noqtn', '--noacl', '--nocache', '-V', '-k', '--nohfsCompression', '--nopreserveHFSCompression', '--arch', 'arm64', '--bom', 'archive.bom', '--zlibCompressionLevel', '5', '--keepParent', '--sequesterRsrc', 'src', 'archive.zip'
        ]
        self.assertEqual(args, expected_args)

    @patch('pyditto.ditto.run_ditto')
    def test_all_options_extract(self, mock_run):
        opts = DittoOptions(
            zip_format=True,
            verbose=True,
            keep_parent=True,
            sequester_rsrc=True
        )
        extract('archive.zip', 'dst', opts)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        expected_args = ['-x', '-V', '-k', 'archive.zip', 'dst']
        self.assertEqual(args, expected_args)
        self.assertNotIn('--keepParent', args)
        self.assertNotIn('--sequesterRsrc', args)

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
