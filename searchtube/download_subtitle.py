import youtube_dl
import os
import json
import requests
import time
from . import utils


def download(channel_id: str, video_id: str) -> dict:
    prefix = '/var/www/searchtube/data'
    subtitle_path = f'{prefix}/{channel_id}/{video_id}.en.vtt'
    map_file = f'{prefix}/{channel_id}/map.json'


    with open(map_file, 'r') as f:
        map_data = json.load(f)

    if not os.path.exists(subtitle_path) or not video_id in map_data:

        youtube_dl_options = {
            'skip_download': True,
        }

        with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
            raw_video_info = ydl.extract_info(video_id)
            time.sleep(os.environ['DOWNLOAD_SLEEP_TIME'])

        date = utils.date_to_epoch(raw_video_info['upload_date'])
        subtitle_data = get_english_subtitles(raw_video_info)
        if subtitle_data:
            download_subtitle(subtitle_data, subtitle_path)
            map_data[video_id] = {'path': subtitle_path, 'date': date}


        elif utils.is_two_weeks_old(date):
            utils.add_to_ignore(channel_id, video_id)


    with open(map_file, 'w') as f:
        json.dump(map_data, f)

    return map_data.get(video_id)



def get_english_subtitles(raw_video_info: dict) -> dict:
    if raw_video_info.get('automatic_captions', {}).get('en'):
        subtitles = raw_video_info['automatic_captions']['en']
    
    elif raw_video_info.get('subtitles'):
        english_subtitle = list(i for i in raw_video_info['subtitles'] if 'en' in i)[0]
        if english_subtitle:
            subtitles = raw_video_info['subtitles'][english_subtitle]
    else:
        subtitles = {}

    return subtitles


def download_subtitle(subtitle_data: dict, output_path: str) -> str:
    url = list(i['url'] for i in subtitle_data if i['ext'] == 'vtt')[0]

    with open(output_path, 'wb') as f:
        f.write(requests.get(url).content)

    return output_path
