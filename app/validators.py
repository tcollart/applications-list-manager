from django.core.exceptions import ValidationError


def is_zipfile(file_url):
    if not file_url.name.endswith('.zip'):
        raise ValidationError('Wrong file extension')
