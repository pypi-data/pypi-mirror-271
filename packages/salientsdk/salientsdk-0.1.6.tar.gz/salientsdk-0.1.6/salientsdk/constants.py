#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Constants for the Salient SDK.

This module contains constants used throughout the Salient SDK.

"""

import datetime
import hashlib
import itertools
import os
import urllib

import pandas as pd
import requests

# This is the base URL for the Salient API:
URL = "https://api.salientpredictions.com/"

API_VERSION = "v2"

MODEL_VERSION = "v8"
MODEL_VERSIONS = ["v7_1", "v8"]


DESTINATION = "salient_data"


def get_file_destination(destination: str = "-default", make: bool = True) -> str:
    """Get the default destination for downloaded files.

    Args:
        destination (str): If `-default`, return the destination
            set by `set_file_destination`.  Otherwise, return the
            value of `destination`.
        make (bool): If True, create the directory if it doesn't exist.

    Returns:
        str: The destination for downloaded files.

    """
    if destination is None:
        return destination

    destination = str(destination)
    if destination == "-default":
        destination = DESTINATION

    if destination is not None and make:
        os.makedirs(destination, exist_ok=True)

    return destination


def set_file_destination(destination: str = "salient_data") -> str:
    """Set the default destination for downloaded files.

    Args:
        destination (str): The default destination for downloaded files.

    Returns:
        str: The destination that was set by the function.

    """
    global DESTINATION
    if destination is not None:
        destination = str(destination)

    DESTINATION = destination
    return DESTINATION


def _build_url(
    endpoint: str, args: None | dict = None, destination: str = "-default"
) -> tuple[str, str]:
    """Build an API query and associated file name for a given endpoint and arguments.

    Args:
        endpoint (str): The API endpoint to query.
        args (dict): The arguments to pass to the endpoint.
        destination (str): The destination directory for downloaded files.
            If `-default`, will call `get_file_destination()`

    Returns:
        tuple[str, str]: A tuple containing the query URL and the file name to
            download to.
            File name will be `/<destination>/<endpoint>_<argshash>.<format>`.
    """
    url = URL + API_VERSION + "/" + endpoint
    file_name = endpoint

    destination = get_file_destination(destination)
    if destination is not None:
        file_name = os.path.join(destination, file_name)

    if args:
        # apikey will often be None when we're using a persistent session.
        # Eliminate it (and anything else that's None too.)
        args = {k: v for k, v in args.items() if v is not None}

        url += "?"
        url += urllib.parse.urlencode(args, safe=",")

        # apikey doesn't influence the file contents, so shouldn't be in the hash:
        if "apikey" in args:
            del args["apikey"]

        file_name += "_"
        file_name += hashlib.md5(str(args).encode()).hexdigest()

        if "format" in args:
            file_name += "." + args["format"]

    return (url, file_name)


def _build_urls(
    endpoint: str, args: None | dict = None, destination: str = "-default"
) -> pd.DataFrame:
    """Build URLs for a given endpoint and arguments.

    This is the vectorized version of `_build_url`.

    Args:
        endpoint (str): The API endpoint to query.
        args (dict): The arguments to pass to the endpoint.  If any values
            in `args` are lists or tuples, the function will perform a
            combinatoric expansion on all vectorized arguments.
        destination (str): The destination directory for downloaded files.

    Returns:
        pd.DataFrame: A DataFrame containing the queries and file names.
            Will have a single row if all `args` are scalar, or multiple
            rows if any `args` are vectorized.
    """
    if args:
        vector_args = {k: v for k, v in args.items() if isinstance(v, (list, tuple))}

        if vector_args:
            scalar_args = {k: v for k, v in args.items() if not isinstance(v, (list, tuple))}

            expanded_args = list(itertools.product(*vector_args.values()))
            expanded_args = [dict(zip(vector_args.keys(), values)) for values in expanded_args]
            queries = [
                _build_urls(
                    endpoint=endpoint, args={**arg, **scalar_args}, destination=destination
                ).assign(**arg)
                for arg in expanded_args
            ]
            return pd.concat(queries, ignore_index=True)

    (url, file_name) = _build_url(endpoint, args, destination)
    return pd.DataFrame([{"query": url, "file_name": file_name}])


def _validate_date(date: str | datetime.datetime) -> str:
    if isinstance(date, str) and date == "-today":
        date = datetime.datetime.today()

    if isinstance(date, datetime.datetime):
        date = date.strftime("%Y-%m-%d")

    # ENHANCEMENT: accept other date formats like numpy datetime64, pandas Timestamp, etc
    # ENHANCEMENT: make sure date is properly formatted

    return date


def get_model_version(version: str = "-default") -> str:
    """Get the current default model version.

    Args:
        version (str): If `-default`, return the current model version.
            Otherwise, return the value of `version`.

    Returns:
        str: The current model version

    """
    if version is None or version == "-default":
        version = MODEL_VERSION

    return version


def set_model_version(version: str) -> None:
    """Set the default model version.

    Args:
        version (str): The model version to set

    """
    version = str(version)
    assert version in MODEL_VERSIONS
    global MODEL_VERSION
    MODEL_VERSION = version


def _expand_comma(
    val: str | list[str] | None,
    valid: list[str] | None = None,
    name="value",
    default: str | None = None,
) -> list[str] | str:
    """Expand a comma-separated string into a list of strings.

    Args:
        val (str | list[str] | None): A single string that may contain commas.
            If a list of strings, convert to a single string if length == 1.
            If None, return None.
        valid (list[str] | None): A list of valid values for the string.
            If None (default) no validation is performed.
            If provided, asserts if any `val` is not in `valid`.
        name (str): The name of the value to use in error messages.
            Not used if `valid` is None.
        default (str): If not `None`, will replace a string value of `-default` with this

    Returns:
        list[str] | str | None: A list of strings if commas are present,
            otherwise the original string or list of strings.
    """
    if val is None:
        return val

    if isinstance(val, str) and "," in val:
        val = val.split(",")

    # Check to see if val is a list of strings
    if isinstance(val, list):
        if len(val) == 1:
            val = val[0]

    DEFAULT = "-default"
    if default is not None:
        if isinstance(val, list):
            if DEFAULT in val:
                val[val.index(DEFAULT)] = default
        elif isinstance(val, str):
            val = default if val == DEFAULT else val

    if valid:
        if isinstance(val, list):
            for v in val:
                assert v in valid, f"{name} {v} not in {valid}"
        else:
            assert val in valid, f"{name} {val} not in {valid}"

    return val
