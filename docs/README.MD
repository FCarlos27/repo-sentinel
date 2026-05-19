**RepoSentinel** is a high-performance, containerized CLI utility designed to audit GitHub repositories for architectural debt, security vulnerabilities, and local secret leaks.

By implementing a **Zero-Trust local gatekeeper** alongside **cloud-based intelligence**, RepoSentinel analyzes source code efficiently while aggressively optimizing for API token consumption.

---

## Core Architecture & Features

* **Multi-Layered Security (Fail-Fast Logic):** Features a localized `SecretScanner` that runs high-speed regex checks for exposed credentials (AWS, GitHub, Stripe, etc.) before any code leaves the machine. If a leak is found, cloud operations are aborted instantly.
* **Selective Auditing (Token-Saving Gatekeeper):** Automatically skips large dependency structures (`node_modules`, `venv`, `__pycache__`) and evaluates only whitelisted source extensions (`.py`, `.js`, `.ts`, `.go`, etc.).
* **Interactive Controls:** Prompts the user with discrete actions—`[s]can`, `s[k]ip`, or `[q]uit`—for each eligible file to prevent terminal flooding and manage API query quotas intentionally.
* **Polished Terminal UI:** Leverages `Rich` and `Typer` to render structured dashboards, markdown reports, status spinners, and real-time scanning progress natively inside the shell.
* **Deterministic Deployment:** Fully Dockerized using an optimized multi-layer `python:3.12-slim` setup that keeps the production image footprint under 200MB.

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root directory:

```env
GITHUB_PAT=your_github_personal_access_token
GROQ_API_KEY=your_groq_api_key

```

---

## Getting Started (Local Development)

### Prerequisites

* Python 3.12+
* A configured virtual environment (`venv`)

### Installation & Execution

1. Install dependencies:
```bash
pip install --only-binary :all: aiohttp PyGithub
pip install -r requirements.txt

```

2. Expose the source tree to your Python path and run the tool in **Interactive Mode**:

```powershell
   # Windows PowerShell
   $env:PYTHONPATH = "src"
   python -m reposentinel.main scan "owner/repository-name" --interactive

```

*(Omit the `--interactive` or `-i` flag to run an automated, unattended scan).*

---

## Docker Deployment

### 1. Build the Optimized Image

```bash
docker build -t repo-sentinel .

```

### 2. Execute the Secure Container

Pass your local environment variables into the container dynamically:

```bash
docker run -it --env-file .env repo-sentinel scan "owner/repository-name" -i

```

---

##  Security & Systems Design Highlights

### Separation of Concerns (SoC)

The AI agent operates as a decoupled, isolated service provider. It contains zero knowledge about file trees, terminal interfaces, or user flow choices. The orchestration logic resides entirely within the `AuditEngine`.

### Microsecond Fail-Fast Execution

Cloud LLM processing introduces network latency and structural costs. RepoSentinel mitigates this by running pattern-matching sweeps locally. 
