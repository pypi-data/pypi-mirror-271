# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import configparser
import json
import os
import time
import warnings
from enum import Enum
from importlib import metadata
from urllib.parse import urlparse

import click
import requests
import urllib3

from kadi_apy.cli.lib.misc import Miscellaneous
from kadi_apy.globals import CONFIG_PATH
from kadi_apy.globals import Verbose
from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template
from kadi_apy.lib.resources.users import User
from kadi_apy.lib.search import Search


def _key_exit(key, instance):
    raise KadiAPYConfigurationError(
        f"Please define the key '{key}' for instance '{instance}' in the config file."
    )


def _read_config(config, value, instance):
    try:
        value_read = config[instance][value]
    except:
        _key_exit(value, instance)
    if not value_read:
        _key_exit(value, instance)
    return value_read


def _read_verify(config, instance):
    try:
        return config[instance].getboolean("verify")
    except ValueError as e:
        raise KadiAPYConfigurationError(
            "Please set either 'True' or 'False' in the config file for the"
            " key 'verify'."
        ) from e


def _read_timeout(config, instance):
    try:
        return config[instance].getint("timeout")
    except ValueError as e:
        raise KadiAPYConfigurationError(
            "Please set an integer in the config file for the key 'timeout'."
        ) from e


def _read_ca_bundle(config, instance):
    ca_bundle = config[instance]["ca_bundle"]

    if not os.path.isfile(ca_bundle):
        raise KadiAPYConfigurationError(
            f"CA bundle file does not exist at '{ca_bundle}'."
        )
    return ca_bundle


def _read_whitelist(config, instance):
    return [host.strip() for host in config[instance]["whitelist"].split(",")]


