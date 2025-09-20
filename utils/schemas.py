POST_SCHEMA = {
    "type": "object",
    "required": [
        "userId",
        "id",
        "title",
        "body"
    ],
    "properties": {
        "userId": {"type": "integer"},
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
    },
    "additionalProperties": True
}

POST_CREATE_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id":     {"type": "integer"},          # JSONPlaceholder devuelve un id simulado (p.ej., 101)
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
    "additionalProperties": True
}
