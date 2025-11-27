import os


class OpenRunnerTooling:
    def __init__(self):
        self.tool_directory = "providers"

    def create_provider_script(self, directory: str, file_name: str) -> None:
        provider_directory = os.path.join(directory, self.tool_directory)
        file_path = os.path.join(provider_directory, f"{file_name}.py")
        if os.path.exists(file_path):
            raise OpenRunnerToolingError(f"File {file_path} already exists")

        if not os.path.exists(provider_directory):
            os.makedirs(provider_directory)

        with open(file_path, "w") as file:
            file.write("")


class OpenRunnerToolingError(Exception):
    pass
