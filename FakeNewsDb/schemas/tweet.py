# app/schemas/tweet.py
def tweetEntity(item)-> dict:
    return{
        "id":str(item["_id"]),
        "id_autor":item["id_autor"],
        "tweet_id":item["tweet_id"],
        "text":item["text"],
        "date_of_publication":item["date_of_publication"],
        "retweet_count":item["retweet_count"],
        "reply_count":item["reply_count"],
        "like_count":item["like_count"],
        "quote_count":item["quote_count"],
        "bookmark_count":item["bookmark_count"],
        "impression_count":item["impression_count"],
        "verasidad":item["verasidad"]
    }

def tweetsEntity(entity)->list:
    return[tweetEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]