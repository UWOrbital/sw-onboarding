# sw-onboarding
This repo contains the mandatory onboarding challenge for all UW Orbital software developers.

**Read this README thoroughly before beginning the challenge**. It contains the requirements, setup instructions, and implementation details you will need to complete it.

The goal of this onboarding challenge is to implement an audit log for commands sent through the ground station. The audit log should record each change to a command, allowing its lifecycle to be tracked and reconstructed after the fact.

This challenge will teach you the skills needed for full-stack development on our design team. It's designed to be similar to the type of work you'd do on the team (and co-op) and will give you a deeper understanding of web development.

This onboarding challenge may be harder than that of other design teams. We expect members to struggle at various points of this challenge. Don't be afraid to ask questions about the onboarding process in the #sw-onboarding channel on Discord. It's very important to us that you're able to ask questions when you don't understand something.

Once you complete this challenge, you'll be ready to join the Software team.

## Installation
1. Ensure you are running on WSL (for Windows), Linux, or Mac.
2. Clone this repo into a working directory `./sw-onboarding`.
3. Run the setup script with `./setup.sh`. The script will install dependencies, start PostgreSQL, apply database migrations, seed the database, and verify that the backend starts successfully.

## AI usage
AI is becoming increasingly prevalent in software development. You are free to use AI tools to help complete this challenge, but try to avoid relying too heavily on it (i.e. using AI to write solutions that you do not understand). The purpose of this challenge is to provide you with some fundamental development knowledge and skills, which may be missed if you submit an AI solution without learning from it.
You are responsible for understanding the code you submit and you should be able to explain your implementation.

## Requirements
We don't expect members to be experts in software development before getting involved. However, this challenge assumes some basic programming knowledge and introduces several technologies used by the Software team.
If you've never coded before in any language, there will be a learning curve.

### Python/TypeScript
If you're unfamiliar with Python or TypeScript, there are many great resources online to begin programming in these languages.

### Git/GitHub
If you're not familiar with Git version control, there are plenty of online resources to learn from. Git is an essential tool for many software developers. You only need to know the basics for now, since you can learn more about Git as you work on tasks. There are also GUI applications available for Git that don't require you to use the command line.

### FastAPI
FastAPI is a web framework for building APIs in Python. Our backend is written using FastAPI, so make sure you are familiar with its syntax and conventions. The FastAPI docs are a great resource: https://fastapi.tiangolo.com/

### React
React is a JavaScript library for building user interfaces using components. Our frontend is written using React, so make sure you are familiar with its best practices and core features. The React docs are fantastic: https://react.dev/

### PostgreSQL
Postgres is the relational database system we use for our ground station. If you've never worked with a database before, this is a great opportunity to learn with a relatively simple schema. Most of the behaviour is abstracted away by SQLModel.

## Challenge description

The UW Orbital mission control centre (part of the ground station) is a web application that allows operators to send commands to a satellite. Each command has a lifecycle: it is created, sent, and may transition through several states before it reaches its final state.

Currently, there is no way to view the history of a command after its state changes. Your task is to implement an audit log that records the history of every command.

The audit log should create a new entry whenever a command is created, updated, or deleted. Each entry should contain the command's state at the time the entry was created, including its status, parameters, and timestamp.

The completed feature should allow a user to:
1. Select a command and view its audit log from the frontend.
2. See the historical state of a command, including its status, parameters, and timestamp.
3. Preserve historical entries even if the original command is later updated or deleted.
4. Retrieve command history through a backend API endpoint.
5. Store command history persistently in PostgreSQL.

**Search the entire repo for `TODO` (you can do this with an IDE or with `grep`)**. This will locate the code that is missing. You must finish the implementation of all stubs to complete this challenge. You will need to work across both the backend and frontend.

### Backend
The backend portion requires you to:

1. **Implement the `CommandHistory` database model** (`backend/app/database/models.py`), then create the necessary database migration with Alembic (see the model's docstring for the command).
2. **Implement the `CommandHistoryRepository`** (`backend/app/database/repositories.py`).
3. **Implement the command history endpoint** (`backend/app/api/routes/command_history.py`).
4. **Complete the command update endpoint** (`backend/app/api/routes/commands.py`).
5. **Record history when commands are created, updated, or deleted** by wiring `CommandHistory` appending into the create, update, and delete routes (`backend/app/api/routes/commands.py`).
6. **Configure CORS** so that the frontend can communicate with the backend during local development (`backend/app/config/env_settings/cors_config.py`).

### Frontend
The frontend portion requires you to:

7. **Define the `CommandHistory` type** (`frontend/src/utils/types.ts`).
8. **Implement the command history API hook** using React Query (`frontend/src/hooks/useCommandHistory.ts`).
9. **Build the command history page** (`frontend/src/pages/CommandHistoryPage.tsx`):
   - Define the table columns and display the relevant information for each history entry in the provided Table component.
   - Include a way for the user to select which command's audit log they want to view.
   - Handle loading and error states appropriately.

During development, the backend should run on port `8001` and the frontend on port `5175`.

You are expected to explore the existing codebase and understand how the existing command functionality works before implementing the feature. There may be parts of the codebase that are unfamiliar to you, which is okay!

Good luck on the onboarding challenge!
