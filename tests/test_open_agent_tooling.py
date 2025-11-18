import os
import pytest
from openagent.tooling import OpenAgentTooling
from openagent.tooling import OpenAgentToolingError


@pytest.fixture
def tooling():
    return OpenAgentTooling()


def test_create_provider_script(tooling):
    tooling = OpenAgentTooling()
    tooling.create_provider_script("temp", "test_1")
    assert os.path.exists(os.path.join("temp", "test_1.py"))
    os.remove(os.path.join("temp", "test_1.py"))
    os.rmdir("temp")

def test_create_provider_script_already_exists(tooling):
    tooling.create_provider_script("temp", "test_2")
    with pytest.raises(OpenAgentToolingError):
        tooling.create_provider_script("temp", "test_2")
    os.remove(os.path.join("temp", "test_2.py"))
    os.rmdir("temp")


