#coding=utf-8

'''
requires Python 3.6 or later
pip install requests pydub
'''
import os
import base64
import json
import uuid
import requests
import play

# 填写平台申请的appid, access_token以及cluster
appid = ""
access_token= ""
cluster = "volcano_tts"

voice_type = "BV700_V2_streaming"
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

def say(text, index):

    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "wav",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }
    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        # print(f"resp body: \n{resp.json()}")
        if "data" in resp.json():
            data = resp.json()["data"]
            file_path = f"temp_audio_{index}.wav"
            with open(file_path, "wb") as file_to_save:
                file_to_save.write(base64.b64decode(data))
                file_to_save.close()
            play.play_mp3(file_path)
            # os.remove(file_path)
    except Exception as e:
        e.with_traceback()

# say(input("Please enter the text you want to convert to speech: "))
