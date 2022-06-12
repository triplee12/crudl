import json
from django.http import HttpResponse
from django.template import Context, Template
from django.views.decorators.cache import cache_page
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
