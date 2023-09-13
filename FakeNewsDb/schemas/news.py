def newsEntity(item) -> dict:
    return {
        "id": str(item["_id"]) if "_id" in item else None,
        "title": item["title"],
        "body": item["body"],
        "type": item["type"],
        "source": item["source"],
        "date": item["date"],
        "link": item["link"]
    }

def newsEntityList(entity) -> list:
    return [newsEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]