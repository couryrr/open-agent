from .app import OpenAgent as OpenAgent
from .app import OpenAgentContext as OpenAgentContext
from .app import OpenAgentProvider as OpenAgentProvider
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=['cli', 'tui'], default='cli', nargs='?')
    args = parser.parse_args()

    if args.mode == 'tui':
        pass
    else:
        agent = OpenAgent()
        agent.add_provider(OpenAgentProvider("1"))
        agent.add_provider_model(name="1", model="some_llm_name")
        print(agent.providers)
