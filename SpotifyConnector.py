import pprint
import sys
import os
import subprocess

import spotipy
import spotify
import spotipy.util as util
import time
import datetime
import requests
import json

client_id = "c6e2c7784be448a683604b5d115d8a8f"
client_secret = "a6a3a7242e824e37abd61240ea162cc6"
grant_type = 'client_credentials'

def generateToken():
    #Generates a new token to get around 1-hour token expiry
    body_params = {'grant_type' : grant_type}

    url='https://accounts.spotify.com/api/token'

    response=requests.post(url, data=body_params, auth = (client_id, client_secret))

    json_response = json.loads(response.text)
    print json_response
    token = json_response[u'access_token']
    return token

def addPlaylist(genre, valence):
    #token setup
    token = 'BQCECxiGjCH3hV_GTBxR9kDBqh0vEynEkv0NphQZM3Tv6WCu9pVtgOZ05S9jQ_uBArhm8P8U3681wL5uEEdNnQSkr_jweY9TExWtW-OfsdS0EOZGF7cDpHazbEn5DLbV9svXBlt2MbFSHR9gXq6e8CXzarDoD9wAcM10YEdk4QEj17buW5wU94YXiwMDQFYZR2XLZQ__Maiz9bkoeTorsfJbmH4tHt2QnBVBS9J95yuPirOwgwGzJl1dPo5zUC1hFtoxhabotQ1f60OS9M4vW0rOXmPdm2ZvJHpGpL_rOHqy_wr7g8o2UhiRM7uN'
    token = generateToken()
    sp = spotipy.Spotify(token)
    sp.trace = False

    #new playlist housekeeping
    user = 'csdg_interns_2016'
    playlistname = "Generated Playlist: " + str(datetime.datetime.now())
    oldList = sp.user_playlists(user)
    oldListId = oldList[u'items'][0][u'id']

    #valence-based track generation
    trackids = []
    #valenceArg = {'target_valence' : str(valence)}
    tracks = sp.recommendations(seed_genres = [genre], limit = 5, target_valence = valence)
    for song in tracks[u'tracks']:
        trackids.append(song[u'id'])

    #Shuffles new songs to add
    trackids.sort()

    #Update aggregate playlist
    sp.user_playlist_replace_tracks(user, oldListId, trackids)

    #create new playlist and return URL
    newlist = sp.user_playlist_create(user, playlistname)
    sp.user_playlist_add_tracks(user, newlist[u'id'], trackids)

addPlaylist('rock', 0.99)
