import os
import uuid
from django.core.exceptions import FieldDoesNotExist
from django.db.models import FileField



def generate_filename(filename, keyword):
    """
    Generates filename with uuid and a keyword
    :param filename: original filename
    :param keyword: keyword to be added after uuid
    :return: new filename in string
    """
    ext = filename.split('.')[-1]
    new_filename = "%s_%s.%s" % (keyword, uuid.uuid4(), ext)
    return new_filename


def upload_to_folder(instance, filename, folder, keyword):
    """
    Generates the path where it should to uploaded

    :param instance: model instance
    :param filename: original filename
    :param folder: folder name where it should be stored
    :param keyword: keyword to be attached with uuid
    :return: string of new path
    """
    return os.path.join(folder, generate_filename(
        filename=filename,
        keyword=keyword
    ))


def file_cleanup(sender, **kwargs):
    """
        File cleanup callback used to emulate the old delete
        behavior using signals. Initially django deleted linked
        files when an object containing a File/ImageField was deleted.

        Usage:
        from django.db.models.signals import post_delete
        post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    for single_field in sender._meta.get_fields():
        try:
            field = sender._meta.get_field(single_field.name)
        except FieldDoesNotExist:
            field = None
        if field and isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, single_field.name)
            if f:
                f.delete(save=False)