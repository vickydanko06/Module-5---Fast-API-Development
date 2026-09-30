# exercises/test-suite/tests/test_tasks.py
# L11 — Task API test suite
#
# Your task: Write 8+ tests for the Task CRUD API.
# Run with: pytest tests/ -v  (from the test-suite/ folder)

# Key concept: Test structure — AAA (Arrange / Act / Assert)
# Every test follows the same pattern:
#   Arrange: Set up any prerequisite state (e.g., create a task first)
#   Act:     Make the HTTP request via the TestClient
#   Assert:  Check the response status code and body

# TODO: Write the following tests:

def test_create_task(client):
    """
    Test: POST /tasks creates a task and returns 201.

    TODO:
    1. POST to /tasks with {"title": "Buy groceries", "completed": False}
    2. Assert response.status_code == 201
    3. Assert response.json()["title"] == "Buy groceries"
    4. Assert "id" is in the response
    """
    pass  # TODO: implement
    response = client.post("/tasks", json={"title": "Buy groceries", "completed": False})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy groceries"
    assert "id" in response.json()



def test_list_tasks(client):
    """
    Test: GET /tasks returns 200 and a list.

    TODO:
    1. GET /tasks
    2. Assert 200
    3. Assert isinstance(response.json(), list)
    """
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id(client):
    """
    Test: GET /tasks/{id} returns the created task.

    TODO:
    1. Create a task first (POST)
    2. GET /tasks/{id} using the returned id
    3. Assert 200 and correct title
    """
    response = client.post("/tasks", json={"title": "test", "completed": False})
    task_id = response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "test"


def test_get_nonexistent_task_returns_404(client):
    """
    Test: GET /tasks/9999 returns 404.

    TODO:
    1. GET /tasks/9999
    2. Assert response.status_code == 404
    """
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_patch_task(client):
    """
    Test: PATCH /tasks/{id} updates only the specified fields.

    TODO:
    1. Create a task
    2. PATCH with {"completed": True}
    3. Assert 200 and completed == True in response
    4. Assert title is unchanged
    """
    response = client.post("/tasks", json={"title": "test", "completed": False})
    task_id = response.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"completed" : True})
    assert response.status_code == 200
    assert response.json()["completed"] == True
    assert response.json()["title"] == "test"

def test_delete_task(client):
    """
    Test: DELETE /tasks/{id} removes the task.

    TODO:
    1. Create a task
    2. DELETE /tasks/{id}
    3. Assert 200
    4. GET /tasks/{id} again — assert 404
    """
    response = client.post("/tasks", json={"title": "test", "completed": False})
    task_id = response.json()["id"]
    response =client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404



def test_create_task_invalid_data_returns_422(client):
    """
    Test: POST /tasks with an empty title returns 422.

    TODO:
    1. POST /tasks with {"title": ""}  (empty string violates min_length=1)
    2. Assert response.status_code == 422
    """
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422

def test_duplicate_task_title_returns_409(client):
    """
    Test: Creating two tasks with the same title returns 409.

    TODO:
    1. POST /tasks with title "Unique Task"
    2. POST /tasks with the same title again
    3. Assert second response.status_code == 409
    """

    response1 = client.post("/tasks", json={"title": "Unique Task", "completed": False})
    assert response1.status_code == 201
    response2 = client.post("/tasks", json={"title": "Unique Task", "completed": False})
    assert response2.status_code == 409