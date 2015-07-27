"""
Supported books formats for watermarking
"""
import shutil
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from watermarking.exceptions import MalformedEPUBError


def add_watermark_to_xml(content, watermark):
    """
    Adds watermark to XML's content, as params takes strings and basically puts
    one into other
    """
    # IDEA: it's really ugly way for adding wattermark to xml file, but why
    #           not? i'm limited in time for proper realization
    return "{0}\n<!-- {1} -->".format(content.decode(), watermark)


class EpubWatermarker(object):
    """
    Class for watermarking epub <files></files>
    """

    watermark_template = "watermark: {0}"

    def watermark(self, file_path, watermark):
        """
        Watermark provided epub file with given watermark - adds it into file
        META-INF/container.xml as a comment.
        WARNING :: This function will modify file content.
        """
        file_to_update = 'META-INF/container.xml'

        with NamedTemporaryFile() as dest_file:

            # unfortunately there is no efficient way for updating files
            # on zip`s, so only way is to unzip, edit and zip again.
            try:
                with ZipFile(file_path, 'r') as origin_epub, \
                     ZipFile(dest_file.name, 'w') as watermarkedd_epub:
                    # simply copping other content
                    for content in origin_epub.infolist():
                        data = origin_epub.read(content.filename)
                        if content.filename == file_to_update:
                            # adding watermark to META-INF/container.xml file
                            # without changing file meta-info (last modify)
                            data = add_watermark_to_xml(
                                origin_epub.read(file_to_update),
                                self.watermark_template.format(watermark))
                        watermarkedd_epub.writestr(content, data)
            except Exception as exp:
                raise MalformedEPUBError(exp)
            # replacing origin epub file with watermarked epub
            shutil.copyfile(dest_file.name, file_path)
