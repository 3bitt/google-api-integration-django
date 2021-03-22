def get_date_format(date: str):
    parts = date.split('-')
    if len(parts) == 1:
        return '%Y'
    elif len(parts) == 2:
        return '%Y-%m'
    else:
        return '%Y-%m-%d'
