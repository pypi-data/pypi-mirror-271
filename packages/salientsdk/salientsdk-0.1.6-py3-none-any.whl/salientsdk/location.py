#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Define the Location class."""

# Usage example:
# python location.py --lat 42 --lon -73

import argparse
import datetime
import os
import urllib

from . import constants, login_api


class Location:
    """Define geographical parameters for an API query.

    The Salient API
    can define location by a single latitude/longitude, multiple
    latitude/longitude pairs in a single location_file, or a polygon
    defined in a shapefile.
    """

    def __init__(
        self,
        lat: float | None = None,
        lon: float | None = None,
        location_file: str | list[str] | None = None,
        shapefile: str | list[str] | None = None,
        region: str | list[str] | None = None,
    ):
        """Initialize a Location object.

        Only one of the following 4 options should be used at a time: lat/lon,
        location_file, shapefile, or region.

        Args:
            lat (float): Latitude in degrees, -90 to 90.
            lon (float): Longitude in degrees, -180 to 180.
            location_file (str | list[str]): Path(s) to CSV file(s) with latitude and longitude columns.
            shapefile (str | list[str]): Path(s) to a shapefile(s) with a polygon defining the location.
            region (str | list[str]): Accepts continents, countries, or U.S. states (e.g. "usa")
                Only available for `hindcast_summary()`
        """
        self.lat = lat
        self.lon = lon
        self.location_file = self._expand_user_files(location_file)
        self.shapefile = self._expand_user_files(shapefile)
        self.region = region

        self.__validate()

    @staticmethod
    def _expand_user_files(files: str | list[str] | None) -> str | list[str] | None:
        files = constants._expand_comma(files)

        # When referencing user files, the user may specify them with
        # a directory name because that's how functions like upload_*
        # create them.  But the API doesn't have a directory structure and
        # only uses the file name.  So we need to strip off the directory.
        if files is None:
            pass
        elif isinstance(files, str):
            files = os.path.basename(files)
        elif isinstance(files, list):
            files = [os.path.basename(f) for f in files]

        return files

    def asdict(self, **kwargs) -> dict:
        """Render as a dictionary.

        Generates a dictionary representation that can be encoded into a URL.
        Will contain one and only one location_file, shapefile, or lat/lon pair.

        Args:
            **kwargs: Additional key-value pairs to include in the dictionary.
                Will validate some common arguments that are shared across API calls.
        """
        if self.location_file:
            dct = {"location_file": self.location_file, **kwargs}
        elif self.shapefile:
            dct = {"shapefile": self.shapefile, **kwargs}
        elif self.region:
            dct = {"region": self.region, **kwargs}
        else:
            dct = {"lat": self.lat, "lon": self.lon, **kwargs}

        if "apikey" in dct and dct["apikey"] is not None:
            dct["apikey"] = login_api._get_api_key(dct["apikey"])

        if "start" in dct:
            dct["start"] = constants._validate_date(dct["start"])
        if "end" in dct:
            dct["end"] = constants._validate_date(dct["end"])
        if "forecast_date" in dct:
            dct["forecast_date"] = constants._validate_date(dct["forecast_date"])

        if "version" in dct:
            dct["version"] = constants._expand_comma(
                val=dct["version"],
                valid=constants.MODEL_VERSIONS,
                name="version",
                default=constants.get_model_version(),
            )

        if "shapefile" in dct and "debias" in dct and dct["debias"]:
            raise ValueError("Cannot debias with shapefile locations")

        return dct

    def asargs(self, **kwargs) -> str:
        """Render as api arguments.

        Encodes a dictionary of the type returned by `asdict` into a
        single string appropriate for an API request.
        """
        return urllib.parse.urlencode(self.asdict(**kwargs), safe=",")

    def __validate(self):
        if self.location_file:
            assert not self.lat, "Cannot specify both lat and location_file"
            assert not self.lon, "Cannot specify both lon and location_file"
            assert not self.region, "Cannot specify both region and location_file"
            assert not self.shapefile, "Cannot specify both shape_file and location_file"
        elif self.shapefile:
            assert not self.region, "Cannot specify both region and shapefile"
            assert not self.lat, "Cannot specify both lat and shape_file"
            assert not self.lon, "Cannot specify both lon and shape_file"
        elif self.region:
            assert not self.lat, "Cannot specify both lat and region"
            assert not self.lon, "Cannot specify both lon and region"
            assert not self.location_file, "Cannot specify both location_file and region"
            assert not self.shapefile, "Cannot specify both shape_file and region"
        else:
            assert self.lat, "Must specify lat & lon, location_file, shapefile, or region"
            assert self.lon, "Must specify lat & lon, location_file, shapefile, or region"
            assert -90 <= self.lat <= 90, "Latitude must be between -90 and 90 degrees"
            assert -180 <= self.lon <= 180, "Longitude must be between -180 and 180 degrees"

    def __str__(self):
        """Return a string representation of the Location object."""
        if self.location_file:
            return f"location file: {self.location_file}"
        elif self.shapefile:
            return f"shape file: {self.shapefile}"
        elif self.region:
            return f"region: {self.region}"
        else:
            return f"({self.lat}, {self.lon})"

    def __eq__(self, other):
        """Check if two Location objects are equal."""
        if self.location_file:
            return self.location_file == other.location_file
        elif self.shapefile:
            return self.shapefile == other.shape_file
        elif self.region:
            return self.region == other.region
        else:
            return self.lat == other.lat and self.lon == other.lon

    def __ne__(self, other):
        """Check if two Location objects are not equal."""
        return not self.__eq__(other)
