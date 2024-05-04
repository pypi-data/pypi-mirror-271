import json
from pathlib import Path
from contextlib import contextmanager


from ploomber_cloud.util import pretty_print, raise_error_on_duplicate_keys
from ploomber_cloud.constants import VALID_PROJECT_TYPES, FORCE_INIT_MESSAGE
from ploomber_cloud.exceptions import InvalidPloomberConfigException


@contextmanager
def path_to_config(path_new):
    """
    Context manager to temporarily change the path that PloomberCloudConfig uses to
    read/write the config file.
    """
    CURRENT_PATH = PloomberCloudConfig.PATH_TO_CONFIG

    if path_new is not None:
        PloomberCloudConfig.PATH_TO_CONFIG = path_new

    try:
        yield
    finally:
        PloomberCloudConfig.PATH_TO_CONFIG = CURRENT_PATH


class PloomberCloudConfig:
    """Manages the ploomber-cloud.json file"""

    PATH_TO_CONFIG = "ploomber-cloud.json"

    def __init__(self) -> None:
        self._path = Path(self.PATH_TO_CONFIG)
        self._data = None

    @property
    def data(self):
        """Return the data stored in the config file"""
        if self._data is None:
            raise RuntimeError("Data has not been loaded")

        return self._data

    def exists(self):
        """Return True if the config file exists, False otherwise"""
        return self._path.exists()

    def _validate_labels(self):
        if "labels" not in self._data.keys():
            return None
        for label in self._data["labels"]:
            if not isinstance(label, str):
                return (
                    f"'labels' must be a list of strings. "
                    f"Found invalid label: {label}.\n"
                )

    def _validate_secret_keys(self):
        if "secret-keys" not in self._data.keys():
            return None
        for key in self._data["secret-keys"]:
            if not isinstance(key, str):
                return (
                    f"'secret-keys' must be a list of strings. "
                    f"Found invalid key: {key}.\n"
                )

    def _validate_resources(self):
        if "resources" not in self._data.keys():
            return None

        error = ""
        resources = self._data["resources"]

        KEYS_RESOURCES = {"cpu", "ram", "gpu"}
        RESOURCES_TYPES = {"cpu": float, "ram": int, "gpu": int}
        for required_key in KEYS_RESOURCES:
            if required_key not in resources.keys():
                error = f"{error}Mandatory key '{required_key}' is missing.\n"

        for resource, resource_value in resources.items():
            if resource not in KEYS_RESOURCES:
                error = (
                    f"{error}Invalid resource: '{resource}'. "
                    f"Valid keys are: {pretty_print(KEYS_RESOURCES)}\n"
                )
            elif not isinstance(resource_value, RESOURCES_TYPES[resource]):
                error = (
                    f"{error}Only {RESOURCES_TYPES[resource].__name__} "
                    f"values allowed for resource '{resource}'\n"
                )

        if error:  # Add fix resources message if resources have error
            error = f"{error}To fix it, run 'ploomber-cloud resources --force'\n"

        return error

    def _validate_config(self):
        """Method to validate the ploomber-cloud.json file
        for common issues"""
        KEYS_REQUIRED = {"id", "type"}
        KEYS_OPTIONAL = {"resources", "template", "labels", "secret-keys"}
        TYPES = {
            "id": str,
            "type": str,
            "resources": dict,
            "template": str,
        }

        error = ""

        for key in KEYS_REQUIRED:
            if key not in self._data.keys():
                error = f"{error}Mandatory key '{key}' is missing.\n"

        for key, value in self._data.items():
            if key not in KEYS_REQUIRED | KEYS_OPTIONAL:
                error = (
                    f"{error}Invalid key: '{key}'. "
                    f"Valid keys are: {pretty_print(KEYS_REQUIRED | KEYS_OPTIONAL)}\n"
                )
            elif value == "":
                error = f"{error}Missing value for key '{key}'\n"
            elif key in TYPES and not isinstance(value, TYPES[key]):
                error = (
                    f"{error}Only {TYPES[key].__name__} "
                    f"values allowed for key '{key}'\n"
                )
            elif key == "labels" and not isinstance(value, list):
                error = "'labels' must be a list of strings.\n"
            elif key == "secret-keys" and not isinstance(value, list):
                error = "'secret-keys' must be a list of strings.\n"
            elif key == "type" and value not in VALID_PROJECT_TYPES:
                error = (
                    f"{error}Invalid type '{value}'. "
                    f"Valid project types are: "
                    f"{pretty_print(VALID_PROJECT_TYPES)}\n"
                )

        resources_error = self._validate_resources()
        if resources_error:
            error = f"{error}{resources_error}"

        labels_error = self._validate_labels()
        if labels_error:
            error = f"{error}{labels_error}"

        secret_keys_error = self._validate_secret_keys()
        if secret_keys_error:
            error = f"{error}{secret_keys_error}"

        if error:
            raise InvalidPloomberConfigException(
                f"There are some issues with the ploomber-cloud.json file:\n{error}\n"
                f"{FORCE_INIT_MESSAGE}\n"
            )

    def load(self):
        """
        Load the config file. Accessing data will raise an error if this
        method hasn't been executed
        """
        if not self.exists():
            raise InvalidPloomberConfigException(
                "Project not initialized. "
                "Run 'ploomber-cloud init' to initialize your project."
            )

        try:
            self._data = json.loads(
                self._path.read_text(), object_pairs_hook=raise_error_on_duplicate_keys
            )
        except ValueError as e:
            error_message = "Please add a valid ploomber-cloud.json file."
            if "Duplicate keys" in str(e):
                error_message = f"{error_message} {str(e)}"
            raise InvalidPloomberConfigException(
                f"{error_message}\n{FORCE_INIT_MESSAGE}"
            ) from e
        self._validate_config()

    def dump(self, data_new):
        """Dump data to the config file"""
        self._data = data_new
        self._path.write_text(json.dumps(data_new, indent=4))

    def __setitem__(self, key, value):
        self._data[key] = value
        self._validate_config()
        self.dump(self._data)

    def __delitem__(self, key):
        if key not in self._data:
            raise InvalidPloomberConfigException(f"Key does not exist: {key}")
        del self._data[key]
        self.dump(self._data)
