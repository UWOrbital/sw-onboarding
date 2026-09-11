# sw-onboarding
The mandatory onboarding challenge for all UW Orbital software developers

Backend on :3001
Frontend on :5175

## DEV: TASK LIST

> Update this task list when tasks are finished/foregone/updated/added

- .github
    - add workflow for frontend testing
    - add workflow for frontend linting and formatting
- backend
    - write pytests for testing onboarder code
        - tests for CORS middleware
        - tests for command update endpoint
        - tests for CommandHistory model implementation
        - tests for CommandHistoryRepository concrete method
        - tests for command history get endpoint
        - tests for command history wiring in existing command endpoints
- frontend
    - copy over table stubs from original GS onboarding
    - add stub for onboarder to write command history display
- update `README.md` with instructions (maybe hints)
- add `CLAUDE.md` describing read-only behavior + `.claude/settings.json`
