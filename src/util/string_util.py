class StringUtil:

    @staticmethod
    def camel_case_to_normal(text: str) -> str:
        import re

        text = text.replace("_", "")
        pattern = re.compile(
            r"""
                (?<=[a-z])      # preceded by lowercase
                (?=[A-Z])       # followed by uppercase
                |               #   OR
                (?<=[A-Z])       # preceded by lowercase
                (?=[A-Z][a-z])  # followed by uppercase, then lowercase
            """,
            re.X,
        )
        return pattern.sub(" ", text).lower()
