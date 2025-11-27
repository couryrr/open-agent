import argparse
import json
import os

from platformdirs import user_data_dir

from .app import OpenRunner as OpenRunner
from .context import OpenRunnerContext as OpenRunnerContext
from .provider import OpenRunnerProvider as OpenRunnerProvider
from .session import OpenRunnerSession as OpenRunnerSession


def main():
    appname = "openrunner"
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
    parser.add_argument("--smoke-test-provider", help="smoke test a provider")
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

    #TODO: Load config from file
    #TODO: Set config file or use default
    data_dir = user_data_dir(appname, appauthor)
    runner = OpenRunner()
    runner.state.load_config()

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, "data.json"), "w") as file:
            file.write("{}")

    with open(os.path.join(data_dir, "data.json"), "r") as file:
        args = parser.parse_args()
        agent = OpenRunner.model_validate(json.load(file))
        if args.create_session:
            agent.create_session(
                OpenRunnerProvider(name="ollama"), name=f"{args.create_session}"
            )

        if args.add_provider:
            name = input("Enter provider name: ")
            url = input("Enter provider url: ")
            port = input("Enter provider port: ")
            # auth = input("Enter provider auth: ")
            agent.add_provider(OpenRunnerProvider(name=name, url=url, port=port))

        if args.remove_provider:
            agent.remove_provider(args.remove_provider)

        agent.save()

        if args.create_provider_script:
            agent.tool_create_provider_script(args.create_provider_script)
        if args.list_providers:
            [print(provider.name) for provider in agent.list_providers()]
        if args.list_sessions:
            [print(session.name) for session in agent.list_sessions()]
        if args.smoke_test_provider:
            agent.tool_smoke_test_provider(args.smoke_test_provider)
