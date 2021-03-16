import json
import datetime
import requests

TOKEN = "BQAPI3LgoqO2RC9KLbPnlelmVRf_7AxIruAH0-jPeRl72GTSqRiGwUZw5VDMc1adQx_IL-xn_KREHEt60mdU36umfL3mkwt0JCmnayEeEzOcf8o2F77E8MZPDB9bZES0hMDkQOxgY4lw6anA5fnZ6qComvbv91VoqDWSWHzjI_K3oDkZNeroLQ"

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token = TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_unix = int(yesterday.timestamp()) * 1000 #convert unix in seconds to milliseconds for spotify

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix), headers=headers)
    data = r.json()
    print(data)