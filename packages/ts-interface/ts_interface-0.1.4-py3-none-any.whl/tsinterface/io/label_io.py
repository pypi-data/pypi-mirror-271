from tsinterface.io.io import IO


class LabelIO(IO):

    def __init__(self, label, probability):
        # The Label provides the proposed label and probability
        # For the detections it is a predefined LabelType
        # For vessels it is an unstructured string
        self.label: str = label
        self.probability: float = probability

    def to_dict(self):
        return vars(self)
