import os

from django.conf import settings

from templated_email import InlineImage


def make_email_image(path: str) -> InlineImage:
    """
    Create InlineImage for static images to be used in templated email.
    """
    full_path = os.path.join(settings.APPS_DIR, 'static/img', path)
    with open(full_path, 'rb') as f:
        img_content = f.read()
    basename = os.path.basename(full_path)
    return InlineImage(basename, img_content)


def get_default_email_context() -> dict:  # TODO
    """
    Return default context for email, like icons.
    """
    return {}
