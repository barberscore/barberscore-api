
# Third-Party
from rest_framework.response import Response


class XLSXResponse(Response):
    def __init__(self, xlsx, file_name, *args, **kwargs):
        headers = {
            'Content-Disposition': 'filename="{}.xlsx"'.format(file_name),
            'Content-Length': len(xlsx),
        }

        super().__init__(
            xlsx,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers=headers,
            *args,
            **kwargs
        )
