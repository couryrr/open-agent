from openagent import OpenAgent, OpenAgentProvider
import pytest


def test_open_agent_can_init():
    oa = OpenAgent()
    assert oa


def test_open_agent_can_add_provider():
    oa = OpenAgent()
    assert len(oa.providers) == 0
    provider = OpenAgentProvider(name="1")
    oa.add_provider(provider)
    assert len(oa.providers) == 1


def test_open_agent_can_add_multiple_providers():
    oa = OpenAgent()
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        oa.add_provider(provider)
    assert len(oa.providers.keys()) == 5


def test_open_agent_can_remove_provider():
    name = "1"
    oa = OpenAgent()
    provider = OpenAgentProvider(name=name)
    oa.add_provider(provider)
    assert len(oa.providers) == 1
    oa.remove_provider(name=name)
    assert len(oa.providers) == 0


def test_open_agent_removes_correct_provider():
    oa = OpenAgent()
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        oa.add_provider(provider)
    assert len(oa.providers) == 5
    oa.remove_provider(name="4")
    assert len(oa.providers.keys()) == 4
    assert [str(i) for i in range(4)] == [
        provider for provider in oa.providers.keys()]


def test_open_agent_removes_correct_providers():
    oa = OpenAgent()
    for i in range(5):
        provider = OpenAgentProvider(name=str(i))
        oa.add_provider(provider)
    assert len(oa.providers) == 5
    oa.remove_provider(name="4")
    oa.remove_provider(name="2")
    assert len(oa.providers) == 3
    assert ["0", "1", "3"] == [provider for provider in oa.providers.keys()]


def test_open_agent_can_add_model_to_provider():
    oa = OpenAgent()
    provider = OpenAgentProvider(name="1")
    oa.add_provider(provider)
    assert len(provider.models) == 0
    oa.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    oa.add_provider_model(name="1", model="some_llm_name")


def test_open_agent_can_add_multiple_models_to_provider():
    oa = OpenAgent()
    provider = OpenAgentProvider(name="1")
    oa.add_provider(provider)
    assert len(provider.models) == 0
    for i in range(5):
        oa.add_provider_model(name="1", model=f"some_llm_name_{i}")
    assert len(provider.models) == 5


def test_open_agent_cannt_add_model_to_non_existent_provider():
    oa = OpenAgent()
    provider = OpenAgentProvider(name="1")
    oa.add_provider(provider)
    assert len(provider.models) == 0
    with pytest.raises(Exception):
        oa.add_provider_model(name="2", model="some_llm_name")
    assert len(provider.models) == 0


def test_open_agent_can_remove_model_from_provider():
    open_agent = OpenAgent()
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    open_agent.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    open_agent.remove_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 0


def test_open_agent_can_remove_multiple_models_from_provider():
    open_agent = OpenAgent()
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


def test_open_agent_removes_correct_model_from_multiple_provider():
    open_agent = OpenAgent()
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


def test_open_agent_cant_remove_model_from_non_existent_provider():
    open_agent = OpenAgent()
    provider = OpenAgentProvider(name="1")
    open_agent.add_provider(provider)
    assert len(provider.models) == 0
    open_agent.add_provider_model(name="1", model="some_llm_name")
    assert len(provider.models) == 1
    with pytest.raises(Exception):
        open_agent.remove_provider_model(name="2", model="some_llm_name")
