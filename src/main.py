import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.secretScanner import AuditEngine

# Initialize Typer and Rich Console
app = typer.Typer(help="RepoSentinel: AI-Powered Repository Auditor")
console = Console()


@app.command()
def scan(
    repo: str = typer.Argument(..., help="The full name of the GitHub repo"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Ask for confirmation before scanning each file")
):
    console.print(Panel.fit(
        "[bold cyan]RepoSentinel CLI[/bold cyan]\n[viewing] Systems Engineering Audit Mode",
        border_style="green"
    ))

    engine = AuditEngine()
    
    try:
        # Pass the interactive flag to the engine
        engine.run_audit(repo, console=console, interactive=interactive)
    except Exception as e:
        console.print(f"[bold red]Critical Error:[/bold red] {e}")

if __name__ == "__main__":
    app()