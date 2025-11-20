import importlib.util
import os
from typing import Protocol, runtime_checkable


@runtime_checkable
class YourProtocol(Protocol):
    def __init__(self):
        pass

    def smoke_test(self):
        print("smoke test passed")


class OpenAgentTooling:
    def __init__(self):
        self.providers = "providers"

    def create_provider_script(self, directory: str, file_name: str) -> None:
        provider_directory = os.path.join(directory, self.providers)
        file_path = os.path.join(provider_directory, f"{file_name}.py")
        if os.path.exists(file_path):
            raise OpenAgentToolingError(f"File {file_path} already exists")

        if not os.path.exists(provider_directory):
            os.makedirs(provider_directory)

        with open(file_path, "w") as file:
            file.write("")

    def smoke_test(self, directory: str, file_name: str) -> None:
        provider_directory = os.path.join(directory, self.providers)
        file_path = os.path.join(provider_directory, file_name)
        if not os.path.exists(file_path):
            raise OpenAgentToolingError(f"File {file_path} does not exist")

        # Extract module name from filename (remove .py)
        module_name = file_name.removesuffix(".py")

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"No module named {module_name}")

        module = importlib.util.module_from_spec(spec)

        if spec.loader is None:
            raise ImportError(f"No loader for {module_name}")

        spec.loader.exec_module(module)
        provider_class = getattr(module, "Provider")

        # Validate against protocol
        if not isinstance(provider_class(), YourProtocol):
            raise TypeError(f"{file_name} doesn't implement required protocol")

        p = provider_class()
        p.smoke_test()


class OpenAgentToolingError(Exception):
    pass
