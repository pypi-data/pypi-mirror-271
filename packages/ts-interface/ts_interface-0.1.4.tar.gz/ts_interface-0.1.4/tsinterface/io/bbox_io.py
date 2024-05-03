from tsinterface.io.io import IO


class BBoxIO(IO):

    def __init__(self, x, y, width, height):
        self.x: float = x  # Object center position in pixel
        self.y: float = y  # Object center position in pixel
        self.width: float = width  # Object width in pixel
        self.height: float = height  # Object height in pixel

    def to_dict(self):
        return vars(self)
