from dataclasses import dataclass
from functools import cached_property
from .nc_datafile import NcDataFile
import numpy as np
from datetime import datetime  # , timedelta
from scipy.interpolate import RegularGridInterpolator  # griddata


@dataclass
class NcVariable:
    """NcVariable class"""
    ncdf: NcDataFile
    varname: str

    @property
    def long_name(self) -> str:
        return self.ncdf.dataset.variables[self.varname].long_name

    @cached_property
    def values(self) -> np.ma.masked_array:
        return self.ncdf.dataset.variables[self.varname][:]

    @cached_property
    def min_value(self) -> float:
        return self.values.min()

    @cached_property
    def max_value(self) -> float:
        return self.values.max()

    def get_point_interpolation_at_time_index(
            self, lat: float, lon: float,
            time_index: int) -> float:
        # Create meshgrid of longitude and latitude
        lon_grid, lat_grid = np.meshgrid(self.ncdf.lon, self.ncdf.lat)

        data_values_at_time = self.values[time_index]
        # # Flatten the arrays
        # lon_flat = lon_grid.flatten()
        # lat_flat = lat_grid.flatten()
        # data_flat = data_values_at_time.flatten()

        # Interpolate the data to the new location
        # interpolated_value = griddata(
        #     (lon_flat, lat_flat), data_flat, (lon, lat), method='linear')
        f = RegularGridInterpolator(
            (self.ncdf.lat, self.ncdf.lon), data_values_at_time)
        interpolated_value = f([lat, lon])

        return interpolated_value

    # def get_interpolations(self, lat: float, lon: float) -> np.ma.masked_array:
    #     """
    #     Get values from a masked array at specified coordinates across all arrays.

    #     Parameters:
    #         lat (float): Latitude.
    #         lon (float): Longitude.

    #     Returns:
    #         np.ma.masked_array: Array of values at the specified coords
    #                             for each time step.
    #     """
    #     lat_index = np.where(self.ncdf.lat == lat)[0][0]
    #     lon_index = np.where(self.ncdf.lon == lon)[0][0]
    #     return self.values[:, lat_index, lon_index]

    def get_time_history_at_indices(
            self, lat_index: int, lon_index: int) -> np.ma.masked_array:
        # start_date_index: int = 0,
        # end_date_index: int = -1) -> np.ma.masked_array:
        """
        Get values from a masked array at specified indices across all arrays.

        Parameters:
            lat_index (int): Index along the lat dimension.
            lon_index (int): Index along the lon dimension.

        Returns:
            np.ma.masked_array: Array of values at the specified coord indices
                                for each time step.
        """
        values = self.values[:, lat_index, lon_index]
        # values = self.values[start_date_index:end_date_index, lat_index, lon_index]
        return values

    def get_time_history_at_coords(
            self, lat: float, lon: float) -> np.ma.masked_array:
        """
        Get values from a masked array at specified coordinates across all arrays.

        Parameters:
            lat (float): Latitude.
            lon (float): Longitude.

        Returns:
            np.ma.masked_array: Array of values at the specified coords
                                for each time step.
        """

        if self.ncdf.check_lan_lon_existence(lat, lon):
            lat_index = np.where(self.ncdf.lat == lat)[0][0]
            lon_index = np.where(self.ncdf.lon == lon)[0][0]
            return self.get_time_history_at_indices(lat_index, lon_index)
        elif not self.ncdf.check_lat_lon_boundaries(lat, lon):
            raise ValueError('Latitude or longitude out of bounds.')
        else:
            # interpolated_values = np.ma.zeros(self.values.shape[0])

            interpolated_values = np.ma.array([
                self.get_point_interpolation_at_time_index(lat, lon, i)
                for i in range(self.values.shape[0])
            ])

            return interpolated_values[:, 0]
