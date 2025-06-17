def indivitual_data(todo):
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "status": todo["is_completed"],
    }


def list_data(todos):
    return [indivitual_data(todo) for todo in todos]