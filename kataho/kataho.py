import kataho.core.kataho_converters as KatahoConverters


class KatahoSDK:
    @staticmethod
    def plus_to_lat_lng(plus_code: str) -> str:
        return KatahoConverters.convert_from_plus_code_to_lat_lng(plus_code)

    @staticmethod
    def lat_lng_to_plus(lat_lng: str) -> str:
        return KatahoConverters.convert_from_lat_lng_to_plus_code(lat_lng)
