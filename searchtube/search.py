from . import db, str_find


def search(channel_id: str, q: str, limit = 0):
    results = []
    client = db.get_client()
    database = client.get_database(channel_id)
    full_coll = database.get_collection('full_text')
    vague_results = full_coll.find({'data': {'$regex': rf'\b{q}\s'}}).sort('date', -1).allow_disk_use(True).limit(limit)
    for video in vague_results:
        video_id = video['video_id']
        video_coll = database.get_collection(video_id)
        points = str_find.split_find(video['data'], q)
        for result in points:
            data = list(video_coll.find({'indexes': {"$in": result}}))
            start = data[0]['start']
            end = data[-1]['end']
            results.append(f"https://www.youtube.com/embed/{video_id}?start={start}&end={end}")


    return results
