from django.core.exceptions import ValidationError


def validate_page_count(value):
    if not str(value).isdigit():
        raise ValidationError('Only numbers allowed')
    return value

def validate_language(value):
    if not str(value).isalpha() or len(value) > 2:
        raise ValidationError('Only alphabet characters allowed')
    return value
