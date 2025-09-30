# Endorsements MCP Server

This MCP server manages endorsements for the travel agent, allowing users to add their names to a list of people who endorse this agent and retrieve the list of endorsements.

## Features

- Add endorsements with user name and optional comment
- Retrieve all endorsements
- Get endorsement statistics
- Persistent storage in text files

## Usage

To run the server:
```bash
uv run main.py
```

The server will be available at `http://localhost:8004` by default.

## API Endpoints

- `add_endorsement(name: str, comment: str = "")` - Add a new endorsement
- `get_endorsements()` - Get all endorsements 
- `get_endorsement_stats()` - Get endorsement statistics
- `remove_endorsement(name: str)` - Remove an endorsement by name

## Data Storage

Endorsements are stored in `endorsements.txt` in the server directory, with each endorsement on a separate line in the format:
```
timestamp|name|comment
```