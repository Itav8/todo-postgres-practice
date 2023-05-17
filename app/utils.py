def map_fields_to_array(items, cols):
    response_data = []
    for item in items:
        data = {}
        for i, col in enumerate(cols):
            data[col] = item[i]

        response_data.append(data)

    return response_data


# Map a single item's fields.
def map_fields(items, cols):
    data = {}
    for item in items:
        for i, col in enumerate(cols):
            data[col] = item[i]

    return data
