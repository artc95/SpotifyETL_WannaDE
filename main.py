import json
import datetime
import requests
import pandas as pd

TOKEN = "BQABhg8g6s_ZUgZfDOWHedzRW2UoqN3Om8GDvRLoYf1DO-rC74zZKovjIRJ7drqDgTIs6njNOl4Eh20Uet_l9L_6ofGCpVYUQd9rrxcDSOuelrr3t44QIBQlJezLaxyRdB1teNgKrOOCq9xunkfR9oWy4Lh8cqtv2MDPwsUU07SNoYpUj35-_Q"

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
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0-10]) #only date, no time

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    print(song_df)