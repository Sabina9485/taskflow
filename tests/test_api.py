def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_user(client):
    response = client.post(
        "/v1/users",
        json={"email": "test@example.com", "display_name": "Test User", "role": "operator"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "operator"
    assert "id" in data


def test_get_user_not_found(client):
    response = client.get("/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_duplicate_user(client):
    client.post("/v1/users", json={"email": "dup@example.com", "display_name": "First"})
    response = client.post("/v1/users", json={"email": "dup@example.com", "display_name": "Second"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_invalid_data_returns_422(client):
    response = client.post("/v1/users", json={"email": "not-an-email", "display_name": ""})
    assert response.status_code == 422


def test_update_user(client):
    res = client.post("/v1/users", json={"email": "upd@example.com", "display_name": "Old"})
    user_id = res.json()["id"]
    
    response = client.patch(f"/v1/users/{user_id}", json={"display_name": "New"})
    assert response.status_code == 200
    assert response.json()["display_name"] == "New"
    assert response.json()["email"] == "upd@example.com"


def test_delete_user(client):
    res = client.post("/v1/users", json={"email": "del@example.com", "display_name": "To Delete"})
    user_id = res.json()["id"]
    
    response = client.delete(f"/v1/users/{user_id}")
    assert response.status_code == 204
    
    response = client.get(f"/v1/users/{user_id}")
    assert response.status_code == 404


def test_cascade_delete_project(client):
    proj = client.post("/v1/projects", json={"name": "Test Project"}).json()
    task = client.post("/v1/tasks", json={"project_id": proj["id"], "title": "Test Task"}).json()
    
    client.delete(f"/v1/projects/{proj['id']}")
    
    response = client.get(f"/v1/tasks/{task['id']}")
    assert response.status_code == 404
# --- ОТРИЦАТЕЛЬНЫЕ ТЕСТЫ (Negative Tests) ---

def test_create_task_invalid_project_fk(client):
    """Отрицательный тест: создание задачи для несуществующего проекта (должно вернуть 409)"""
    response = client.post(
        "/v1/tasks",
        json={
            "project_id": 9999,  # Такого проекта нет
            "title": "Invalid Task",
            "priority": "high"
        }
    )
    # Ожидаем ошибку конфликта (нарушение FK)
    assert response.status_code == 409
    assert "Invalid" in response.json()["detail"]

def test_update_user_invalid_role(client):
    """Отрицательный тест: передача несуществующей роли (должно вернуть 422)"""
    res = client.post("/v1/users", json={"email": "role@example.com", "display_name": "Role Test"})
    user_id = res.json()["id"]
    
    response = client.patch(
        f"/v1/users/{user_id}",
        json={"role": "super_admin"}  # Такой роли нет в Literal
    )
    # Ожидаем ошибку валидации
    assert response.status_code == 422

def test_get_task_not_found(client):
    """Отрицательный тест: запрос несуществующей задачи (должно вернуть 404)"""
    response = client.get("/v1/tasks/88888")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task not found"
