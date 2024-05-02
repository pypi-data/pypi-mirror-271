import typing

from tsinterface.io.bbox_io import BBoxIO
from tsinterface.io.info_dto import InfoIO
from tsinterface.io.io import IO
from tsinterface.io.label_io import LabelIO


class DetectionIO(IO):

    def __init__(self, labels, bbox, info):
        self.labels: typing.List[LabelIO] = labels
        self.bbox: BBoxIO = bbox
        self.info: InfoIO = info

    def to_dict(self):
        return {
            'labels:': [label.to_dict() for label in self.labels],
            'bbox:': self.bbox.to_dict(),
            'info': self.info.to_dict(),
        }
