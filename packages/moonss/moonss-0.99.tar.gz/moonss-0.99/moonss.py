import os
import time
from DownloadHelper import download_ytdlp, download_tiktok_video, download_douyin_video, donwload_instagram_video, donwload_artlistio_video, donwload_canva_video
from SourceDataHelper import process_video_sd
import requests

URL_HOME="https://moonseo.app"
URL_GET_JOB=f"{URL_HOME}/api/source/data/crawl"
URL_UPDATE_JOB=f"{URL_HOME}/api/source/data/update-by-id"
headers={"platform":"autowin"}


def execute():
    print("crawling: "+str(time.time()))
    obj = requests.get(URL_GET_JOB, headers=headers).json()
    if "id" in obj:
        print("Process: "+str(obj['id']))
        video_path = None
        if obj['platform'] =='tiktok':
            video_path = download_tiktok_video(obj['ori_link'])
        if obj['platform'] =='youtube' or obj['platform'] =='youtube-long':
            video_path = download_ytdlp(obj['ori_link'])
        if obj['platform'] =='douyin':
            video_path = download_douyin_video(obj['platform_id'])
        if obj['platform'] == 'instagram':
            video_path = donwload_instagram_video(obj['crawl_data'])
        if obj['platform'] == 'artlistio':
            video_path = donwload_artlistio_video(obj['crawl_data'])
        if obj['platform'] == 'canva':
            video_path = donwload_canva_video(obj['crawl_data'])
        sc_new = process_video_sd(video_path)
        if not sc_new:
            sc_new={"id": obj['id']}
            if(obj['crawl_retries']<3):
                sc_new['crawl_retries']=obj['crawl_retries']+1
                sc_new['status'] = 1 #retries
            else:
                sc_new['status'] = 4
        else:
            sc_new['id']=obj['id']
            sc_new['status'] = 3
        rs=requests.post(URL_UPDATE_JOB, json=sc_new, headers=headers).json()
        print(rs)
        return True
    else:
        return False
def update():
    libs=["moonss", "coolbg", "gbak"]
    for lib in libs:
        os.system(f"pip install -U {lib}")

