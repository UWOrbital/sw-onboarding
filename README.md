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
    - add `Command` and `MainCommand` models from GS (including `BaseSQLModel`)
    - add database engine and dependency code from GS
    - add `DAL` from GS with only `Command` and `MainCommand` repositories
    - add existing routes for commands and main commands
    - add stubs for onboarders to implement
        - add route function stub for commands PATCH method
        - add model stub for `CommandHistory` audit table
            - indicate making migration with alembic (`alembic revision --autogenerate -m "<msg>"`)
        - add repository stub for audit model, wiring into `DAL`
        - add indicators to refactor existing commands routes to write to new audit model
        - add stub for `CORSMiddleware` binding function and `PydanticSettings` class for pulling CORS .env variables
            - add .env.example for CORS settings
        - add route function stub for command history GET method
    - write pytests for testing onboarder code
    - update `scripts/seed_onboarding_data.py` inject ~50 random commands into DB
- frontend
    - copy over table stubs from original GS onboarding
    - add stub for onboarder to write command history display
- add `OPTIONAL.md` detailing optional addition of authentication with keycloak (end-to-end functionality)
    - add keycloak container to docker compose (not started by `setup.sh`)
- update `README.md` with instructions (maybe hints)
- add `CLAUDE.md` describing read-only behavior + `.claude/settings.json`
- add pre-commit config YAML