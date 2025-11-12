from openagent import OpenAgentProvider


def test_can_add_model():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    provider.add_model("some_llm_name")
    assert len(provider.models) == 1


def test_cannot_add_same_model():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    provider.add_model("some_llm_name")
    provider.add_model("some_llm_name")
    assert len(provider.models) == 1


def test_can_add_multiple_models():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    for i in range(5):
        provider.add_model(f"some_llm_name_{i}")
    assert len(provider.models) == 5


def test_can_remove_model():
    provider = OpenAgentProvider(name="1")
    assert len(provider.models) == 0
    provider.add_model("some_llm_name")
    assert len(provider.models) == 1
    provider.remove_model("some_llm_name")
    assert len(provider.models) == 0


def test_can_remove_multiple_models():
    # TODO: Find a better way to test set equality
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    for i in range(5):
        provider.add_model(f"some_llm_name_{i}")
    assert len(provider.models) == 5
    provider.remove_model("some_llm_name_0")
    assert len(provider.models) == 4
    expected = set([f"some_llm_name_{i}" for i in range(1, 5)])
    assert provider.models == expected


def test_can_remove_non_existent_model():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    provider.add_model("some_llm_name")
    assert len(provider.models) == 1
    provider.remove_model("some_llm_name_1")
    assert len(provider.models) == 1


def test_can_delete_all_models():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    for i in range(5):
        provider.add_model(f"some_llm_name_{i}")
    assert len(provider.models) == 5
    provider.remove_model("some_llm_name_0")
    assert len(provider.models) == 4
    provider.remove_model("some_llm_name_1")
    assert len(provider.models) == 3
    provider.remove_model("some_llm_name_2")
    assert len(provider.models) == 2
    provider.remove_model("some_llm_name_3")
    assert len(provider.models) == 1
    provider.remove_model("some_llm_name_4")
    assert len(provider.models) == 0


def test_can_remove_on_empty_model():
    provider = OpenAgentProvider(name="provider_1")
    assert len(provider.models) == 0
    provider.remove_model("some_llm_name")
    assert len(provider.models) == 0
