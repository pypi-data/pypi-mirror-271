
def string_to_list(value,separator):
    return [key.strip() for key in value.split(separator) if key.strip()]