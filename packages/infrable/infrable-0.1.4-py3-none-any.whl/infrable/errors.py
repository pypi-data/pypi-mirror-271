class Error(Exception):
    pass


class FQDNMustNotBeEmptyError(Error, ValueError):
    def __init__(self):
        super().__init__(f"Error: FQDN must not be empty")


class MissingMetadataError(Error, ValueError):
    def __init__(self, src):
        super().__init__(f"missing metadata in template: {src}")


class MissingDestinationError(Error, ValueError):
    def __init__(self, src):
        super().__init__(f"missing `dest` in template metadata: {src}")


class InvalidDestinationError(Error, ValueError):
    def __init__(self, dest):
        super().__init__(f"invalid destination: {dest}")


class InfraDotPyNotFoundError(Error, ImportError):
    def __init__(self, modulename):
        super().__init__(f"{modulename}.py: file not found")


class HostOrServiceNotFoundError(Error, KeyError):
    def __init__(self, name):
        super().__init__(f"{name}: host or service not found")


class SwitchValueError(Error, ValueError):
    def __init__(self, path, value, options):
        options = ", ".join(options)
        super().__init__(
            f"Invalid value {value} for switch {path}. Options are: {options}"
        )


class SwitchCaseError(Error, ValueError):
    def __init__(self, path, options, cases):
        _options = ", ".join(options)
        _cases = ", ".join(cases.keys())

        super().__init__(
            f"{path}: cases are incompatible with the options."
            f" Options are: {_options}, Cases are: {_cases}"
        )


class SwitchError(Error, ValueError):
    def __init__(self, path, val, cases):
        _cases = ", ".join(cases.keys())
        super().__init__(
            f"{path}: switch value is set to {val},"
            f" but no case matched. Cases are: {_cases}"
        )
