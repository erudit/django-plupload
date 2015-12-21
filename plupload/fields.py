import os

from django.db import models
from django.db.models.fields.files import FieldFile

from django.conf import settings


class ResumableFieldFile(FieldFile):
    pass


class ResumableFileField(models.FileField):

    attr_class = ResumableFieldFile

    def pre_save(self, model_instance, add):

        if not hasattr(settings, 'UPLOAD_ROOT'):
            raise AttributeError(
                'You must define UPLOAD_ROOT in your settings'
            )

        upload_root = settings.UPLOAD_ROOT

        directory_name = "{}/{}/{}/{}".format(
            upload_root,
            self.model.__name__,
            self.attname,
            model_instance.pk
        )

        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

    def __init__(self, *args, **kwargs):
        super(ResumableFileField, self).__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super(ResumableFileField, self).deconstruct()
        return name, path, args, kwargs
