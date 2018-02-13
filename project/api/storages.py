import cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary_storage.storage import MediaCloudinaryStorage


class CustomMediaCloudinaryStorage(MediaCloudinaryStorage):
    def _upload(self, name, content):
        options = {
            'use_filename': False,
            'resource_type': 'image',
            'overwrite': True,
            'invalidate': True,
            'public_id': name,
            'format': 'png',
        }
        return cloudinary.uploader.upload(content, **options)


class CustomExcelCloudinaryStorage(RawMediaCloudinaryStorage):
    def _upload(self, name, content):
        options = {
            'use_filename': False,
            'resource_type': 'raw',
            'overwrite': True,
            'invalidate': True,
            'public_id': name,
            'format': 'xlsx',
        }
        return cloudinary.uploader.upload(content, **options)


class CustomPDFCloudinaryStorage(RawMediaCloudinaryStorage):
    def _upload(self, name, content):
        options = {
            'use_filename': False,
            'resource_type': 'raw',
            'overwrite': True,
            'invalidate': True,
            'public_id': name,
            'format': 'pdf',
        }
        return cloudinary.uploader.upload(content, **options)
