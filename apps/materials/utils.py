from apps.core.utils import upload_to_folder


def upload_materials_to(instance, filename):
    return upload_to_folder(instance, filename, folder='materials/file', keyword='materials')
