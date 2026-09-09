# sw-onboarding
The mandatory onboarding challenge for all UW Orbital software developers

Backend on :3001
Frontend on :5175

## DEV: TASK LIST

> Update this task list when tasks are finished/foregone/updated/added

- .github
    - add workflow for pytests
    - add workflow for mypy
    - add workflow for frontend testing
    - add workflow for pre-commit, frontend linting and formatting
- backend
    - add stubs for onboarders to implement
        - add indicators to refactor existing commands routes to write to new audit model
        - add schema stubs for route stubs
    - write pytests for testing onboarder code
    - update `scripts/seed_onboarding_data.py` inject ~50 random commands into DB
- frontend
    - copy over table stubs from original GS onboarding
    - add stub for onboarder to write command history display
- add `OPTIONAL.md` detailing optional addition of authentication with keycloak (end-to-end functionality)
    - add keycloak container to docker compose (not started by `setup.sh`)
- update `README.md` with instructions (maybe hints)
- add `CLAUDE.md` describing read-only behavior + `.claude/settings.json`
