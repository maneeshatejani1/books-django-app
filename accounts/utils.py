def split_full_name(full_name):
    first_name = last_name = None
    parts = full_name.split(' ')
    if len(parts) == 1:
        first_name = parts[0]
    elif len(parts) == 2:
        first_name = parts[0]
        last_name = parts[1]
    else:
        first_name = parts[0]
        last_name = ' '.join(parts[1:])
    return first_name, last_name
