from openagent.app import OpenAgent, OpenAgentProvider


def test_can_create_session_without_name():
    oa = OpenAgent()
    assert len(oa.state.sessions.items()) == 0
    provider = OpenAgentProvider(name="provider_1")
    oa.create_session(provider=provider)
    assert len(oa.state.sessions.items()) == 1
    assert oa.state.sessions.get("something strange")


def test_can_create_session_with_name():
    oa = OpenAgent()
    assert len(oa.state.sessions.items()) == 0
    provider = OpenAgentProvider(name="provider_1")
    oa.create_session(provider=provider, name="test")
    assert len(oa.state.sessions.items()) == 1
    assert oa.state.sessions.get("test")


def test_can_list_sessions():
    oa = OpenAgent()
    assert len(oa.state.sessions.items()) == 0

    provider = OpenAgentProvider(name="provider_1")
    oa.add_provider(provider)

    provider = OpenAgentProvider(name="provider_2")
    oa.add_provider(provider)

    oa.create_session(provider=provider, name="test")
    oa.create_session(provider=provider, name="test_2")
    oa.create_session(provider=provider, name="test_3")

    assert len(oa.list_sessions()) == 3
    assert oa.list_sessions()[0].name == "test"
    assert oa.list_sessions()[1].name == "test_2"
    assert oa.list_sessions()[2].name == "test_3"
