# project/starter/tests/test_tasks.py
# Module 5 Project — Example test (starter)

def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# project/starter/tests/test_tasks.py

def register_user(client, username, email, password="TestPassword123!"):
    """Helper function to register a user."""
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def login_user(client, username, password="TestPassword123!"):
    """Helper function to log in and retrieve an access token."""
    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": password
        }
    )

    return response


def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_user(client):
    """A new user can register."""

    response = register_user(
        client,
        "testuser",
        "test@example.com"
    )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    assert "hashed_password" not in response.json()


def test_login(client):
    """A registered user can log in."""

    register_user(client, "loginuser", "login@example.com")

    response = login_user(client, "loginuser")

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_task_authenticated(client):
    """An authenticated user can create a task."""

    register_user(client, "taskuser", "task@example.com")

    login_response = login_user(client, "taskuser")
    token = login_response.json()["access_token"]

    response = client.post(
        "/tasks/",
        json={
            "title": "Finish Module 5",
            "description": "Complete API testing",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Finish Module 5"
    assert response.json()["completed"] is False
    assert response.json()["owner_id"] > 0


def test_list_tasks_scoped_to_user(client):
    """Users should only see their own tasks."""

    # Register two users
    register_user(client, "alice", "alice@example.com")
    register_user(client, "bob", "bob@example.com")

    # Log in both users
    alice_token = login_user(client, "alice").json()["access_token"]
    bob_token = login_user(client, "bob").json()["access_token"]

    # Alice creates a task
    client.post(
        "/tasks/",
        json={
            "title": "Alice's task",
            "description": "Private task"
        },
        headers={
            "Authorization": f"Bearer {alice_token}"
        }
    )

    # Bob creates a task
    client.post(
        "/tasks/",
        json={
            "title": "Bob's task",
            "description": "Another private task"
        },
        headers={
            "Authorization": f"Bearer {bob_token}"
        }
    )

    # Retrieve Alice's tasks
    alice_response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {alice_token}"
        }
    )

    # Retrieve Bob's tasks
    bob_response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {bob_token}"
        }
    )

    assert alice_response.status_code == 200
    assert bob_response.status_code == 200

    alice_tasks = alice_response.json()
    bob_tasks = bob_response.json()

    assert len(alice_tasks) == 1
    assert len(bob_tasks) == 1

    assert alice_tasks[0]["title"] == "Alice's task"
    assert bob_tasks[0]["title"] == "Bob's task"


def test_get_task_suggest(client):
    """An authenticated user can get a task suggestion."""

    register_user(client, "suggestuser", "suggest@example.com")

    token = login_user(
        client,
        "suggestuser"
    ).json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create a task
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Learn Python",
            "description": "Practice Python programming"
        },
        headers=headers
    )

    task_id = create_response.json()["id"]

    # Request a suggestion
    response = client.get(
        f"/tasks/{task_id}/suggest",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["task_id"] == task_id
    assert "suggestion" in response.json()
