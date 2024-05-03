import typing

from tsinterface.io.io import IO


class DistributionIO(IO):

    # The distributions can for all intended purposes can be seen as gaussian.
    # However, the parameters may not describe a gaussian distribution
    def __init__(self, mean, std=None):
        self.mean: float = mean
        self.std: typing.Optional[float] = std

    def to_dict(self):
        return vars(self)
