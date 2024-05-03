class Dto:
    def __init__(self) -> None:
        self.pages: list[DtoPage] = []
        self.fonts: list[DtoFont] = []
        # self.images: list[ImageData] = []


class DtoFont:
    def __init__(self, name: str, font_raw_data: bytes) -> None:
        self.name = name
        self.raw_data = font_raw_data


class DtoPage:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.contents: list[object] = []


class DtoTextArea:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.height_empty_space: float = 0.0
        self.v_align: str = ""
        self.paragraphs: list[DtoParagraph] = []
        self.fragments: list[DtoFragment] = []


class DtoParagraph:
    def __init__(self, x: float, y: float, text_area: DtoTextArea) -> None:
        self.x = x
        self.y = y
        self.text_area = text_area
        self.width: float = 0.0
        self.height: float = 0.0
        self.h_align: str = ""
        self.chars: str = ""
        self.line_height_ratio: float = 0.0
        self.tab_size: float = 0.0
        self.first_line_indent: float = 0.0
        self.hanging_indent: float = 0.0
        self.left_indent: float = 0.0
        self.right_indent: float = 0.0
        self.space_before: float = 0.0
        self.space_after: float = 0.0
        self.num_of_lines: int = 0
        self.textlines: list[DtoTextLine] = []
        self.fragments: list[DtoFragment] = []


class DtoTextLine:
    def __init__(
        self,
        x: float,
        y: float,
        paragraph: DtoParagraph,
        justify_padding_after: float,
    ) -> None:
        self.x = x
        self.y = y
        self.paragraph = paragraph
        self.justify_padding_after = justify_padding_after
        self.width: float = 0.0
        self.height: float = 0.0
        self.baseline: float = 0.0
        self.space_after: float = 0.0
        self.paragraph_h_align: str = ""
        self.words: list[DtoWord] = []
        self.fragments: list[DtoFragment] = []


class DtoWord:
    def __init__(self, x: float, y: float, textline: DtoTextLine) -> None:
        self.x = x
        self.y = y
        self.textline = textline
        self.width: float = 0.0
        self.height: float = 0.0
        self.baseline: float = 0.0
        self.justify_space: float = 0.0
        self.fragments: list[DtoFragment] = []


class DtoFragment:
    def __init__(
        self,
        x: float,
        y: float,
        word: DtoWord,
    ) -> None:
        self.x = x
        self.y = y
        self.word = word
        self.width: float = 0.0
        self.height: float = 0.0
        self.baseline: float = 0.0
        self.chars: str = ""
        self.font_name: str = ""
        self.font_size: float = 0.0
        self.font_color: tuple[int, int, int] = (0, 0, 0)
