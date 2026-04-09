# Inventory Management System

A Flask-based REST API with CLI interface for managing product inventory.

## Setup
```bash
pipenv install
pipenv shell
python run.py
```

## CLI Example Usage

1. Run `python cli.py`
2. Select option 1 to view all inventory items
3. Select option 3 to manually add a new item
4. Select option 4 to search and add from OpenFoodFacts

## Route Inputs & Outputs

| Route | Input | Output |
|-------|-------|--------|
| GET /inventory | None | Array of all items |
| GET /inventory/<id> | URL param: id | Single item or 404 |
| POST /inventory | JSON body: product_name, brand... | Created item, 201 |
| PATCH /inventory/<id> | URL param: id, JSON: field/value | Updated item |
| DELETE /inventory/<id> | URL param: id | Success message |

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | /inventory | Get all items |
| GET | /inventory/<id> | Get specific item |
| POST | /inventory | Add item manually |
| POST | /inventory/fetch | Add item from OpenFoodFacts |
| PATCH | /inventory/<id> | Update item |
| DELETE | /inventory/<id> | Delete item |
| GET | /inventory/category/<category> | Get by category |
| GET | /inventory/low-stock | Get low stock items |
| GET | /inventory/expiring-soon | Get items expiring within 30 days |



## Running Tests
```bash
pytest tests/test_app.py -v
```
