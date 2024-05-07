from typing import Callable

import click
from textual.app import App, ComposeResult
from textual.widgets import Static

from ..handlers import Namespace, View
from ._interface import BuilderInterface


class TextualizeBuilder(BuilderInterface):
    no_input = False

    def _build(self) -> Callable:
        return self.__build_cli()

    def __build_cli(self) -> Callable:
        class TextualApp(App):
            def compose(self) -> ComposeResult:
                self.widget = Static('Textual')
                yield self.widget

            def on_mount(self) -> None:
                self.widget.styles.background = 'darkblue'
                self.widget.styles.border = ('heavy', 'white')

        app = TextualApp()

        return app.run

    def __build_namespace(self, namespace: Namespace, cli: click.Group):
        pass

    def __build_view(self, view: View, namespace_cli: click.Group):
        pass
