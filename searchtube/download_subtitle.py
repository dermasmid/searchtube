from typing import Generator
from youtube_dl import std_headers, YoutubeDL
import webvtt
import random
import os
import requests
import time
import list_youtube_channel
from . import utils



def get_videos(channel_id: str, channel_is_new: bool) -> Generator:
    limit = 20 if channel_is_new else None
    videos = list_youtube_channel.get_channel(channel_id, limit = limit)
    return videos


def download(channel_id: str, video_id: str) -> dict:
    subtitle_path = f'/var/www/searchtube/data/{channel_id}/{video_id}.en.vtt'

    youtube_dl_options = {
        'skip_download': True,
    }
    with YoutubeDL(youtube_dl_options) as ydl:
        video_data = ydl.extract_info(video_id)

    if not os.path.exists(subtitle_path):
        date = utils.date_to_epoch(video_data['upload_date'])
        subtitle_data = get_english_subtitles(video_data)

        if subtitle_data:
            print('Downloading subtitles for ' + video_id)
            download_subtitle(subtitle_data, subtitle_path)
            if bool(int(os.environ['SLEEP_AFTER_DOWNLOAD'])):
                print('Sleeping')
                sleep_interval = random.uniform(30, 60)
                time.sleep(sleep_interval)
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

    success = False

    while not success:
        with open(output_path, 'wb') as f:
            f.write(requests.get(url, headers= std_headers).content)

        try:
            webvtt.read(output_path)
            success = True
        except webvtt.errors.MalformedCaptionError:
            sleep_interval = random.uniform(30 * 60, 45 * 60)
            print(f'Got reject from youtube, going to sleep for {int(sleep_interval // 60)} minutes')
            time.sleep(sleep_interval)
            continue

    return output_path
