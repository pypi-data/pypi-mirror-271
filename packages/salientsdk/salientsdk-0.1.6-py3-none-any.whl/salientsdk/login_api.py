#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Login to the Salient API.

Command line usage:
```
cd ~/salientsdk
python -m salientsdk login -u testusr -p testpwd
# or, to use api keys:
python -m salientsdk login --apikey testkey

```

"""

import argparse
import os
from concurrent.futures import ThreadPoolExecutor

import requests

from .constants import _build_url

try:
    from google.cloud import secretmanager
except ImportError as ie:
    # secretmanager is a convenience for internal Salient users.
    # Not needed for customer use.
    pass


VERIFY_SSL = True

CURRENT_SESSION = None


def _get_api_key(apikey: str | None = None) -> str | None:
    """Regularize API key values."""
    if apikey is None:
        return apikey

    apikey = str(apikey)
    assert len(apikey) > 0, f"API key must not be empty"

    if apikey == "apikey":
        apikey_path = "projects/forecast-161702/secrets/API_TEST_USER_KEY/versions/1"
        try:
            apikey = (
                secretmanager.SecretManagerServiceClient()
                .access_secret_version(request={"name": apikey_path})
                .payload.data.decode("UTF-8")
            )
        except Exception as e:
            raise ValueError("Supply your Salient api key")
    elif apikey == "testkey":
        # https://api.salientpredictions.com/accounts/testing
        apikey = "950d43ac7571d8a8"

    return apikey


def get_current_session() -> requests.Session:
    """Get the current session.

    All calls to the Salient API have a `session` argument
    that defaults to `None`.  If session is not passed to the
    function, the api call will use the output of this function.


    Returns:
        requests.Session: The current session if one was set via
            `login()` or `set_current_session()`, or a temporary
            session for use with `apikey`.
    """
    return requests.Session() if CURRENT_SESSION is None else CURRENT_SESSION


def set_current_session(session: requests.Session | None) -> None:
    """Set the current session.

    This function is called internally as a side effect of
    `login()`. In most cases, users will never need
    to call it explicitly.

    Args:
        session (requests.Session | None): The session that will be
              returned by `get_current_session()`.  Set `None` to
              clear the session.

    """
    assert session is None or isinstance(session, requests.Session)

    global CURRENT_SESSION
    CURRENT_SESSION = session


def get_verify_ssl(verify: bool | None = None) -> bool:
    """Get the current SSL verification setting.

    All functions that call the Salient API have a
    `verify` argument that controls whether or not to use
    SSL verification when making the call.  That argument
    will default to use this function, so in most cases
    users will never need to call it.

    Args:
        verify (bool | None): If `None` (default), returns the
            SSL verification setting that was set
            by `set_verify_ssl()` as a side effect of `login()`.
            If `True` or `False`, passes through without checking
            the default value.

    Returns:
        bool: The current SSL verification setting

    """
    if verify is None:
        verify = VERIFY_SSL
        if verify is None:
            verify = True

    verify = bool(verify)

    return verify


def set_verify_ssl(verify: bool = True) -> bool:
    """Set the SSL verification setting.

    Sets the default value to be used when calling
    `get_verify_ssl(None)`.
    This is usually set automatically as a side
    effect of `login(..., verify=None)` so in most
    cases users will never need to call it.

    Args:
        verify (bool): The SSL verification setting
           that will be returned by `get_verify_ssl()`.

    Returns:
        bool: The SSL verification setting that was set
    """
    global VERIFY_SSL
    VERIFY_SSL = bool(verify)
    return VERIFY_SSL


def login(
    username: str = "username",
    password: str = "password",
    apikey: str | None = None,
    verify: bool | None = None,
    verbose=False,
) -> requests.Session | None:
    """Login to the Salient API.

    This function is a local convenience wrapper around the Salient API
    [login](https://api.salientpredictions.com/v2/documentation/api/#/Authentication/login)
    endpoint.  It will use your credentials to create a persistent session you
    can use to execute API calls.

    Args:
        username (str): The username to login with
        password (str): The password to login with
        apikey (str | None): The API key to use instead of a login.
            If `None` (default) uses `username` and `password` to create a `Session`.
            If specified bypasses `login` and ignores `username` / `password`
        verify (bool): Whether to verify the SSL certificate.
            If `None` (default) will try `True` and then `False`, remembering the
            last successful setting and preserving it for future calls in `get_verify_ssl()`.
        verbose (bool): Whether to print the response status

    Returns:
        Session | None: Session object to pass to other API calls.
            As a side effect, will also set the default session for
            use with `get_current_session()`
    """
    if apikey is not None:
        set_current_session(None)  # clear out existing session, if there is one
        session = get_current_session()  # temporary session
        if verbose:
            print(f"Using API key {apikey} with a temporary Session {session}.")
        return session

    if username == "username" and password == "password":
        password_path = "projects/forecast-161702/secrets/API_TEST_USER_PWD/versions/1"
        try:
            password = (
                secretmanager.SecretManagerServiceClient()
                .access_secret_version(request={"name": password_path})
                .payload.data.decode("UTF-8")
            )
        except Exception as e:
            raise ValueError("Supply your Salient username and password")
        username = "testuser@salientpredictions.com"

    elif username == "testusr" and password == "testpwd":
        # https://api.salientpredictions.com/accounts/testing
        username = "help+test@salientpredictions.com"
        password = "salty!"

    if verify is None:
        try:
            session = login(username, password, verify=True, verbose=verbose)
            set_verify_ssl(True)
        except requests.exceptions.SSLError:
            session = login(username, password, verify=False, verbose=verbose)
            set_verify_ssl(False)
        return session

    auth = (username, password)
    (url, file_name) = _build_url("login")

    session = requests.Session()
    login_ok = session.get(url, auth=auth, verify=verify)
    login_ok.raise_for_status()

    if verbose:
        print(login_ok.text)

    set_current_session(session)

    return session


def download_queries(
    query: list[str],
    file_name: list[str],
    format: str = "-auto",
    force: bool = False,
    session: requests.Session | None = None,
    verify: bool | None = None,
    verbose: bool = False,
    max_workers: int | None = None,
) -> None:
    """Downloads multiple queries saves them to a file.

    This function handles the downloading of data based on the provided query URLs.
    It saves the data to the specified file names.
    If the file already exists and `force` is not set to True, the download is skipped.
    Download will happen in parallel.

    Parameters:
        query (list[str]): The URLs from which to download the data.
        file_name (list[str]): The paths where the data will be saved.
        format (str, optional): The format of the file.
            Defaults to '-auto', which will infer the format from the file extension.
        force (bool, optional): If True, the file will be downloaded even if it already exists.
            Defaults to False.
        session (requests.Session, optional): The session to use for the download.
            If `None` (default) uses `get_current_session()`.
        verify (bool, optional): Whether to verify the server's TLS certificate.
            Defaults to the current verification setting via `get_verify_ssl()`.
        verbose (bool, optional): If True, prints additional output about the download process.
            Defaults to False.
        max_workers (int, optional): The maximum number of threads to use for downloading.


    Raises:
        requests.HTTPError: If the server returns an error status code.
    """
    assert len(query) == len(file_name)

    if len(query) == 0:
        return None
    elif len(query) == 1:
        # Much of the time we won't have vectorized queries.  Keep it simple.
        download_query(query[0], file_name[0], format, force, session, verify, verbose)
        return None

    if max_workers is None:
        # This is the default value for ThreadPoolExecutor
        max_workers = os.cpu_count() * 5

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_query, qry, fil, format, force, session, verify, verbose)
            for qry, fil in zip(query, file_name)
        ]
        for future in futures:
            future.result()  # raises exceptions

    return None


def download_query(
    query: str,
    file_name: str,
    format: str = "-auto",
    force: bool = False,
    session: requests.Session | None = None,
    verify: bool = None,
    verbose: bool = False,
) -> [requests.Response | None]:
    """Downloads the query result and saves it to a file.

    This function handles the downloading of data based on the provided query URL.
    It saves the data to the specified file name.
    If the file already exists and `force` is not set to True, the download is skipped.

    Parameters:
        query (str): The URL from which to download the data.
        file_name (str): The path where the data will be saved.
        format (str, optional): The format of the file.
            Defaults to '-auto', which will infer the format from the file extension.
        force (bool, optional): If False (default) skips downloading `file_name` if it already exists.
        session (requests.Session, optional): The session to use for the download.
            If `None` (default) uses `get_current_session()`.
        verify (bool, optional): Whether to verify the server's TLS certificate.
            If `None` (default) uses the current verification setting via `get_verify_ssl()`.
        verbose (bool, optional): If True, prints additional output about the download process.
            Defaults to False.

    Returns:
        requests.Response | None: The response object from the server after attempting the download,
            or None if the file was already cached and not re-downloaded.

    Raises:
        requests.HTTPError: If the server returns an error status code.
    """
    if format == "-auto":
        # extract the file extension from the file name
        format = file_name.split(".")[-1]

    if session is None:
        session = get_current_session()

    verify = get_verify_ssl(verify)

    result = None
    if force or not os.path.exists(file_name):
        if verbose:
            print(f"Downloading\n  {query}\n to {file_name}\n with {session}")
        result = session.get(query, verify=verify)
        result.raise_for_status()
        with open(file_name, "wb" if format == "nc" else "w") as f:
            if format == "nc":
                f.write(result.content)
            else:
                f.write(result.text)
    elif verbose:
        print(f"File {file_name} already exists")

    return result
