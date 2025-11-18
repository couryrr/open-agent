import argparse
import json
import os

from platformdirs import user_data_dir

from .app import OpenAgent as OpenAgent
from .context import OpenAgentContext as OpenAgentContext
from .provider import OpenAgentProvider as OpenAgentProvider
from .session import OpenAgentSession as OpenAgentSession


def main():
    appname = "openagent"
    appauthor = "nextbubble"
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-session", help="create a new session")
    parser.add_argument(
        "--list-sessions", action="store_true", help="list all sessions"
    )
    parser.add_argument(
        "--attach-session", action="store_true", help="attach to a session"
    )
    parser.add_argument("--add-provider", action="store_true", help="add a provider")
    parser.add_argument(
        "--create-provider-script",
        help="create a script for a provider",
    )
    parser.add_argument(
        "--list-providers", action="store_true", help="list all providers"
    )
    parser.add_argument("--remove-provider", help="remove a provider")
    parser.add_argument(
        "--add-provider-model", action="store_true", help="add a model to a provider"
    )
    parser.add_argument(
        "--remove-provider-model",
        action="store_true",
        help="remove a model from a provider",
    )

    data_dir = user_data_dir(appname, appauthor)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, "data.json"), "w") as file:
            file.write("{}")

    with open(os.path.join(data_dir, "data.json"), "r") as file:
        args = parser.parse_args()
        agent = OpenAgent.model_validate(json.load(file))
        # FIXME: Not sure if this should be set
        agent.state.data_dir = data_dir

        if args.create_session:
            agent.create_session(
                OpenAgentProvider(name="ollama"), name=f"{args.create_session}"
            )

        if args.add_provider:
            name = input("Enter provider name: ")
            url = input("Enter provider url: ")
            port = input("Enter provider port: ")
            # auth = input("Enter provider auth: ")
            agent.add_provider(OpenAgentProvider(name=name, url=url, port=port))

        if args.remove_provider:
            agent.remove_provider(args.remove_provider)

        agent.save()

        if args.create_provider_script:
            agent.tool_create_provider_script(args.create_provider_script)
        if args.list_providers:
            [print(provider.name) for provider in agent.list_providers()]
        if args.list_sessions:
            [print(session.name) for session in agent.list_sessions()]
