## MEM_AGENT Comprehensive Error Audit

Generated: current session

### Scope
- Local development and Dockerized stack (`mem-agent-api`, `n8n`, `mautic`, databases, Redis)
- Git/GitHub repository setup and push
- Cloudflare Tunnel temporary access
- Streamlit dashboard deployment readiness

---

### Critical Incidents (Chronological)

1) Docker compose invocation from wrong directory / inline comment executed
- Symptom: `no configuration file provided: not found` and `Access : The term 'Access' is not recognized`
- Root cause: Command run outside project root and a comment appended to command in PowerShell
- Resolution:
  - `cd E:\MEM_AGENT`
  - Run only: `docker compose up -d`

2) Unset env vars and obsolete compose version key
- Symptom: Compose warnings for `MAUTIC_DB_NAME`, `GCP_PROJECT_ID`, `SUPABASE_URL`, etc.; deprecated `version` in `docker-compose.yml`
- Root cause: `.env` missing required variables; outdated schema
- Resolution:
  - Created `.env` from templates and populated placeholders
  - Removed obsolete `version` key in `docker-compose.yml`

3) API container restart: ASGI app import failure
- Symptom: `Error loading ASGI app. Could not import module 'main'`
- Root cause: Missing `main.py` in project root for FastAPI entrypoint
- Resolution: Added `main.py` implementing `/health`, `/stats`, `/mentor/chat`, etc.; restarted service

4) PowerShell pipe misuse
- Symptom: `docker compose ps | cat` → `The input object cannot be bound...`
- Root cause: `cat` in PowerShell expects files, not pipeline
- Resolution: Use `docker compose ps` directly

5) Mautic URI typo in health probe
- Symptom: `Cannot convert value "http://localhost::8888" to type System.Uri`
- Root cause: Double colon in URL
- Resolution: Corrected to `http://localhost:8888`

6) Mautic DB connection errors; n8n DB init error
- Symptom (Mautic): `mysqladmin: connect to server at 'mautic-db' failed`, `Access denied for user 'mPixC'`
- Symptom (n8n): `There was an error initializing DB`
- Root cause: Invalid or mismatched DB creds and corrupted volumes
- Resolution:
  - `docker compose down`
  - `docker volume rm mem_agent_postgres_data mem_agent_mautic_db_data`
  - Regenerated strong passwords and updated `.env` (`POSTGRES_PASSWORD`, `N8N_DB_PASSWORD`, `MAUTIC_DB_USER`, `MAUTIC_DB_PASSWORD`, `JWT_SECRET_KEY`, `ENCRYPTION_KEY`, `SESSION_SECRET`)
  - `docker compose up -d`

7) Apache ServerName warning in Mautic
- Symptom: `AH00558: Could not reliably determine the server's fully qualified domain name`
- Root cause: No `ServerName` configured in Apache
- Resolution: Added `config/apache-server-name.conf` with `ServerName localhost` and mounted into container

8) Cloudflare Tunnel logging/URL detection issues
- Symptom: PowerShell errors about `RedirectStandardOutput` and invalid paths; inability to detect URLs
- Root cause: Incorrect `Start-Process` redirection; missing `--logfile` usage
- Resolution: Updated `hosted-access.ps1` to use `--logfile` with valid paths and no conflicting redirections

9) Streamlit Cloud form errors (repo/branch/main file path)
- Symptom: `Repository: This field is required`, `Branch: This branch does not exist`, `Main file path: This file does not exist`
- Root cause: Code not yet pushed to GitHub; invalid form entries
- Resolution: Create repo, push code, set `Repository`, `Branch=main`, `Main file path=dashboard/app.py`

10) Git push rejection and merge conflict
- Symptom: `! [rejected] main -> main (fetch first)`; `CONFLICT (add/add): Merge conflict in README.md`
- Root cause: Remote had changes not present locally
- Resolution:
  - `git pull --rebase origin main`
  - Resolve `README.md` conflict
  - Commit and push

11) Current session: Docker engine not initially running
- Symptom: `error during connect: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`
- Root cause: Docker Desktop not started
- Resolution: Launched Docker Desktop; proceed to `docker compose ps`/`up -d` afterwards

12) Linter and syntax errors in `enhanced_memory_agent_ui.py`
- Symptom: Multiple errors: `Try statement must have at least one except`, `Expected expression`, `Unexpected indentation`
- Root cause: Mis-indented `except`, mis-indented Streamlit UI blocks and stray indent
- Resolution: Fixed try/except alignment; corrected `Session Controls` block and `st.rerun()` indentation; re-ran lints → no errors

13) GitHub push large file warning (latest)
- Symptom: `remote: warning: GH001: Large files detected. You may want to try Git LFS`
- Root cause: One or more files over GitHub’s recommended size threshold
- Impact: Push succeeded, but repository contains large files. May affect clone speed; files over 100MB will be blocked.
- Recommended Action:
  - Audit repo for large artifacts: `git lfs track "*.bin" "*.pdf" "*.log"` (example)
  - Move logs or generated artifacts out of VCS; add to `.gitignore`
  - If >100MB files exist in history, rewrite with `git filter-repo` or `git filter-branch`

---

### Current Status Snapshots
- Git: on `main`; latest commit includes UI syntax fixes and merge conflict resolution; push successful
- Docker: Installed; ensure Docker Desktop is running before stack operations
- Lints: `enhanced_memory_agent_ui.py` now clean
- Streamlit: Ready to deploy with repo `luxurioupotato/mem-agent`, branch `main`, main file `dashboard/app.py`

---

### Repro/Verification Commands
- Docker engine check: `docker info`
- Stack status: `docker compose ps`
- API health (local): `Invoke-WebRequest http://localhost:8000/health -UseBasicParsing`
- n8n UI: `http://localhost:5678`
- Mautic UI: `http://localhost:8888`
- Git status: `git status && git log --oneline -5`

---

### Preventive Hardening
- Keep `.env` authoritative and avoid committing secrets
- Add `logs/` and generated artifacts to `.gitignore`
- Manage oversized assets via Git LFS or external storage
- For Cloudflare Tunnels, install as a service for persistent URLs
- Back up volumes before destructive operations

---

### Open Follow-ups
- Audit and optionally migrate large files to LFS; update `.gitattributes`
- Start Docker and verify services with `docker compose ps` and health endpoints
- Complete Streamlit Cloud deployment; set `API_BASE_URL` secret


