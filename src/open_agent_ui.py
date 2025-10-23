from datetime import datetime
import json
from typing import cast
from textual import events, work
from ollama import ChatResponse, chat
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalGroup, VerticalScroll
from textual.widget import Widget
from textual.widgets import (
    Footer, Header, Markdown, OptionList, RichLog, TextArea)

from open_agent import (
    OllamaProvider, SystemMessage, SystemState, SYSTEM_PROMPT, subtract_two_numbers_tool, available_functions)


class AgentResponseGroup(VerticalScroll, can_focus=False):
    def compose(self) -> ComposeResult:
        markdown = Markdown("")
        yield markdown


class UserPromptTextArea(TextArea):
    def on_key(self, event: events.Key) -> None:
        if event.character == "\n":
            user_message = self.text
            app = self.app
            app = cast(OpenAgentApp, app)
            self.disabled = True
            self.clear()
            self.query_llm(user_message)

    @work(thread=True)
    async def query_llm(self, user_message: str) -> None:
        markdown = self.app.query_one(Markdown)
        markdown = cast(Markdown, markdown)

        self.app.call_from_thread(
            markdown.append, f"\n\n**User:** {user_message}")

        app = self.app
        app = cast(OpenAgentApp, app)

        # TODO: This needs to be determined by the system
        app.system_state.messages.append(SystemMessage(role="user",
                                                       message=user_message,
                                                       fn=None,
                                                       create_at=datetime.now()))
        rich_log = app.query_one(RichLog)
        rich_log.clear()
        rich_log.write(app.system_state)
        provider = OllamaProvider()
        response = provider.chat(app.system_state.messages)
        app.system_state.messages.append(response)
        app.call_from_thread(
            markdown.append, f"\n\n**Assistant:** {response.message}")
        self.disabled = False
        self.focus()
        app.query_one(
            AgentResponseGroup).scroll_end(animate=False)


class UserPromptGroup(Widget):
    def compose(self) -> ComposeResult:
        yield UserPromptTextArea("",
                                 show_line_numbers=False,
                                 tab_behavior="indent",
                                 language="markdown")


class CommandPalletGroup(Widget):
    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList("Tools", "Something", "Other")


class OpenAgentApp(App):
    BINDINGS = [("ctrl+t", "toggle_command_pallet",
                 "Toggle the command pallet view")]
    CSS_PATH = "chat.tcss"
    system_state = SystemState(messages=[])
    system_state.messages.append(SystemMessage(role="system",
                                               message=SYSTEM_PROMPT,
                                               fn=None,
                                               create_at=datetime.now()))

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical():
                yield AgentResponseGroup(id="agent_response", can_focus=False)
                yield UserPromptGroup(id="user_prompt")
            yield RichLog(highlight=True, markup=True)
        yield Footer()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.text = event.text_area.text

    def action_toggle_command_pallet(self) -> None:
        self.query_one(CommandPalletGroup).toggle_class(
            "command_pallet_hidden")
