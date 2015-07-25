"""
Backend web-part of watermarking service. Contains only view for front-end app
interaction.
"""
import json
import colander

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


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

    return JsonResponse(deserialized)
