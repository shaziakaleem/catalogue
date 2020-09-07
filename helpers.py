class JsonValidationHelper:
    class MalformedDataException(Exception):
        def __init__(self, message="Malformed Data"):
            super().__init__(message)
            self._message = message

        def __str__(self):
            return self._message

    @staticmethod
    def validate(post_dict, expected_dict):
        """Validate JSON based on expected dictionary """
        for key, _ in expected_dict.items():
            if key not in post_dict:
                raise JsonValidationHelper.MalformedDataException(
                    "Malformed Data"
                )
        return post_dict
