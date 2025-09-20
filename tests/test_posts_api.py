import time
import json
import pytest
from jsonschema import validate
from utils.schemas import POST_SCHEMA, POST_CREATE_SCHEMA

# 1) GET: lista de posts → 200, JSON y contrato básico para algunos elementos
def test_list_posts_contract(api):
    t0 = time.perf_counter()
    resp = api.get("/posts")
    print("respuesta", resp)
    dt = time.perf_counter() - t0

    assert resp.status == 200, f"Status: {resp.status}"
    assert "application/json" in resp.headers.get("content-type", "").lower()

    data = resp.json()

    assert isinstance(data, list) and len(data) > 0

    # validar contrato en los tres primeros (muestra)
    for item in data[:3]:
        validate(instance=item, schema=POST_SCHEMA)

    # performance (demostrativo)
    assert dt < 2.0, f"Respuesta lenta: {dt:.2f}s"


# 2) GET: detalle por id → 200 y coincide id
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_get_post_by_id(api, post_id):
    resp = api.get(f"/posts/{post_id}")
    assert resp.status == 200
    body = resp.json()
    validate(instance=body, schema=POST_SCHEMA)
    assert body["id"] == post_id

# 3) POST: crear recurso simulado → 201 y contrato de creación
def test_create_post(api):
    payload = {"title": "mi titulo", "body": "mi contenido", "userId": 1}
    resp = api.post("/posts", data=json.dumps(payload))
    assert resp.status in (201, 200)  # JSONPlaceholder suele devolver 201; toleramos 200
    body = resp.json()
    validate(instance=body, schema=POST_CREATE_SCHEMA)
    # eco de datos
    assert body["title"] == payload["title"], "el titulo no es el mismo"
    assert body["userId"] == payload["userId"], "el userId no es el mismo"
    assert body["body"] == payload["body"], "el body no es el mismo"


# 4) PUT: actualizar recurso simulado → 200 y refleja cambios
def test_update_post(api):
    post_id = 1
    payload = {"id": post_id, "title": "titulo actualizado", "body": "contenido", "userId": 1}
    resp = api.put(f"/posts/{post_id}", data=json.dumps(payload))
    assert resp.status == 200
    body = resp.json()
    # Algunos backends podrían ignorar campos; validamos los esenciales
    assert body.get("title") == "titulo actualizado"

# 5) DELETE: eliminar recurso simulado → 200/204 y cuerpo vacío o {}
def test_delete_post(api):
    post_id = 1
    resp = api.delete(f"/posts/{post_id}")
    assert resp.status in (200, 204)
    # En JSONPlaceholder, suele devolver {} con 200
    if resp.status == 200:
        assert resp.json() == {}

# 6) Búsqueda con query params → 200 y todos del userId indicado
def test_filter_posts_by_user(api):
    resp = api.get("/posts", params={"userId": 1})
    assert resp.status == 200
    items = resp.json()
    assert len(items) > 0
    assert all(item.get("userId") == 1 for item in items)

# 7) Cabeceras y tipo de contenido
def test_response_headers_are_json(api):
    resp = api.get("/posts/1")
    ctype = resp.headers.get("content-type", "").lower()
    assert "application/json" in ctype
    assert "charset=utf-8" in ctype


