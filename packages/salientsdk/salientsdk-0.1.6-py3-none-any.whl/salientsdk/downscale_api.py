#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Interface to the Salient data_timeseries API.

Command line usage example:
```
cd ~/salientsdk
python -m salientsdk downscale -lat 42 -lon -73 --date 2020-01-01 -u username -p password --force
```

"""

import os
from datetime import datetime

import requests
import xarray as xr

from .constants import _build_urls
from .location import Location
from .login_api import download_queries

REFERENCE_CLIMS = ["30_yr", "10_yr", "5_yr"]


def downscale(
    # API arguments -----
    loc: Location,
    variables: str = "temp,precip",
    debias: bool = False,
    date: str = "-today",
    reference_clim: str = "30_yr",
    members: int = 50,
    version: str | list[str] = "-default",
    # Non-API arguments --------
    destination: str = "-default",
    force: bool = False,
    session: requests.Session | None = None,
    apikey: str | None = None,
    verify: bool | None = None,
    verbose: bool = False,
    **kwargs,
) -> str | list[str]:
    """Temporal downscale of forecasts.

    Convert temporally coarse probabilistic forecasts into granular daily ensembles.
    For more detail, see the
    [api doc](https://api.salientpredictions.com/v2/documentation/api/#/Forecasts/downscale).

    Args:
        loc (Location): The location to query.
            If using a `shapefile` or `location_file`, may input a vector of file names which
            will trigger multiple calls to `downscale`.  This is useful because `downscale` requires
            that all points in a file be from the same continent.
        variables (str): The variables to query, separated by commas
            See the
            [Data Fields](https://salientpredictions.notion.site/Variables-d88463032846402e80c9c0972412fe60)
            documentation for a full list of available variables.
            Note that `downscale` natively supports a list of variables, so passing a list of
            variables here will not necessarily trigger downloading multiple files.
        date (str): The start date of the time series.
            If `date` is `-today`, use the current date.
        reference_clim (str): Reference period to calculate anomalies.
        members (int): The number of ensemble members to download
        debias (bool): If True, debias the data
        version (str): The model version of the Salient `blend` forecast.
        destination (str): The destination directory for downloaded files.
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided.
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages
        **kwargs: Additional arguments to pass to the API

    Keyword Arguments:
        gdd_base (int): The base temperature for growing degree days
        units (str): US or SI

    Returns:
        str | pd.DataFrame : If only one file was downloaded, return the name of the file.
            If multiple files were downloaded, return a table with column `file_name` and
            additional columns documenting the vectorized input arguments such as
            `location_file`.
    """
    format = "nc"
    frequency = "daily"
    model = "blend"

    assert members > 0, "members must be a positive integer"

    if date == "-today":
        date = datetime.today().strftime("%Y-%m-%d")

    assert reference_clim in REFERENCE_CLIMS, f"reference_clim must be one of {REFERENCE_CLIMS}"

    endpoint = "downscale"
    args = loc.asdict(
        variables=variables,
        date=date,
        reference_clim=reference_clim,
        debias=debias,
        members=members,
        format=format,
        model=model,
        version=version,
        frequency=frequency,
        apikey=apikey,
        **kwargs,
    )

    queries = _build_urls(endpoint, args, destination)

    download_queries(
        query=queries["query"].values,
        file_name=queries["file_name"].values,
        force=force,
        session=session,
        verify=verify,
        verbose=verbose,
        format=format,
        max_workers=5,  # downscale @limiter.limit("5 per second")
    )

    if len(queries) == 1:
        return queries["file_name"].values[0]
    else:
        # Now that we've executed the queries, we don't need it anymore:
        queries = queries.drop(columns="query")
        return queries
