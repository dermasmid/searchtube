import youtube_dl
import os
import json
from . import utils


def download(channel_id, video_id):
    prefix = '/var/www/rextube/data'
    subtitle_path = f'{prefix}/{channel_id}/{video_id}.en.vtt'
    output_path = f'{prefix}/{channel_id}/{video_id}'
    map_file = f'{prefix}/{channel_id}/map.json'

    with open(map_file, 'r') as f:
        map_data = json.load(f)

    if not os.path.exists(subtitle_path) or not video_id in map_data:

        ydl_opts = {
            'writeautomaticsub': True,
            'outtmpl': output_path,
            'skip_download': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(video_id)

        date = utils.date_to_epoch(data['upload_date'])

        if os.path.exists(subtitle_path):
            map_data[video_id] = {'path': subtitle_path, 'date': date}

        elif utils.is_two_weeks_old(date):
            utils.add_to_ignore(channel_id, video_id)


    with open(map_file, 'w') as f:
        json.dump(map_data, f)

    return map_data.get(video_id)
