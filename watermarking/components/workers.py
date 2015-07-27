"""
The workers for watermarking files.
I would like to have jobs with 3-states:
    * new
    * watermarked
    * delivered
Also jobs older than 1 day should be deleted

"""
from celery import Celery
from watermarking.components.watermarking import EpubWatermarker
import urllib.request
import shutil
from tempfile import mkstemp
import arrow

# TODO: make console script from it, make this D project as python package
app = Celery('tasks', backend='redis://localhost:9987/1', broker='redis://localhost:9987/0',)
epub_watermarker = EpubWatermarker()


def add_time_stamp_to_watermark(watermark):
    """
    Adds timestamp to has
    """
    return '{0} {1}'.format(watermark, str(arrow.utcnow()))


@app.task
def download_and_watermark(url, watermark):
    """

    """
    # TODO: looks horrible, add mechanism for files clean up
    _, tmpfile = mkstemp()

    with urllib.request.urlopen(url) as response, open(tmpfile, 'wb') as dest:
        shutil.copyfileobj(response, dest)

    sign = add_time_stamp_to_watermark
    epub_watermarker.watermark(tmpfile, sign)

    return tmpfile
