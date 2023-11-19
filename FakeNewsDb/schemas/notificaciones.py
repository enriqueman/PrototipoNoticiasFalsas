def notificationEntity(item)-> dict:
    return{
        #"id":str(item["_id"]),
        "titulo":item["titulo"],
        "texto":item["texto"],
        "fecha":item["fecha"],
        "veracidad":item["veracidad"],
        "autor":item["autor"],
        "notificado":item["notificado"],
    }

def notificationsEntity(entity)->list:
    return[notificationEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]