class KadiManager:
    r"""Base manager class for the API.

    Manages the host and the personal access token (PAT) to use for all API requests.
    The KadiManager can instantiate new resources (e.g. records) via factory methods.

    :param instance: The name of the instance to use in combination with a config file.
    :type instance: str, optional
    :param host: Name of the host.
    :type host: str, optional
    :param token: Personal access token.
    :type token: str, optional
    :param verify: Whether to verify the SSL/TLS certificate of the host.
    :type verify: bool, optional
    :param timeout: Timeout in seconds for the requests.
    :type timeout: float, optional
    :param whitelist: A list of hosts that kadi-apy is allowed to redirect to.
    :type whitelist: list, optional
    :param verbose: Global verbose level to define the amount of prints.
    :type verbose: optional
    """

    def __init__(
        self,
        instance=None,
        host=None,
        token=None,
        verify=True,
        timeout=60,
        whitelist=None,
        verbose=None,
    ):
        self.instance = instance
        self.host = host
        self.token = token
        self.verify = verify
        self.timeout = timeout
        self.whitelist = whitelist if whitelist is not None else []
        self.verbose = verbose

        self._pkg_version = metadata.version("kadi-apy")
        self._session = requests.Session()
        self._pat_user = None
        self._misc = None
        self._search = None

        if host is None and token is None:
            if not os.path.isfile(CONFIG_PATH):
                raise KadiAPYConfigurationError(
                    f"Config file does not exist at '{CONFIG_PATH}'.\n"
                    "You can run 'kadi-apy config create' to create the config file at"
                    f" '{CONFIG_PATH}'."
                )

            if os.name == "posix" and (os.stat(CONFIG_PATH).st_mode & 0o777) != 0o600:
                warnings.warn(
                    "It is recommended to keep the permissions of the config file at"
                    f" '{CONFIG_PATH}' restrictive (read/write for the file owner"
                    " only)."
                )

            config = configparser.ConfigParser()

            try:
                config.read(CONFIG_PATH)
            except configparser.ParsingError as e:
                raise KadiAPYConfigurationError(
                    f"Error during parsing of config file:\n{e}"
                ) from e

            if self.instance is None:
                try:
                    self.instance = config["global"]["default"]
                except Exception as e:
                    raise KadiAPYConfigurationError(
                        "No default instance defined in the config file at"
                        f" '{CONFIG_PATH}'."
                    ) from e

            instances = config.sections()
            instances.remove("global")

            if self.instance not in instances:
                raise KadiAPYConfigurationError(
                    "Please use an instance which is defined in the config file.\n"
                    f"Choose one of {instances}"
                )

            self.token = _read_config(config, "pat", self.instance)
            self.host = _read_config(config, "host", self.instance)

            if "verify" in config[self.instance]:
                self.verify = _read_verify(config, self.instance)
            elif "verify" in config["global"]:
                self.verify = _read_verify(config, "global")

            if self.verify is True:
                if "ca_bundle" in config[self.instance]:
                    self.verify = _read_ca_bundle(config, self.instance)
                elif "ca_bundle" in config["global"]:
                    self.verify = _read_ca_bundle(config, "global")

            if "timeout" in config[self.instance]:
                self.timeout = _read_timeout(config, self.instance)
            elif "timeout" in config["global"]:
                self.timeout = _read_timeout(config, "global")

            if "whitelist" in config[self.instance]:
                self.whitelist = _read_whitelist(config, self.instance)
            elif "whitelist" in config["global"]:
                self.whitelist = _read_whitelist(config, "global")

        if self.host is None:
            raise KadiAPYConfigurationError("No host information provided.")

        if self.token is None:
            raise KadiAPYConfigurationError("No personal access token (PAT) provided.")

        if self.host.endswith("/"):
            self.host = self.host[:-1]

        if not self.host.endswith("/api"):
            self.host = self.host + "/api"

        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    @property
    def pat_user(self):
        """Get the user related to the PAT.

        :return: The user.
        :rtype: User
        """
        if self._pat_user is None:
            self._pat_user = self.user(use_pat=True)

        return self._pat_user

    @property
    def misc(self):
        """Central entry point for miscellaneous functionality."""
        if self._misc is None:
            self._misc = Miscellaneous(self)

        return self._misc

    @property
    def search(self):
        """Central entry point for search functionality."""
        if self._search is None:
            self._search = Search(self)

        return self._search

    def _make_request(
        self, endpoint, method=None, headers=None, is_redirect=False, **kwargs
    ):
        headers = headers if headers is not None else {}

        if endpoint.startswith("/"):
            endpoint = self.host + endpoint

        self.debug(f"----- Request Info -----\nMethod: {method}\nEndpoint: {endpoint}")

        try:
            self.debug(f"Kwargs: {json.dumps(kwargs, indent=4)}")
        except:
            pass

        self.debug("------------------------")

        if is_redirect:
            headers.pop("Authorization", None)
        elif "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.token}"

        if "User-Agent" not in headers:
            headers["User-Agent"] = f"kadi-apy/{self._pkg_version}"

        response = getattr(self._session, method)(
            endpoint,
            headers=headers,
            verify=self.verify,
            timeout=self.timeout,
            allow_redirects=False,
            **kwargs,
        )

        if response.is_redirect:
            location = response.headers["Location"]
            parsed_url = urlparse(location)
            host = f"{parsed_url.scheme}://{parsed_url.netloc}"

            if host in self.whitelist:
                return self._make_request(
                    location, method=method, headers=headers, is_redirect=True, **kwargs
                )

            raise KadiAPYRequestError(
                f"The server answered with a redirection to '{host}'. Please either use"
                " this host name for your configured Kadi4Mat instance, if the host"
                " name of the instance changed, or add it to the redirect whitelist in"
                " the config file."
            )

        # Check if the rate limit has been exceeded.
        if response.status_code == 429:
            time.sleep(int(response.headers.get("Retry-After", 1)))
            return self._make_request(
                endpoint, method=method, headers=headers, **kwargs
            )

        return response

    def _get(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="get", **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="post", **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="patch", **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="put", **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="delete", **kwargs)

    def make_request(self, endpoint, method="get", **kwargs):
        r"""Low level functionality to perform a request.

        This function can be used to use endpoints for which no own functions exist yet.

        :param endpoint: Endpoint to use for the request.
        :type endpoint: str
        :param method: Method to use for the request. One of ``"get"``, ``"post"``,
            ``"patch"``, ``"put"`` or ``"delete"``.
        :type method: str, optional
        :param \**kwargs: Additional arguments for the request.
        :raises KadiAPYInputError: If the specified method is invalid.
        :raises KadiAPYRequestError: If the server answered with an invalid redirection.
        """

        if method not in ["get", "post", "patch", "put", "delete"]:
            raise KadiAPYInputError(f"No valid method given ('{method}').")

        return self._make_request(endpoint, method, **kwargs)

    def record(self, **kwargs):
        r"""Init a record.

        :param \**kwargs: Arguments to initialize the record with.
        :return: The record.
        :rtype: Record
        :raises KadiAPYRequestError: If initializing the record was not successful.
        """

        return Record(manager=self, **kwargs)

    def collection(self, **kwargs):
        r"""Init a collection.

        :param \**kwargs: Arguments to initialize the collection with.
        :return: The collection.
        :rtype: Collection
        :raises KadiAPYRequestError: If initializing the collection was not successful.
        """

        return Collection(manager=self, **kwargs)

    def template(self, **kwargs):
        r"""Init a template.

        :param \**kwargs: Arguments to initialize the template with.
        :return: The template.
        :rtype: Template
        :raises KadiAPYRequestError: If initializing the template was not successful.
        """

        return Template(manager=self, **kwargs)

    def group(self, **kwargs):
        r"""Init a group.

        :param \**kwargs: Arguments to initialize the group with.
        :return: The group.
        :rtype: Group
        :raises KadiAPYRequestError: If initializing the group was not successful.
        """

        return Group(manager=self, **kwargs)

    def user(self, **kwargs):
        r"""Init a user.

        :param \**kwargs: Arguments to initialize the user with.
        :return: The user.
        :rtype: User
        :raises KadiAPYRequestError: If initializing the user was not successful.
        """

        return User(manager=self, **kwargs)

    def is_verbose(self, verbose_level=Verbose.INFO):
        """Check the verbose level.

        :param verbose_level: Local verbose level of the function.
        :return: ``True`` if verbose level is reached, ``False`` otherwise.
        :rtype: bool
        """

        if isinstance(verbose_level, Enum):
            value_verbose_level_local = verbose_level.value
        else:
            value_verbose_level_local = verbose_level

        if isinstance(self.verbose, Enum):
            value_verbose_level_global = self.verbose.value
        else:
            value_verbose_level_global = self.verbose

        if (
            self.verbose is None
            or value_verbose_level_global > value_verbose_level_local
        ):
            return False

        return True

    def error(self, text, **kwargs):
        r"""Print text for error level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.ERROR, **kwargs)

    def warning(self, text, **kwargs):
        r"""Print text for warning level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.WARNING, **kwargs)

    def info(self, text, **kwargs):
        r"""Print text for info level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.INFO, **kwargs)

    def debug(self, text, **kwargs):
        r"""Print text for debug level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.DEBUG, **kwargs)

    def echo(self, text, verbose_level, **kwargs):
        r"""Print text via :func:`click.echo()` if global verbose level is reached.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param verbose_level: Verbose level.
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        """

        if self.is_verbose(verbose_level):
            click.echo(text, **kwargs)
