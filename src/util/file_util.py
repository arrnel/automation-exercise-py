class TxtUtil:

    def __init__(self, absolute_path_to_file: str):
        self.__path_to_file = absolute_path_to_file

    def get_row_text(self, row_number: int) -> str:
        if row_number <= 0:
            raise ValueError("Row number should be greater or equal 1")

        with open(self.__path_to_file, "r", encoding="utf-8") as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == row_number:
                    return line.rstrip("\n")

        raise IndexError(
            f"File with path [{self.__path_to_file}] has fewer string lines than expected."
            f"Expected lines: {row_number}"
        )
