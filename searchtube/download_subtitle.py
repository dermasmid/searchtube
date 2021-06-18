import youtube_dl
from youtube_dl.extractor.common import InfoExtractor
from youtube_dl.utils import std_headers
import webvtt
import random
import os
import requests
import time
from . import utils

# Add sleep, youtube-dl only sleeps when it downloads something, we don't
def report_download_webpage_decorator(report_download_webpage_orig):
    def report_download_webpage(self, video_id):
        report_download_webpage_orig(self, video_id)
        sleep_interval = random.uniform(40, 60)
        print("Sleeping for %s" % sleep_interval)
        time.sleep(sleep_interval)

    return report_download_webpage

InfoExtractor.report_download_webpage = report_download_webpage_decorator(InfoExtractor.report_download_webpage)


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
