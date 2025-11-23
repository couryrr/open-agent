import os
import pytest
from openrunner.tooling import OpenRunnerTooling
from openrunner.tooling import OpenRunnerToolingError


@pytest.fixture
def tooling():
    return OpenRunnerTooling()


def test_create_provider_script(tooling):
    tooling = OpenRunnerTooling()
    tooling.create_provider_script("temp", "test_1")
    assert os.path.exists(os.path.join("temp", "providers", "test_1.py"))
    os.remove(os.path.join("temp", "providers", "test_1.py"))
    os.rmdir(os.path.join("temp", "providers"))
    os.rmdir("temp")

def test_create_provider_script_already_exists(tooling):
    tooling.create_provider_script("temp", "test_2")
    with pytest.raises(OpenRunnerToolingError):
        tooling.create_provider_script("temp", "test_2")
    os.remove(os.path.join("temp", "providers", "test_2.py"))
    os.rmdir(os.path.join("temp", "providers"))
    os.rmdir("temp")


