import re, typer
from src.githubProvider import GitHubProvider
from src.aiClient import GroqAgent
from rich.table import Table
from rich.markdown import Markdown

class AuditEngine:
    """
    This class allows to run AI generated audits of Github files
    that checks for security risk and technical flaws. 
    """
    def __init__(self):
        self.github = GitHubProvider()
        self.ai = GroqAgent()
        self.scanner = SecretScanner() 

    def run_audit(self, repo_name: str, console, interactive: bool = False):
        files = self.github.get_repo_contents(repo_name)
        
        if not files:
            console.print("[yellow]⚠ No audit-eligible files found.[/yellow]")
            return

        for index, file in enumerate(files):
            # --- TOKEN SAVING ---
            if interactive:
                console.print(f"\n[bold white]Next File ({index + 1}/{len(files)}):[/bold white] [cyan]{file['path']}[/cyan]")
                
                # We use typer.prompt for multiple choices
                action = typer.prompt(
                    "Action? [s]can, s[k]ip, [q]uit", 
                    default="s"
                ).lower()

                if action == 'q':
                    console.print("[bold red]Audit aborted by user.[/bold red]")
                    break
                elif action == 'k':
                    console.print(f"[yellow]⏭️ Skipped {file['path']} .[/yellow]")
                    continue


            # Local Secret Scan
            
            findings = self.scanner.scan(file['path'], file['content'])
            
            if findings:
                console.print(f"[bold red] CRITICAL: Secret(s) Found![/bold red]")
                for f in findings:
                    console.print(f"   [red]![/red] {f['type']} on line {f['line']}")
                continue

            # Ai audit
            console.print(f"[bold blue] Sending to AI:[/bold blue] {file['path']}...")
            with console.status("[dim]Processing architectural review...[/dim]"):
                report = self.ai.analyze_code(file['content'])
                console.print(Markdown(report))
            
            console.print("[hr]")
            
        console.print(f"\n[bold green] Finished processing {repo_name}.[/bold green]")

class SecretScanner:
    def __init__(self):
        self.patterns = {
            "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
            "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
            "AWS Secret Access Key": r"aws_secret_access_key\s*=\s*['\"][a-zA-Z0-9/+=]{40}['\"]",
            "Google API Key": r"AIza[0-9A-Za-z\\-_]{35}",
            "Generic Secret/Password": r"(password|secret|passwd|api_key|token)\s*[:=]\s*['\"][a-zA-Z0-9!@#$%^&*()_+]{3,}['\"]",
            "Stripe API Key": r"sk_live_[0-9a-zA-Z]{24}",
        }

    def scan(self, file_path: str, content: str):
        """
        Scans file content for sensitive patterns.
        Returns a list of findings with line numbers.
        """
        findings = []
        lines = content.splitlines()

        for line_num, line in enumerate(lines, 1):
            for name, pattern in self.patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        "file": file_path,
                        "line": line_num,
                        "type": name,
                        "snippet": line.strip()[:50] + "..." # Truncate for safety
                    })
        return findings