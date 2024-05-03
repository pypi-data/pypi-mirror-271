import typing

from tsinterface.io.distribution_io import DistributionIO
from tsinterface.io.io import IO
from tsinterface.io.label_io import LabelIO


class InfoIO(IO):

    def __init__(self, latitude, longitude, labels=None, velocity_dist=None, length_dist=None, beam_dist=None,
                 heading_dist=None):
        # NB! latitude and longitude are computed from the available geocoding
        self.latitude: float = latitude  # Latitude corresponding to x coordinate of BBox
        self.longitude: float = longitude  # Longitude corresponding to y coordinate of BBox

        self.labels: typing.List[LabelIO] = labels  # vessel types

        self.velocity_dist: typing.Optional[DistributionIO] = velocity_dist  # in m/s
        self.length_dist: typing.Optional[DistributionIO] = length_dist  # in m
        self.beam_dist: typing.Optional[DistributionIO] = beam_dist  # in m
        self.heading_dist: typing.Optional[DistributionIO] = heading_dist  # in degrees 0-360 clockwise from north

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'labels:': [label.to_dict() for label in self.labels],
            'velocity_dist': self.velocity_dist.to_dict(),
            'length_dist': self.length_dist.to_dict(),
            'beam_dist': self.beam_dist.to_dict(),
            'heading_dist': self.heading_dist.to_dict(),
        }
