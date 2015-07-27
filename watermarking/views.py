"""
Backend web-part of watermarking service. Contains only view for front-end app
interaction.
"""
import json
import colander

from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods

from watermarking.components.workers import download_and_watermark


class EPUBFileDataSchema(colander.MappingSchema):
    """
    Schema for validation and errors handling and notification
    """
    hash = colander.SchemaNode(
        colander.String(), validator=colander.Length(min=1, max=32))
    url = colander.SchemaNode(
        colander.String(), validator=colander.url)


@require_http_methods(["POST"])
def add_to_watermark_queue(request):
    """
    This view adds request for watermarking file to queue
    """
    data = json.loads(request.body.decode('utf-8'))

    schema = EPUBFileDataSchema()
    try:
        deserialized = schema.deserialize(data)
    except colander.Invalid as exp:
        JsonResponse(exp.asdict(), status=500)

    # XXX: this is really dumb way of processing data and use of celery task,
    #      but I'm out of time on his. I really would like to have here just
    #      adding task to queue wit returning to frontend-app task id, and
    #      additional view that will notify client that his epub is ready
    #      and provide a link to it and start downloading
    task = download_and_watermark.delay(**deserialized)
    file_path = task.get()

    return FileResponse(open(file_path, 'rb'))
