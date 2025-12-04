
# Dynamic Attribute Management

## Overview
Both templates and classes support up to 35 dynamic attributes. These attributes are stored in the database as columns named `attribute_1` through `attribute_35`.

## Templates
- When creating or updating a template, you can provide any subset of attributes using a dictionary in the request body:
  ```json
  {
    "name": "Test Template",
    "attributes": {
      "attribute_1": "A1",
      "attribute_2": "A2",
      "attribute_5": "A5"
    },
    "created_by": "tester",
    "is_active": true
  }
  ```
- Only the provided attributes will be set or updated; others remain unchanged or null.
- The response will include all attributes, with keys as `attribute_1`, `attribute_2`, etc.

## Classes
- When creating or updating a class, you provide attribute values using template-defined names (e.g., `C1`, `C2`, ...):
  ```json
  {
    "template_id": 1,
    "name": "Class Name",
    "attributes": {
      "C1": "Hari",
      "C3": "Baskar"
    },
    "created_by": "tester",
    "is_active": true
  }
  ```
- The system maps these names to the correct database columns (`attribute_1`, `attribute_2`, ...), based on the template definition.
- The response will show attribute values using the template-defined names as keys:
  ```json
  {
    "class_id": 1,
    "template_id": 1,
    "name": "Class Name",
    "attributes": {
      "C1": "Hari",
      "C2": null,
      "C3": "Baskar",
      ...
    },
    ...
  }
  ```

## Attribute Mapping Logic
- For templates: request and response keys are `attribute_1` ... `attribute_35`.
- For classes: request keys are template-defined names (e.g., `C1`, `C2`), mapped to the correct columns; response keys are also template-defined names.
- This allows partial updates and flexible data entry for both templates and classes.


# Template Field Endpoints

## Create Template Field
**POST** `/api/pdc-template-field/create`

**Request Body:**
```
{
  "template_id": 1,
  "metadata_key": "C1",
  "display_name": "First Name",
  "data_type": "string",
  "is_required": true,
  "default_value": "",
  "validation_rule": "^[A-Za-z]+$",
  "sort_order": 1,
  "is_active": true,
  "created_by": "tester"
}
```

**Response:**
```
{
  "template_field_id": 1,
  "template_id": 1,
  "metadata_key": "C1",
  "display_name": "First Name",
  "data_type": "string",
  "is_required": true,
  "default_value": "",
  "validation_rule": "^[A-Za-z]+$",
  "sort_order": 1,
  "is_active": true,
  "created_at": "2025-12-03T00:00:00",
  "created_by": "tester",
  "modified_at": null,
  "modified_by": null
}
```

---

## Get Template Field
**GET** `/api/pdc-template-field/get?template_field_id=1`

**Response:**
```
{
  "template_field_id": 1,
  "template_id": 1,
  "metadata_key": "C1",
  "display_name": "First Name",
  "data_type": "string",
  "is_required": true,
  "default_value": "",
  "validation_rule": "^[A-Za-z]+$",
  "sort_order": 1,
  "is_active": true,
  "created_at": "2025-12-03T00:00:00",
  "created_by": "tester",
  "modified_at": null,
  "modified_by": null
}
```

---

## List Template Fields
**GET** `/api/pdc-template-field/list?template_id=1`

**Response:**
```
[
  {
    "template_field_id": 1,
    "template_id": 1,
    "metadata_key": "C1",
    "display_name": "First Name",
    "data_type": "string",
    "is_required": true,
    "default_value": "",
    "validation_rule": "^[A-Za-z]+$",
    "sort_order": 1,
    "is_active": true,
    "created_at": "2025-12-03T00:00:00",
    "created_by": "tester",
    "modified_at": null,
    "modified_by": null
  }
]
```

---

## Update Template Field
**POST** `/api/pdc-template-field/update`

**Request Body:**
```
{
  "template_field_id": 1,
  "display_name": "First Name Updated",
  "is_active": false,
  "modified_by": "updater"
}
```

**Response:**
```
{
  "template_field_id": 1,
  "template_id": 1,
  "metadata_key": "C1",
  "display_name": "First Name Updated",
  "data_type": "string",
  "is_required": true,
  "default_value": "",
  "validation_rule": "^[A-Za-z]+$",
  "sort_order": 1,
  "is_active": false,
  "created_at": "2025-12-03T00:00:00",
  "created_by": "tester",
  "modified_at": "2025-12-03T01:00:00",
  "modified_by": "updater"
}
```

---

## Delete Template Field
**POST** `/api/pdc-template-field/delete`

**Request Body:**
```
{
  "template_field_id": 1
}
```

**Response:**
```
Deleted
```

---

## Create Template
**POST** `/api/pdc-template`

