from openagent import OpenAgent, OpenAgentMessage, OpenAgentProvider


def test_state_init_empty():
    openagent = OpenAgent()
    messages = openagent.get_messages()
    assert len(messages) == 0


def test_can_add_message_to_state():
    oa = OpenAgent()
    message = OpenAgentMessage()
    oa.add_message(message)
    assert len(oa.get_messages()) == 1


def test_provider_init_empty():
    oa = OpenAgent()
    assert len(oa.get_providers()) == 0

def test_can_add_provider():
    oa = OpenAgent()
    provider = OpenAgentProvider()
    oa.add_provider(provider)
    assert len(oa.get_providers()) == 1
