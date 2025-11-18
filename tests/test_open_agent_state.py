import os
import pytest

from openagent import OpenAgent, OpenAgentProvider


@pytest.fixture
def open_agent():
    os.makedirs("temp")
    open_agent = OpenAgent()
    open_agent.state.data_dir = "temp"
    yield open_agent
    os.rmdir("temp")

def test_open_agent_can_add_provider(open_agent):
    assert len(open_agent.state.providers) == 0
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(open_agent.state.providers) == 1


def test_open_agent_can_add_multiple_providers(open_agent):
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        open_agent.add_provider(provider)
    assert len(open_agent.state.providers.keys()) == 5


def test_open_agent_can_remove_provider(open_agent):
    name = "1"
    provider = OpenAgentProvider(name=name)
    open_agent.add_provider(provider)
    assert len(open_agent.state.providers) == 1
    open_agent.remove_provider(name=name)
    assert len(open_agent.state.providers) == 0


def test_open_agent_removes_correct_provider(open_agent):
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        open_agent.add_provider(provider)
    assert len(open_agent.state.providers) == 5
    open_agent.remove_provider(name="4")
    assert len(open_agent.state.providers.keys()) == 4
    assert [str(i) for i in range(4)] == [
        provider for provider in open_agent.state.providers.keys()
    ]


def test_open_agent_removes_correct_providers(open_agent):
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        open_agent.add_provider(provider)
    assert len(open_agent.state.providers) == 5
    open_agent.remove_provider(name="4")
    open_agent.remove_provider(name="2")
    assert len(open_agent.state.providers) == 3
    assert ["0", "1", "3"] == [provider for provider in open_agent.state.providers.keys()]


def test_open_agent_can_add_model_to_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    open_agent.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    open_agent.add_provider_model(name="1", model="some_llm_name")


def test_open_agent_can_add_multiple_models_to_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    for i in range(5):
        open_agent.add_provider_model(name="1", model=f"some_llm_name_{i}")
    assert len(provider.models) == 5


def test_open_agent_cannt_add_model_to_non_existent_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    with pytest.raises(Exception):
        open_agent.add_provider_model(name="2", model="some_llm_name")
    assert len(provider.models) == 0


def test_open_agent_can_remove_model_from_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    open_agent.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    open_agent.remove_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 0


def test_open_agent_can_remove_multiple_models_from_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    for i in range(5):
        open_agent.add_provider_model(name="1", model=f"some_llm_name_{i}")
    assert len(provider.models) == 5
    open_agent.remove_provider_model(name="1", model="some_llm_name_0")
    assert len(provider.models) == 4
    expected = set([f"some_llm_name_{i}" for i in range(1, 5)])
    assert provider.models == expected


def test_open_agent_removes_correct_model_from_multiple_provider(open_agent):
    provider1 = OpenAgentProvider(name="1")
    open_agent.add_provider(provider1)
    provider2 = OpenAgentProvider(name="2")
    open_agent.add_provider(provider2)
    assert len(provider1.models) == 0
    assert len(provider2.models) == 0
    for i in range(5):
        open_agent.add_provider_model(name="1", model=f"some_llm_name_{i}")
        open_agent.add_provider_model(name="2", model=f"some_llm_name_{i}")
    assert len(provider1.models) == 5
    assert len(provider2.models) == 5
    open_agent.remove_provider_model(name="1", model="some_llm_name_0")
    assert len(provider1.models) == 4
    assert len(provider2.models) == 5


def test_open_agent_cant_remove_model_from_non_existent_provider(open_agent):
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    open_agent.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    with pytest.raises(Exception):
        open_agent.remove_provider_model(name="2", model="some_llm_name")


def test_open_agent_can_list_providers(open_agent):
    assert len(open_agent.state.providers) == 0
    for i in range(5):
        name = f"agent_{i}"
        open_agent.add_provider(OpenAgentProvider(name=name))
    assert len(open_agent.state.providers) == 5
    assert [provider.name for provider in open_agent.list_providers()] == [
        f"agent_{i}" for i in range(5)
    ]


def test_open_agent_can_list_sessions(open_agent):
    assert len(open_agent.state.sessions) == 0
    for i in range(5):
        session_name = f"session_{i}"
        name = f"agent_{i}"
        open_agent.create_session(
            name=session_name, provider=OpenAgentProvider(name=name)
        )
    assert len(open_agent.state.sessions) == 5
    assert [session.name for session in open_agent.list_sessions()] == [
        f"session_{i}" for i in range(5)
    ]

def test_open_agent_can_create_provider_script(open_agent):
    open_agent.tool_create_provider_script(name="test")
    assert os.path.exists(os.path.join(open_agent.state.data_dir, "test.py"))
    os.remove(os.path.join(open_agent.state.data_dir, "test.py"))

