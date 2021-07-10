from apps.core.utils import upload_to_folder


def upload_assignment_to(instance, filename):
    return upload_to_folder(instance, filename, folder='assignments/file', keyword='assignment')
