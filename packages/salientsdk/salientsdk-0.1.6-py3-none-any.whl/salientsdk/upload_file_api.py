#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Interface to the Salient `upload_file` API.

There is no command line interface for this module.
"""

import json
import os

import pandas as pd
import requests

from .constants import _build_url, get_file_destination
from .login_api import download_query, get_current_session, get_verify_ssl


def upload_file(file: str, verbose: bool = True, session: requests.Session | None = None) -> None:
    """Uploads a geography file to the Salient API.

    An interface to to the Salient
    [upload_file](https://api.salientpredictions.com/v2/documentation/api/#/General/upload_file)
    API endpoint.

    Args:
        file (str): the file to upload (e.g. a shapefile or CSV).
        verbose (bool): whether to print status messages.
        session (requests.Session): the session to use for the upload.

    """
    if verbose:
        print(f"Uploading {file}")

    (url, loc_file) = _build_url("upload_file")

    if session is None:
        session = get_current_session()

    # do we need to open .zipped shapefiles in 'rb' binary mode?
    req = session.post(url, files={"file": open(file, "r")})
    req.raise_for_status()
    if verbose:
        print(req.text)

    return None


def upload_bounding_box(
    # API arguments ----------
    north: float,
    south: float,
    east: float,
    west: float,
    geoname: str,
    # Non-API arguments --------
    destination: str | None = "-default",
    force: bool = False,
    verbose: bool = True,
    session: requests.Session | None = None,
) -> str:
    """Upload a bounding box.

    Create and upload a GeoJSON shapefile with a rectangular bounding box
    for later use with the `shapefile` location argument.

    Args:
        north (float): Northern extent decimal latitude
        south (float): Southern extent decimal latitude
        east (float): Eastern extent decimal longitude
        west (float): Western extent decimal longitude
        geoname (str): Name of the GeoJSON file and object to create
        destination (str): The destination directory for the generated file
        force (bool): If the file already exists, don't upload it
        verbose (bool): Whether to print status messages
        session (requests.Session): The session object to use for the request

    Returns:
        str: File name of the GeoJSON file
    """
    geofile = geoname + ".geojson"
    destination = get_file_destination(destination)
    if destination is not None:
        geofile = os.path.join(destination, geofile)

    if not force and os.path.exists(geofile):
        if verbose:
            print(f"File {geofile} already exists")
        return geofile

    assert west < east, "West must be less than East"
    assert south < north, "South must be less than North"
    assert session is not None, "login to create a session"

    geoshape = {
        "type": "Feature",
        "properties": {"name": geoname},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[west, north], [east, north], [east, south], [west, south], [west, north]]
            ],
        },
    }
    with open(geofile, "w") as f:
        json.dump(geoshape, f)

    upload_file(file=geofile, verbose=verbose, session=session)

    return geofile


def upload_location_file(
    lats: list[float] | pd.Series,
    lons: list[float] | pd.Series,
    names: list[str] | pd.Series,
    geoname: str,
    destination: str = "-default",
    force: bool = False,
    verbose: bool = False,
    session: requests.Session | None = None,
    **kwargs,
) -> str:
    """Upload a vector of locations.

    Create and upload a CSV file with a list of locations for
    later use with the `location_file` location argument.

    Args:
        lats (list[float] | pd.Series): List of decimal latitudes
        lons (list[float] | pd.Series): List of decimal longitudes
        names (list[str] | pd.Series): List of names for the locations
        geoname (str): Name of the CSV file and object to create
        destination (str): The destination directory for the generated file
        force (bool): When False, if the file already exists don't upload it
        verbose (bool): If True, print status messages
        session (requests.Session): The session object to use for the request
        **kwargs: Additional columns to include in the CSV file

    Returns:
        str: File name of the CSV file
    """
    geofile = geoname + ".csv"
    destination = get_file_destination(destination)
    if destination is not None:
        geofile = os.path.join(destination, geofile)

    if not force and os.path.exists(geofile):
        if verbose:
            print(f"File {geofile} already exists")
        return geofile

    loc_table = pd.DataFrame({"lat": lats, "lon": lons, "name": names, **kwargs})
    loc_table.to_csv(geofile, index=False)

    upload_file(file=geofile, verbose=verbose, session=session)

    return geofile


def user_files(
    destination: str = "-default",
    session: requests.Session | None = None,
    verify: bool | None = None,
    verbose: bool = False,
) -> str:
    """List the files uploaded by the user.

    Args:
        destination (str): The destination directory for the resulting JSON file
        session (requests.Session): The session object to use for the request
        verify (bool): Whether to verify the SSL certificate.
            Defaults to use the value returned by `get_verify_ssl()`
        verbose (bool): If True, print status messages

    Returns:
        str: the location of the JSON file containing the list of files
    """
    format = "json"
    endpoint = "user_files"
    (url, loc_file) = _build_url(endpoint, args=None, destination=destination)
    loc_file = f"{loc_file}.{format}"

    download_query(
        query=url,
        file_name=loc_file,
        format=format,
        session=session,
        verify=verify,
        verbose=verbose,
        force=True,
    )

    if verbose:
        # parse the json file and print the results:
        with open(loc_file, "r") as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))

    return loc_file
