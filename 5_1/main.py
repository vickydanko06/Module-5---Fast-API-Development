# exercises/hello-fastapi/main.py
# L1 — Hello FastAPI
#
# Your task: Build a simple FastAPI app with several endpoints demonstrating
# core concepts: decorators, path parameters, and automatic documentation.
#
# Run with: uvicorn main:app --reload
# Docs at:  http://127.0.0.1:8000/docs

# TODO: Import FastAPI from the fastapi package
from fastapi import FastAPI

# TODO: Create a FastAPI app instance
# Hint: app = FastAPI()
app = FastAPI() #create a FastAPI instance


# TODO: Define a root endpoint at GET /
# It should return a welcome message as a dictionary, e.g.:
# {"message": "Welcome to Hello FastAPI!"}
#
# Key concept: The @app.get("/") decorator tells FastAPI to call this
# function whenever a GET request is made to the "/" path.
@app.get("/")
def root():
    """
    Root endpoint — returns a welcome message.

    TODO: Return a dict with a "message" key.
    """
    pass  # TODO: implement
    return {"message":"Welcome to Hello FastAPI"} #this is returned at the /root 


# TODO: Define GET /hello that returns a plain string greeting
@app.get("/hello")
def say_hello():
    """
    Returns a simple string greeting.

    TODO: Return a string like "Hello, FastAPI!"
    """
    pass  # TODO: implement
    return "Hello, FastAPI!" 


# TODO: Define GET /info that returns a dictionary with app metadata
# Include keys like "name", "version", and "description"
@app.get("/info")
def get_info():
    """
    Returns app metadata as a dict.

    TODO: Return a dict with at least "name", "version", "description".
    """
    pass  # TODO: implement
    return {
    "name": "Hello FastAPI",
    "version": "1.0.0",
    "description": "A simple FastAPI application."
}



# TODO: Define GET /items that returns a list of example items
# Each item should be a dict with at least "id" and "name"
@app.get("/items")
def list_items():
    """
    Returns a list of example items.

    TODO: Return a list of dicts, e.g. [{"id": 1, "name": "Widget"}, ...]
    """
    pass  # TODO: implement
    return [{"id": 1,"name":"Mouse","description":"to control your cursor"},{"id": 2,"name":"Keyboard","description":"to type on your screen"},{"id":3,"name":"Monitor","description":"to see"}]


# TODO: Define GET /items/{item_id} that accepts a path parameter
# Return a dict that includes the item_id you received
#
# Key concept: Path parameters are defined with {curly_braces} in the path
# and appear as function arguments with matching names.
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Returns a single item by ID.

    Args:
        item_id: The integer ID from the URL path.

    TODO: Return a dict like {"id": item_id, "name": "...", "description": "..."}
    """
    pass  # TODO: implement
    return {
        "id": item_id,
        "name": "Example Item",
        "description": "This is an example item."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)