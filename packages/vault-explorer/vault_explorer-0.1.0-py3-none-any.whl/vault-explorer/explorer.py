import hvac
import urllib.parse
import flatten_json
from typing import Callable, Any, List


def _isDirectory(path: "str") -> "bool":
    return path.endswith("/")


def _flatten(contents: "dict") -> "dict":
    return flatten_json.flatten(contents, "/")


class VaultExplorer:

    def __init__(self: "VaultExplorer", client: "hvac.Client", *, flattenJson: "bool" = False) -> "None":
        self._client = client
        self._flattenJson = flattenJson

    def apply(self: "VaultExplorer", path: "str", function: "Callable[[str, Any], None]") -> "None":
        self._explore(path, function)

    def _explore(self: "VaultExplorer", path: "str", function: "Callable[[str, Any], None]") -> "None":
        for currentPath in self._listDirectory(path):
            if _isDirectory(currentPath):
                self._explore(currentPath, function)
            else:
                self._apply(currentPath, function)

    def _apply(self: "VaultExplorer", path: "str", function: "Callable[[str, Any], None]") -> "None":
        contents = self._getContents(path)
        if self._flattenJson:
            for key, item in _flatten(contents).items():
                function(urllib.parse.urljoin(path, key), item)
        else:
            function(path, contents)

    def _listDirectory(self: "VaultExplorer", path: "str") -> "List[str]":
        if not _isDirectory(path):
            raise ValueError(f"Attempting to list directory on non-directory path: {path}")

        secrets = self._listSecrets(path)

        if "data" not in secrets or "keys" not in secrets["data"]:
            raise ValueError(f"Invalid data structure when listing contents at path: {path}")

        return [urllib.parse.urljoin(path, key) for key in secrets["data"]["keys"]]

    def _getContents(self: "VaultExplorer", path: "str") -> "Any":
        if _isDirectory(path):
            raise ValueError(f"Attempting to get contents on a directory path: {path}")

        secret = self._readSecret(path)

        if "data" not in secret or "data" not in secret["data"]:
            raise ValueError("Invalid data structure when getting path contents at path: {path}")

        return secret["data"]["data"]

    def _listSecrets(self: "VaultExplorer", path: "str") -> "dict":
        try:
            return self._client.secrets.kv.v2.list_secrets(path=path)
        except Exception as exception:
            raise RuntimeError(f"An error occured listing directory at path: {path}", exception)

    def _readSecret(self: "VaultExplorer", path: "str") -> "dict":
        try:
            return self._client.secrets.kv.v2.read_secret_version(path=path, raise_on_deleted_version=False)
        except Exception as exception:
            raise RuntimeError(f"An error occured getting contents at path: {path}", exception)
