def userTweetEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Usuario": item["Usuario"],
        "id_user": item["id_user"],
        "name": item["name"],
        "location": item["location"],
        "description": item["description"],
        "entities": item["entities"],
        "followers_count": item["followers_count"],
        "friends_count": item["friends_count"],
        "created_at": item["created_at"],
        "listed_count": str(item["listed_count"]),
        "verified": item["verified"]
        
    }

def userTweetsEntity(entity) -> list:
    return [userTweetEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]
