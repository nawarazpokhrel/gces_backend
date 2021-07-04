from apps.core.utils import upload_to_folder


def upload_notice_image_to(instance, filename):
    return upload_to_folder(instance, filename, folder='notice/image', keyword='notice_image')
