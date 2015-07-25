import os
import filecmp
import os.path
import unittest
from tempfile import mkstemp
import shutil

from testfixtures import compare, ShouldRaise
from watermarking.exceptions import MalformedEPUBError


from watermarking.components.watermarking import EpubWatermarker

_HERE = os.path.dirname(os.path.abspath(__file__))
_ORIGIN_EPUB_PATH = os.path.join(_HERE, 'data', 'The_Little_Prince.epub')
_MALFORMED_EPUB_PATH = os.path.join(_HERE, 'data', 'malformed.epub')
_WATERMARKED_EPUB_PATH = os.path.join(
    _HERE, 'data', 'The_Little_Prince_watermarked.epub')


class TestEpubFilesWatermarking(unittest.TestCase):
    def setUp(self):
        _, self.working_file_path = mkstemp()
        shutil.copyfile(_ORIGIN_EPUB_PATH, self.working_file_path)
        self.epub_watermarker = EpubWatermarker()

    def tearDown(self):
        os.remove(self.working_file_path)

    def test_epub_file_watermarking(self):
        self.epub_watermarker.watermark(
            self.working_file_path, 'my_signature-timestamp')
        compare(
            filecmp.cmp(self.working_file_path, _WATERMARKED_EPUB_PATH, False),
            True)

    def test_malformed_epub_file_hanling(self):
        shutil.copyfile(_MALFORMED_EPUB_PATH, self.working_file_path)
        with ShouldRaise(MalformedEPUBError):
            self.epub_watermarker.watermark(
                self.working_file_path, 'my_signature-timestamp')

