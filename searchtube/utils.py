import datetime
import os
import string
from . import db


def timestamp_to_secs(timestamp: str) -> int:
    if '.' in timestamp:
        timestamp = timestamp.split('.')[0]
    result =  int(str((datetime.datetime.strptime(timestamp, '%H:%M:%S') - datetime.datetime(1900, 1, 1)).total_seconds()).split('.')[0])
    return result


def date_to_epoch(date: str) -> int:
    return int((datetime.datetime.strptime(date, '%Y%m%d') - datetime.datetime(1970,1,1)).total_seconds())


def is_two_weeks_old(timestamp: int) -> bool:
    two_weeks_ago = int((datetime.datetime.now() - datetime.timedelta(days=13)).timestamp())
    return timestamp < two_weeks_ago


def add_to_ignore(channel_id: str, video_id: str) -> None:
    client = db.get_client()
    database = client.get_database(channel_id)
    ignore_coll = database.get_collection('ignore')
    if not ignore_coll.find_one({"video_id": video_id}):
        ignore_coll.insert_one({"video_id": video_id})


def add_channel(channel_id: str, name: str) -> None:
    prefix = '/var/www/searchtube/data'
    if not os.path.exists(f'{prefix}/{channel_id}/'):
        os.mkdir(f'{prefix}/{channel_id}/')

    client = db.get_client()
    database = client.get_database('searchtube')
    channels_coll = database.get_collection('channels')
    if not channels_coll.find_one({"channel_id": channel_id}):
        channels_coll.insert_one({"channel_id": channel_id, "channel_name": name, "is_new": True})


def remove_channel(channel_id: str) -> None:
    client = db.get_client()
    channels_database = client.get_database('searchtube')
    channels_coll = channels_database.get_collection('channels')
    if channels_coll.find_one({"channel_id": channel_id}):
        # Delete from config db
        channels_coll.delete_one({"channel_id": channel_id})
        # Delete videos data
        client.drop_database(channel_id)


def channel_is_in_db(channel_id: str) -> bool:
    client = db.get_client()
    database = client.get_database('searchtube')
    channels_coll = database.get_collection('channels')
    return bool(channels_coll.find_one({"channel_id": channel_id}))


def get_channels() -> list:
    client = db.get_client()
    database = client.get_database('searchtube')
    channels_coll = database.get_collection('channels')
    return list(channels_coll.find())


def clean_vtt(data) -> list:
    results = []
    last_lines = []
    for caption in data:
        if all(bool(x.strip()) for x in caption.text.split('\n')):
            text_lines = caption.text.split('\n')
            text_lines = list(filter(lambda x: x not in last_lines, text_lines))
            text = ' '.join(text_lines)
            caption.text = text
            last_lines = text_lines
            results.append(caption)

    return results


def clean_text(text: str) -> str:
    words = text.split()
    cleaned_text_list = []
    for word in words:
        word = word.lower()
        word = word.strip(string.punctuation)
        if word:
            cleaned_text_list.append(word)
    cleaned_text = ' '.join(cleaned_text_list)
    return cleaned_text
