import webvtt
import get_channel
from . import db, utils, download_subtitle



def proccess(channel_id):
    videos = get_videos(channel_id)
    for video in videos:
        video_id = video['video_url'].split('v=')[1]
        if video_is_new(channel_id, video_id):
            data = download_subtitle.download(channel_id, video_id)
            if data:
                save(channel_id, data['path'], data['date'], video_id)





def save(channel_id, path, date, video_id):
    client = db.get_client()
    database = client.get_database(channel_id)
    full_coll = database.get_collection('full_text')
    video_coll = database.get_collection(video_id)
    lines = webvtt.read(path)
    all_words = ''
    word_index = 0
    for caption in utils.clean_vtt(lines):
        start = utils.timestamp_to_secs(caption.start) - 1
        end = utils.timestamp_to_secs(caption.end) + 1
        all_words += " " + caption.text
        words_len = len(caption.text.split(' '))
        indexes = list(range(word_index, word_index + words_len))
        data = {
            'start': start,
            'end': end,
            'indexes': indexes
        }
        video_coll.insert_one(data)
        video_coll.create_index('indexes')
        word_index += words_len
    data = {
        'video_id': video_id,
        'data': all_words.strip(),
        'date': date,
    }
    full_coll.insert_one(data)
    full_coll.create_index([('data', 'text')])



def video_is_new(channel_id, video_id):
    client = db.get_client()
    database = client.get_database(channel_id)
    ignore_coll = database.get_collection('ignore')
    ignore = bool(ignore_coll.find_one({"video_id": video_id}))
    return video_id not in list(database.list_collection_names()) and not ignore



def get_videos(channel_id):
    getter = get_channel.ListCreator(headless= True, driver= 'chrome', scroll_pause_time= 1, cookie_consent= True)
    data = getter.create_list_for(f'https://www.youtube.com/channel/{channel_id}', channel_id)
    return data