**Request Body:**
```
{
  "name": "Test Template",
  "attributes": {
    "attribute_1": "A1",
    "attribute_2": "A2",
    "attribute_5": "A5"
  },
  "created_by": "tester",
  "is_active": true
}
```

**Response:**
```
{
  "template_id": 1,
  "name": "Test Template",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

---

## Get Template
**POST** `/api/pdc-template/get`

**Request Body:**
```
{
  "template_id": 1
}
```

**Response:**
```
{
  "template_id": 1,
  "name": "Test Template",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

**Note:**
- The `template_id` must be provided in the request body to fetch a specific template.

---

## List Templates (Cursor Pagination)
**POST** `/api/pdc-template/list`

**Request Body:**
```
{
  "cursor": 0,   // optional, returns templates after this id
  "limit": 10     // optional, number of templates to return
}
```

**Response:**
```
{
  "results": [ ...template objects... ],
  "next_cursor": <template_id or null>
}
```

**Note:**
- The `cursor` and `limit` parameters in the request body control pagination. Only templates with `template_id > cursor` are returned, up to the specified limit.

---

## Update Template
**POST** `/api/pdc-template/update`

**Request Body:**
```
{
  "template_id": 1,
  "name": "Updated Name",
  "attributes": {
    "attribute_1": "C1",
    "attribute_3": "C3"
  },
  "updated_by": "updater",
  "is_active": false
}
```

**Response:**
```
{
  "template_id": 1,
  "name": "Updated Name",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": "2025-12-01T01:00:00",
  "updated_by": "updater",
  "is_active": false
}
```

---

## Delete Template
**POST** `/api/pdc-template/delete`

**Request Body:**
```
{
  "template_id": 1
}
```

**Response:**
```
{
  "template_id": 1,
  "name": "Test Template",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

**Note:**
- The response returns the deleted record. If the record does not exist, a 404 is returned.

---

# PDC Class Endpoints
## Get Blank Class
**POST** `/api/pdc-class/blank`

**Request Body:**
```
{
  "template_id": 1
}
```

**Response:**
```
{
  "class_id": null,
  "template_id": 1,
  "name": null,
  "attributes": {
    "C1": null,
    "C2": null,
    "C3": null,
    ...
  },
  "created_at": null,
  "created_by": null,
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

**Note:**
- Returns a blank class record structure with attribute names based on the template definition.

## Create Class
**POST** `/api/pdc-class`

**Request Body:**
```
{
  "template_id": 1,
  "name": "Class Name",
  "attributes": {
    "C1": "Hari",
    "C3": "Baskar"
  },
  "created_by": "tester",
  "is_active": true
}
```

**Response:**
```
{
  "class_id": 1,
  "template_id": 1,
  "name": "Class Name",
  "attributes": {
    "C1": "Hari",
    "C2": null,
    "C3": "Baskar",
    ...
  },
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

---

## Get Class
**POST** `/api/pdc-class/get`

**Request Body:**
```
{
  "class_id": 1
}
```

**Response:**
```
{
  "class_id": 1,
  "template_id": 1,
  "name": "Class Name",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

---

## List Classes (Cursor Pagination)
**POST** `/api/pdc-class/list`

**Request Body:**
```
{
  "cursor": 0,   // optional, returns classes after this id
  "limit": 10     // optional, number of classes to return
}
```

**Response:**
```
{
  "results": [ ...class objects... ],
  "next_cursor": <class_id or null>
}
```

---

## Update Class
**POST** `/api/pdc-class/update`

**Request Body:**
```
{
  "class_id": 1,
  "name": "Updated Name",
  "attributes": {
    "C1": "New Value for C1",
    "C3": "New Value for C3"
  },
  "updated_by": "updater",
  "is_active": false
}
```

**Response:**
```
{
  "class_id": 1,
  "template_id": 1,
  "name": "Updated Name",
  "attributes": {
    "C1": "New Value for C1",
    "C2": null,
    "C3": "New Value for C3",
    ...
  },
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": "2025-12-01T01:00:00",
  "updated_by": "updater",
  "is_active": false
}
```

---

## Delete Class
**POST** `/api/pdc-class/delete`

**Request Body:**
```
{
  "class_id": 1
}
```

**Response:**
```
{
  "class_id": 1,
  "template_id": 1,
  "name": "Class Name",
  ...attributes...
  "created_at": "2025-12-01T00:00:00",
  "created_by": "tester",
  "updated_at": null,
  "updated_by": null,
  "is_active": true
}
```

**Note:**
- The response returns the deleted record. If the record does not exist, a 404 is returned.

---

**Note:**
- All requests and responses use JSON format.
- For pagination, use the `next_cursor` value from the response as the `cursor` in the next request.
