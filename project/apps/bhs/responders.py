
# Third-Party
from rest_framework.response import Response


class PDFResponse(Response):
    def __init__(self, pdf, file_name, *args, **kwargs):
        headers = {
            'Content-Disposition': 'filename="{}.pdf"'.format(file_name),
            'Content-Length': len(pdf),
        }

        super().__init__(
            pdf,
            content_type='application/pdf',
            headers=headers,
            *args,
            **kwargs
        )


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

class DOCXResponse(Response):
    def __init__(self, docx, file_name, *args, **kwargs):
        headers = {
            'Content-Disposition': 'filename="{}.docx"'.format(file_name),
            # 'Content-Length': len(xlsx),
        }

        super().__init__(
            docx,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers=headers,
            *args,
            **kwargs
        )
