from apiclient.discovery import build
from oauth2client.tools import argparser
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.environ.get("API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

channel_ids = []


def youtube_search(nextPageToken, options):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q='hl=ja',  # options.q,
        part="id",
        maxResults=options.max_results,
        publishedAfter='2019-01-01T00:00:00Z',
        regionCode='JP',
        type='channel',
        pageToken=nextPageToken
    ).execute()

    if nextPageToken == '':
        print('totalResults:' +
              str(search_response["pageInfo"]["totalResults"]))

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#channel":
            channel_ids.append(search_result["id"]["channelId"])

    if search_response.get('nextPageToken'):
        return search_response.get('nextPageToken')
    else:
        return ''


def channel_list(id_str):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    results = youtube.channels().list(
        part='statistics,snippet,brandingSettings',
        id=id_str
    ).execute()

    for res in results.get("items", []):
        # res["snippet"]["country"] == 'JP'
        if int(res["statistics"]["subscriberCount"]) >= 1000:
            print("===============================================")
            print("https://www.youtube.com/channel/" + res["id"])
            print("subscriberCount: " + res["statistics"]["subscriberCount"])
            print("title: " + res["snippet"]["localized"]["title"])
            print("videoCount: " + res["statistics"]["videoCount"])
            print("publishedAt: " + res["snippet"]["publishedAt"])


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=50)
    args = argparser.parse_args()

    nextPageToken = youtube_search('', args)

    while nextPageToken:
        print("nextPageToken: " + nextPageToken)
        nextPageToken = youtube_search(nextPageToken, args)

    tmp = []
    for channel_id in channel_ids:
        tmp.append(channel_id)
        # リクエストにわたすチャンネルの数が多すぎるとエラーになるので1リクエスト最大10チャンネルIDにしておく
        if len(tmp) >= 10:
            channel_list(','.join(tmp))
            tmp = []
