import youtube_dl
import os
import requests
import time
from . import utils


def get_videos(channel_id: str, channel_is_new: bool):

    youtube_dl_options = {
        'skip_download': True,
        'ignoreerrors': True
    }

    if not channel_is_new:
        # this does still hit all the videos
        # youtube_dl_options['dateafter'] = 'now-1week'
        youtube_dl_options['playlistend'] = 10

    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
        raw_videos_info = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}/videos')

    return raw_videos_info.get('entries')


def download(channel_id: str, video_data: dict) -> dict:
    video_id = video_data['id']
    subtitle_path = f'/var/www/searchtube/data/{channel_id}/{video_id}.en.vtt'

    if not os.path.exists(subtitle_path):
        date = utils.date_to_epoch(video_data['upload_date'])
        subtitle_data = get_english_subtitles(video_data)

        if subtitle_data:
            print('Downloading subtitles for ' + video_id)
            download_subtitle(subtitle_data, subtitle_path)
            print('Sleeping')
            time.sleep(int(os.environ['DOWNLOAD_SLEEP_TIME']))
            return {'path': subtitle_path, 'date': date}

        elif utils.is_two_weeks_old(date):
            utils.add_to_ignore(channel_id, video_id)
            return None




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
