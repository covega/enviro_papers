
def safe_cast(type, value):
    try:
        return type(value)
    except (ValueError, TypeError):
        return None
