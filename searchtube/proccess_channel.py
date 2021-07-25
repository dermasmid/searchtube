from pymongo.results import UpdateResult
import webvtt
from . import db, utils, download_subtitle



def process(channel_id: str) -> None:
    is_new = channel_is_new(channel_id)
    videos = download_subtitle.get_videos(channel_id, is_new)
    for video in videos:
        video_id = video['videoId']
        if video_is_new(channel_id, video_id):
            data = download_subtitle.download(channel_id, video_id)
            if data:
                save(channel_id, data['path'], data['date'], video_id)
    if is_new:
        set_channel_to_old(channel_id)




def save(channel_id: str, path: str, date: int, video_id: str) -> None:
    client = db.get_client()
    database = client.get_database(channel_id)
    full_coll = database.get_collection('full_text')
    video_coll = database.get_collection(video_id)
    lines = webvtt.read(path)
    all_words = ''
    word_index = 0
    for caption in utils.clean_vtt(lines):
        text = utils.clean_text(caption.text)
        start = utils.timestamp_to_secs(caption.start) - 1
        end = utils.timestamp_to_secs(caption.end) + 1
        all_words += " " + text
        words_len = len(text.split(' '))
        indexes = list(range(word_index, word_index + words_len))
        data = {
            'start': start,
            'end': end,
            'indexes': indexes
        }
        video_coll.insert_one(data)
        word_index += words_len
    data = {
        'video_id': video_id,
        'data': all_words.strip(),
        'date': date,
    }
    full_coll.insert_one(data)
    full_coll.create_index([('data', 'text')])
    video_coll.create_index('indexes')



def video_is_new(channel_id: str, video_id: str) -> bool:
    client = db.get_client()
    database = client.get_database(channel_id)
    ignore_coll = database.get_collection('ignore')
    ignore = bool(ignore_coll.find_one({"video_id": video_id}))
    return video_id not in list(database.list_collection_names()) and not ignore


def channel_is_new(channel_id: str) -> bool:
    client = db.get_client()
    database = client.get_database('searchtube')
    channels_coll = database.get_collection('channels')
    return bool(channels_coll.find_one({"channel_id": channel_id, "is_new": True}))


def set_channel_to_old(channel_id: str) -> UpdateResult:
    client = db.get_client()
    database = client.get_database('searchtube')
    channels_coll = database.get_collection('channels')
    return channels_coll.update_one({"channel_id": channel_id}, {"$set": {"is_new": False}})


def reprocess_channel(channel_id: str) -> None:
    client = db.get_client()
    database = client.get_database(channel_id)
    full_coll = database.get_collection('full_text')
    videos = list({'video_id': i['video_id'], 'date': i['date']} for i in full_coll.find())
    for video in videos:
        video_id = video['video_id']
        print(f'Now reprocessing video: {video_id}')
        date = video['date']
        subtitle_path = f'/var/www/searchtube/data/{channel_id}/{video_id}.en.vtt'
        full_coll.delete_one({'video_id': video_id})
        database.drop_collection(video_id)
        save(channel_id, subtitle_path, date, video_id)


def reprocess_channels() -> None:
    for channel in utils.get_channels():
        print(f'Now reprocessing channel: {channel["channel_id"]}')
        reprocess_channel(channel['channel_id'])
