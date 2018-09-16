
# Third-Party
from rest_framework.renderers import BaseRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_json_api.renderers import JSONRenderer


class NoHTMLFormBrowsableAPIRenderer(BrowsableAPIRenderer):

    def get_rendered_html_form(self, *args, **kwargs):
        return ""


class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class XLSXRenderer(BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class CustomJSONRenderer(JSONRenderer):
    # pass
    @classmethod
    def extract_relationships(cls, fields, resource, resource_instance):
        if resource_instance._meta.model_name == 'group' and resource_instance.kind <= 30:
            try:
                fields.pop('members')
            except KeyError:
                pass
        return super().extract_relationships(fields, resource, resource_instance)
