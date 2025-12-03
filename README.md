# Azure Functions V2 Python Blueprint Project

This project demonstrates an Azure Functions V2 Python app using the Blueprint pattern for modularity and maintainability.

## Structure
- `main.py`: Entry point, registers blueprints
- `blueprints/`: Contains modular function blueprints
- `requirements.txt`: Python dependencies
- `host.json`: Azure Functions runtime config
- `local.settings.json`: Local development settings

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `func start`

## Sample Function
- HTTP-triggered function at `/api/HttpExample` responds with a greeting.

## Cursor-Based Pagination Usage

### Endpoint: List Templates

**POST** `/api/pdc-template` (with body)

Request body:
```
{
	"cursor": 0,   // (optional) template_id to start after
	"limit": 10     // (optional) number of records to return
}
```

Response:
```
{
	"results": [ ...template objects... ],
	"next_cursor": <template_id or null>
}
```

To get the next page, send the previous `next_cursor` as the new `cursor` value.

### General Usage for Other Entities

Use the utility in `utils/pagination.py`:

```
from utils.pagination import paginate_query

with get_session() as session:
		results, next_cursor = paginate_query(session, Model, cursor_field='id', cursor=0, limit=10)
```

Replace `Model` and `cursor_field` as needed for your entity.
