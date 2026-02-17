from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from langchain_core.callbacks import BaseCallbackHandler


# Initialize console with force_terminal=True to ensure color output
# even in non-TTY environments like PyCharm's Python Console.
console = Console(force_terminal=True)

class RichAgentCallbackHandler(BaseCallbackHandler):
    """Custom callback handler to display agent steps in a rich table/box."""
    def __init__(self, bconsole: Console):
        self.console = bconsole

    def on_agent_action(self, action, **kwargs):
        """Displays agent tool calls."""
        # Print a clear divider or spacing if needed
        self.console.print("\n[bold]→ Agent is taking an action...[/bold]")
        self.console.print(
            Panel(
                f"[bold yellow]Tool:[/bold yellow] {action.tool}\n"
                f"[bold yellow]Input:[/bold yellow] {action.tool_input}",
                title="Agent Action",
                border_style="yellow",
                expand=False
            )
        )

    def on_tool_end(self, output, **kwargs):
        """Displays tool outputs."""
        self.console.print(
            Panel(
                str(output),
                title="Tool Output",
                border_style="magenta",
                expand=False
            )
        )

def display_agent_output(raw_response):
    """Displays the raw agent response in a pretty panel."""
    console.print(
        Panel(
            Pretty(raw_response),
            title="Agent Output",
            border_style="green"
        )
    )

def display_structured_response(structured_response):
    """Displays the structured research response in a rich panel."""
    console.print(
        Panel(
            f"[bold blue]Topic:[/bold blue] {structured_response.topic}\n\n"
            f"[bold blue]Summary:[/bold blue] {structured_response.summary}\n\n"
            f"[bold blue]Sources:[/bold blue] {', '.join(structured_response.sources)}\n\n"
            f"[bold blue]Tools Used:[/bold blue] {', '.join(structured_response.tools_used)}",
            title="Structured Research Response",
            border_style="cyan"
        )
    )

def display_error(message, raw_response=None):
    """Displays an error message and optional raw response."""
    console.print(f"[bold red]Error during research:[/bold red] {message}")
    if raw_response:
        console.print(Panel(str(raw_response), title="Raw Response", border_style="red"))

def get_status(message: str):
    """Returns a status context manager."""
    return console.status(message, spinner="dots")

def get_callback_handler():
    """Returns the custom callback handler."""
    return RichAgentCallbackHandler(console)

def get_user_input(prompt_text: str, default_value: str = "") -> str:
    """Prompts the user for input with an optional default value."""
    prompt_str = f"[bold green]{prompt_text}[/bold green]"
    if default_value:
        prompt_str += f" [dim]({default_value})[/dim]"
    prompt_str += ": "
    
    user_input = console.input(prompt_str).strip()
    return user_input if user_input else default_value
