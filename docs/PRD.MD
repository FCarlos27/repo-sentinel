# Project Requirements Document (PRD): RepoSentinel CLI

---

## 1. Project Overview

RepoSentinel CLI is a Python-based developer utility designed to provide automated repository auditing directly from the local terminal. The tool bridges the gap between manual code reviews and heavy enterprise-grade CI/CD security suites by offering a lightweight, localized way to assess repository health.

### 1.1 Problem Statement

Developers often lack immediate, local visibility into the "health" of their repositories before pushing to remote origins. Common issues include:

* **Security Risks:** Accidental inclusion of API keys, secrets, or credentials.
* **Technical Debt:** Accumulated "code smells" and unoptimized logic that pass basic linting but fail architectural standards.
* **Architectural Drift:** Inconsistencies in project structure across large codebases.

RepoSentinel provides a "Pre-Push" sanity check to ensure code meets security and quality standards before it enters the shared pipeline.

---

## 2. Target Audience

The tool is engineered for technical professionals focused on reliability and scale:

* **Backend Engineers:** Requiring deep analysis of logic and architectural consistency.
* **DevOps/SREs:** Aiming to enforce security best practices and reduce "secret leakage" incidents.
* **Systems Engineering Students:** Utilizing the tool for portfolio-grade project management and code quality assurance.

---

## 3. Functional Requirements

### 3.1 Repository Fetching

* **Authentication:** Must support GitHub Personal Access Tokens (PAT) via environment variables or a `.env` file.
* **Scoping:** Ability to fetch metadata and contents from both public and private repositories using `PyGithub`.
* **Selective Auditing:** Users must be able to target specific branches or directories rather than the entire repository.

### 3.2 AI-Driven Analysis

* **Contextual Auditing:** Utilize the Gemini or OpenAI API to perform static analysis on code snippets.
* **Pattern Recognition:** Identify technical debt (e.g., redundant logic, complex nesting) and suggest refactorings.
* **Architectural Review:** Evaluate if the repository follows standard patterns (e.g., MVC, Hexagonal) based on folder structure and imports.

### 3.3 Local Security Scanning

* **Secret Detection:** Implement regex-based and entropy-based scanning to find leaked keys (AWS, Stripe, Google Cloud) locally before data is sent to the AI API.
* **Vulnerability Database:** Cross-reference dependency files (e.g., `requirements.txt`) against known security advisories.

---

## 4. Non-Functional Requirements

### 4.1 Performance & Scalability

* **Latency:** AI analysis calls must be asynchronous to prevent the CLI from hanging during long-running tasks.
* **Rate Limiting:** The system must gracefully handle GitHub and AI API rate limits, implementing exponential backoff where necessary.

### 4.2 Security & Privacy

* **Token Handling:** No API keys or PATs shall be hardcoded; the application must strictly pull from the local environment.
* **Data Minimization:** Only relevant code snippets—stripped of PII—should be sent to the AI for analysis to maintain privacy.

### 4.3 Portability (Dockerization)

* **Environment Parity:** The tool must be packaged as a Docker image to ensure it runs identically on Linux, macOS, and Windows.
* **Minimal Footprint:** The Docker image should be optimized (e.g., using a Python-slim base) for fast pulls and execution.

---

## 5. System Architecture

The flow follows a deterministic, sequential path to ensure data integrity:

1. **Input Layer:** User executes a command via `Typer`/`Click` (e.g., `sentinel scan --repo "my-app"`).
2. **Data Acquisition:** `PyGithub` retrieves the targeted file tree and contents.
3. **Local Security Layer:** A local scan is performed for high-risk secrets. If a critical leak is found, the process halts immediately to prevent sending secrets to the AI API.
4. **AI Analysis Layer:** Sanitized code snippets are sent to the Gemini/OpenAI API.
5. **Reporting Layer:** The `Rich` library formats the findings into a high-visibility terminal dashboard, categorizing issues by "Critical," "Warning," and "Optimization."

---

## 6. Future Roadmap

* **V2 - Integration:** Develop a pre-commit hook installer (`sentinel init-hook`) to automate scans during the `git commit` workflow.
* **V3 - Multi-Provider Support:** Expand the `PyGithub` abstraction layer to include GitLab and Bitbucket APIs.
* **V4 - Custom Rule Engines:** Allow users to define project-specific architectural rules via a `sentinel.yaml` configuration file.

---

