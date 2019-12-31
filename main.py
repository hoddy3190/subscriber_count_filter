from apiclient.discovery import build
from apiclient.errors import HttpError
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

    # videos = []
    # channels = []
    # playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#channel":
            channel_ids.append(search_result["id"]["channelId"])

    if search_response.get('nextPageToken'):
        return search_response.get('nextPageToken')
    else:
        return ''
        # if search_result["id"]["kind"] == "youtube#video":
        #     videos.append("%s (%s)" % (
        #         search_result["snippet"]["title"], search_result["id"]["videoId"]))
        # elif search_result["id"]["kind"] == "youtube#channel":
        #     channels.append("%s (%s)" % (
        #         search_result["snippet"]["title"], search_result["id"]["channelId"]))
        # elif search_result["id"]["kind"] == "youtube#playlist":
        #     playlists.append("%s (%s)" % (
        #         search_result["snippet"]["title"], search_result["id"]["playlistId"]))

    # print("Videos:\n", "\n".join(videos), "\n")
    # print("Channels:\n", "\n".join(channels), "\n")
    # print("Playlists:\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=50)
    args = argparser.parse_args()

    nextPageToken = youtube_search('', args)

    while nextPageToken:
        print("nextPageToken: " + nextPageToken)
        nextPageToken = youtube_search(nextPageToken, args)

    print(','.join(channel_ids))
    # except HttpError, e:
    #     print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
