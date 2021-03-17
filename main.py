import json
import datetime
import requests
import pandas as pd

TOKEN = "BQBtrFOXFbVIad0NDgx091J5sg0e1_dkOtH4-Q99CtlXUznA1JQx9h4DCo5c5HRQaHVwn0-aE2FFE-tDhhDscHiNY0_jwX8qienV7ibd-95KyYrAIsJNfaM2v2Hq3437bA3kPvG3vFEnFRRMMuS6uCFRb24E-CqfkXb-XDnTUI-nW9vJw0tRUA"

# set after timestamp i.e. songs played after this timestamp
after = datetime.datetime.now() - datetime.timedelta(days=3)

def quality_checks(df)->bool:
    #check if dataframe empty
    if df.empty:
        print("No songs downloaded.")
        return False

    #check primary key
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary key check failed.")

    #check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found.")

    #check if all timestamps are after after_timestamp
    after_date = after.replace(hour=0, minute=0, second=0, microsecond=0)

    played_at_list = df["played_at"].tolist()
    for timestamp in played_at_list:
        if datetime.datetime.strptime(timestamp[0:10], "%Y-%m-%d") < after_date: #timestamp[0:10] to only check date
            raise Exception("At least one song was not played after date restriction.")

    return True

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token = TOKEN)
    }

    after_unix = int(after.timestamp()) * 1000 #convert unix in seconds to milliseconds for spotify

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?&after={time}".format(time=after_unix), headers=headers)
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
    
    if quality_checks(song_df):
        print("Data valid.")
        print(song_df)