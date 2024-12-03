from kataho.core.kataho_olc import CodeArea, encode, decode


def convert_from_plus_code_to_lat_lng(plus_code: str):
    center: CodeArea = decode(plus_code)
    c_lat, c_long = center.latlng()
    return f"{c_lat},{c_long}"


def convert_from_lat_lng_to_plus_code(latlng: str):
    latlng_parts = latlng.split(",")
    try:
        return encode(float(latlng_parts[0]) or 0.0, float(latlng_parts[1]) or 0.0)
    except Exception as e:
        return encode(0.0, 0.0)
