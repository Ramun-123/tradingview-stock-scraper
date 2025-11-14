def clean_text(value):
    if not value:
        return None
    return " ".join(value.split())