from dataclasses import dataclass
from functools import cached_property
import netCDF4
import numpy as np
from datetime import datetime  # , timedelta


@dataclass
class NcDataFile:
    """NcDataFile class"""
    dataset: netCDF4.Dataset

    @classmethod
    def from_file(cls, filename: str):
        dataset = netCDF4.Dataset(filename)
        return cls(dataset)

    @cached_property
    def variables(self) -> list[str]:
        variables = list(self.dataset.variables.keys())
        drop_variables = ['time', 'latitude', 'longitude']
        variables = [item for item in variables if item not in drop_variables]
        return variables

    @cached_property
    def time(self) -> np.ma.masked_array:
        return self.dataset.variables['time'][:]

    @cached_property
    def datetime(self) -> list[datetime]:
        date_cftimes = netCDF4.num2date(
            self.time,
            self.dataset.variables['time'].units,
            self.dataset.variables['time'].calendar)
        date_times = np.ma.masked_array(
            data=[datetime(*d.timetuple()[:6]) for d in date_cftimes],
            mask=date_cftimes.mask
        )
        return date_times

    @cached_property
    def time_min(self) -> str:
        # Να το αλλάξω σε np min. Δουλεύει πολύ αργά έτσι
        return self.time[0]

    @cached_property
    def time_max(self) -> str:
        return self.time[-1]

    @cached_property
    def datetime_min(self) -> datetime:
        return self.datetime[0]

    @cached_property
    def datetime_max(self) -> datetime:
        return self.datetime[-1]

    @cached_property
    def lon(self) -> np.ma.masked_array:
        return self.dataset.variables['longitude'][:]

    @cached_property
    def lat(self) -> np.ma.masked_array:
        return self.dataset.variables['latitude'][:]
    
    def check_lat_lon_boundaries(self, lat: float, lon: float) -> bool:
        """
        Check if the given latitude and longitude are within the bounds of the dataset.

        Parameters:
            lat (float): Latitude.
            lon (float): Longitude.

        Returns:
            bool: True if the coordinates are within the bounds, False otherwise.
        """
        if lat < self.lat.min() or lat > self.lat.max():
            return False
        if lon < self.lon.min() or lon > self.lon.max():
            return False
        return True
    
    def check_lan_lon_existence(self, lat: float, lon: float) -> bool:
        """
        Check if the given latitude and longitude exist in the dataset.

        Parameters:
            lat (float): Latitude.
            lon (float): Longitude.

        Returns:
            bool: True if the coordinates exist, False otherwise.
        """
        if lat not in self.lat or lon not in self.lon:
            return False
        return True
