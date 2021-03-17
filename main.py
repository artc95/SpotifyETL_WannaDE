import json
import datetime
import requests
import pandas as pd

TOKEN = "BQBtrFOXFbVIad0NDgx091J5sg0e1_dkOtH4-Q99CtlXUznA1JQx9h4DCo5c5HRQaHVwn0-aE2FFE-tDhhDscHiNY0_jwX8qienV7ibd-95KyYrAIsJNfaM2v2Hq3437bA3kPvG3vFEnFRRMMuS6uCFRb24E-CqfkXb-XDnTUI-nW9vJw0tRUA"

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token = TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_unix = int(yesterday.timestamp()) * 1000 #convert unix in seconds to milliseconds for spotify

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?&after={time}".format(time=yesterday_unix), headers=headers)
    data = r.json()
    
    song_names = []
    artist_names = []
    played_at = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at"])
    print(song_df)