
# Third-Party
from rest_framework.renderers import BaseRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_json_api.renderers import JSONRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx['display_edit_forms'] = False
        return ctx

    def show_form_for_method(self, view, method, request, obj):
        """We never want to do this! So just return False."""
        return False

    def get_rendered_html_form(self, data, view, method, request):
        """Why render _any_ forms at all. This method should return
        rendered HTML, so let's simply return an empty string.
        """
        return ""


class XLSXRenderer(BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data
