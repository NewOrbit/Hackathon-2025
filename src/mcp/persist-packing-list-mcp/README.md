# Persist Packing List MCP Server

A Model Context Protocol (MCP) server for persisting and managing travel packing lists with full CRUD operations and status tracking. Uses markdown file storage for human-readable persistence.

## Features

📋 **Packing List Management**
- Create, read, update, delete packing lists
- Set travel dates and destinations
- Track packing completion progress
- Organize lists by trip or purpose

✅ **Item Management**
- Add items with categories and priorities
- Mark items as packed, unpacked, or optional
- Set quantities and add notes
- Delete unwanted items

📊 **Progress Tracking**
- Visual completion percentage
- Packed vs unpacked item counts
- Priority-based organization
- Category grouping

🗂️ **Categories Supported**
- Clothing
- Electronics
- Toiletries
- Documents
- Medications
- Entertainment
- Food & Snacks
- Sports & Outdoor
- Miscellaneous

## Installation

```bash
## cd to persist-packing-list-mcp project
cd src/mcp/persist-packing-list-mcp
```

```bash
# Install dependencies
uv sync
```

### Running the Server

```bash
uv run mcp dev main.py
```

```bash
# use this when wanting to consume within an agent
uv run main.py
```

## Storage

The server uses a single markdown file for data persistence. The file is stored at:
- `~/.packing_lists/persist-packing-list.md` (default)
- Directory can be overridden with the `PACKING_LIST_DB_PATH` environment variable

All data is stored in human-readable markdown format with embedded metadata for parsing. No database or JSON files are used.

## Available Tools

### Packing List Operations

- **`create_packing_list`** - Create a new packing list
- **`get_packing_list`** - Get a packing list by ID with all items
- **`list_all_packing_lists`** - Get all packing lists with summary info
- **`update_packing_list`** - Update packing list metadata
- **`delete_packing_list`** - Delete a packing list and all items

### Item Operations

- **`add_item_to_list`** - Add an item to a packing list
- **`update_item_status`** - Mark items as packed/unpacked
- **`delete_item`** - Remove an item from a list
- **`export_to_markdown`** - Manually trigger markdown export (refresh the file)

### Resources

- **`packing-list://list/{list_id}`** - Get formatted packing list content

## Usage Examples

### Create a Packing List

```python
create_packing_list(
    name="European Vacation",
    description="2 week trip across Europe",
    destination="Europe",
    travel_start_date="2025-10-01",
    travel_end_date="2025-10-15"
)
```

### Add Items

```python
add_item_to_list(
    list_id=1,
    name="Passport",
    category="documents",
    priority=5,
    notes="Check expiration date"
)

add_item_to_list(
    list_id=1,
    name="T-shirts",
    category="clothing",
    quantity=7,
    priority=3
)
```

### Track Progress

```python
# Mark items as packed
update_item_status(item_id=1, status="packed")
update_item_status(item_id=2, status="packed")

# View completion
get_packing_list(list_id=1)
# Returns completion percentage and packed counts
```

## Configuration

Environment variables:
- `PACKING_LIST_DB_PATH` - Custom storage directory path
- Server runs on port 8009 by default

All changes are immediately persisted to the markdown file. The file format includes embedded HTML comments with IDs for parsing and maintaining data consistency.

## Data Models

### Packing List
- ID, name, description
- Destination and travel dates
- Creation/update timestamps
- Associated items

### Packing Item
- ID, name, category
- Quantity and priority (1-5 scale)
- Status: not_packed, packed, optional
- Notes and timestamps

## Categories

Items can be organized into these categories:
- **clothing** - Shirts, pants, shoes, etc.
- **electronics** - Phone, chargers, adapters
- **toiletries** - Toothbrush, shampoo, etc.
- **documents** - Passport, tickets, insurance
- **medications** - Prescriptions, first aid
- **entertainment** - Books, games, headphones
- **food_snacks** - Travel snacks, water
- **sports_outdoor** - Hiking gear, swimwear
- **miscellaneous** - Everything else

## Status Types

Items can have these statuses:
- **not_packed** - Item needs to be packed
- **packed** - Item is packed and ready
- **optional** - Item is nice-to-have but not essential

Optional items don't count toward completion percentage.