import os


class OpenAgentTooling:
    def create_provider_script(self, directory: str, file_name: str) -> None:
        file_path = os.path.join(directory, f"{file_name}.py")
        if os.path.exists(file_path):
            raise OpenAgentToolingError(f"File {file_path} already exists")

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        print(f"Creating {file_path}")
        with open(file_path, "w") as file:
            file.write("")


class OpenAgentToolingError(Exception):
    pass
