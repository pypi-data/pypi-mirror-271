



import httpx

from ._constants import (
    DEFAULT_LIMITS,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    RAW_RESPONSE_HEADER,
    DEFAULT_HEADERS
)
from typing_extensions import Literal, override

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Type,
    Union,
    Generic,
    Mapping,
    TypeVar,
    Iterable,
    Iterator,
    Optional,
    Generator,
    AsyncIterator,
    cast,
    overload,
)

import distro

from typing import Union, Mapping
from ._streaming import Stream as Stream
import platform
from . import resources
import os
from ._exceptions import RobinError


__all__ = [
    "RobinAIClient",
]


def _merge_mappings(
    obj1,
    obj2,
):
    """Merge two mappings of the same type, removing any values that are instances of `Omit`.
    In cases with duplicate keys the second mapping takes precedence.
    """
    return {**obj1, **obj2}


Platform = Union[
    Literal[
        "MacOS",
        "Linux",
        "Windows",
        "FreeBSD",
        "OpenBSD",
        "iOS",
        "Android",
        "Unknown",
    ],
]


def get_platform() -> Platform:
    system = platform.system().lower()
    platform_name = platform.platform().lower()
    if "iphone" in platform_name or "ipad" in platform_name:
        # Tested using Python3IDE on an iPhone 11 and Pythonista on an iPad 7
        # system is Darwin and platform_name is a string like:
        # - Darwin-21.6.0-iPhone12,1-64bit
        # - Darwin-21.6.0-iPad7,11-64bit
        return "iOS"

    if system == "darwin":
        return "MacOS"

    if system == "windows":
        return "Windows"

    if "android" in platform_name:
        # Tested using Pydroid 3
        # system is Linux and platform_name is a string like 'Linux-5.10.81-android12-9-00001-geba40aecb3b7-ab8534902-aarch64-with-libc'
        return "Android"

    if system == "linux":
        # https://distro.readthedocs.io/en/latest/#distro.id
        distro_id = distro.id()
        if distro_id == "freebsd":
            return "FreeBSD"

        if distro_id == "openbsd":
            return "OpenBSD"

        return "Linux"

    if platform_name:
        return platform_name

    return "Unknown"

class OtherArch:
    def __init__(self, name: str) -> None:
        self.name = name

    @override
    def __str__(self) -> str:
        return f"other:{self.name}"
    
Arch = Union[OtherArch, Literal["x32", "x64", "arm", "arm64", "unknown"]]
def get_architecture() -> Arch:
    python_bitness, _ = platform.architecture()
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64"

    # TODO: untested
    if machine == "arm":
        return "arm"

    if machine == "x86_64":
        return "x64"

    # TODO: untested
    if python_bitness == "32bit":
        return "x32"

    if machine:
        return OtherArch(machine)

    return "unknown"


class RobinAIClient():
    #completions: resources.Completions
    #completions_based_text: resources.Completions
    #upload_file: resources.Completions
    #models: resources.Models
    #fine_tuning: resources.FineTuning
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: int =  DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async ROBIN client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ROBIN_API_KEY`
        """
        if api_key is None:
            api_key = os.environ.get("ROBIN_API_KEY")
        if api_key is None:
            raise RobinError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ROBIN_API_KEY environment variable"
            )
        if default_headers is None:
            self.default_headers = DEFAULT_HEADERS

        self.api_key = api_key

        if base_url is None:
            base_url = f"https://robin-ai.xyz:8443/api/api-response-service/"

        self._default_stream_cls = Stream
        headers = self._build_headers()
        self.http_client = http_client or httpx.Client(
            base_url=base_url,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=timeout,
            verify=False,
            headers=headers
        )

        self.completions = resources.Completions(self)
        #self.completions_based_text: resources.Completions
        #self.upload_file: resources.Completions
        #self.models: resources.Models
        #self.fine_tuning: resources.FineTuning


    @property
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}
    

    def _build_headers(self) -> httpx.Headers:
        headers_dict = _merge_mappings(self.default_headers, self.auth_headers)
        headers_dict = _merge_mappings(headers_dict, self.platform_headers())
        headers = httpx.Headers(headers_dict)
        return headers
    
    def platform_headers(self) -> Dict[str, str]:
        return {
            "X-Stainless-Lang": "python",
            #"X-Stainless-Package-Version": self._version,
            "X-Stainless-OS": str(get_platform()),
            "X-Stainless-Arch": str(get_architecture()),
            "X-Stainless-Runtime": platform.python_implementation(),
            "X-Stainless-Runtime-Version": platform.python_version(),
        }
    


Client = RobinAIClient