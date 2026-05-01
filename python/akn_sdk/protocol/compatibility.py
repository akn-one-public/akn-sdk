# akn_sdk/protocol/compatibility.py

from ..version import SUPPORTED_PROTOCOL_VERSIONS
from ..exceptions import ProtocolVersionError


def ensure_supported(version: str):
    if version not in SUPPORTED_PROTOCOL_VERSIONS:
        raise ProtocolVersionError(
            f"Unsupported protocol version: {version}"
        )