import os
import json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from django.template import Context, Template
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import crsf_protect
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import render

JS_SETTINGS_TEMPLATE = """
window.settings = JSON.parse('{{ json_data|escapejs }}');
"""

@cache_page(60 * 15)
def js_settings(request):
    data = {
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "DEBUG": settings.DEBUG,
        "LANGUAGES": settings.LANGUAGES,
        "DEFAULT_LANGUAGES_CODE": settings.LANGUAGES_CODE,
        "CURRENT_LANGUAGES_CODE": request.LANGUAGES_CODE,
    }
    json_data = json.dumps(data)
    template = Template(JS_SETTINGS_TEMPLATE)
    context = Context({"json_data": json_data})
    response = HttpResponse(
        content=template.render(context),
        content_type="application/javascript; charset=UTF-8"
    )
    return response

@crsf_protect
def upload_file(request):
    status_code = 400
    data = {"files": [], "error": _("Bad request")}
    if request.method == "POST" and request.is_ajax() and "picture" in request.FILES:
        file_types = [f"image/{x}" for x in ["gif", "jpg", "jpeg", "png"]]
        file = request.FILES.get("picture")
        if file.content_type not in file_types:
            status_code = 405
            data["error"] = _("Invalid file format")
        else:
            upload_to = os.path.join("temporary-uploads", file.name)
            name = default_storage.save(upload_to, ContentFile(file.read()))
            file = default_storage.open(name)
            status_code = 200
            del data["error"]
            absolute_uploads_dir = os.path.join(settings.MEDIA_ROOT, "temporary-uploads")
            file.filename = os.path.basename(file.name)
            data["files"].append(
                {
                    "name": file.filename,
                    "size": file.size,
                    "deleteType": "DELETE",
                    "deleteUrl": (reverse("delete_file") + f"?filename={file.filename}"),
                    "path": file.name[len(absolute_uploads_dir) + 1 :],
                }
            )
    return JsonResponse(data, status=status_code)
